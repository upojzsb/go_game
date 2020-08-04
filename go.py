import numpy as np


class ChessBoard:
    WHITE = -1
    SPACE = 0
    BLACK = 1
    valid_color = (-1, 0, 1)

    def __init__(self, shape=19):
        """
        :param shape: shape of chessboard
        """
        self.chessboard = np.zeros([shape, shape])
        self.breath = np.zeros_like(self.chessboard)
        self.shape = shape

    def validate_color(self, color):
        """
        :param color: color
        :return: whether or not the specified color is legal
        """
        if color in self.valid_color:
            return True
        return False

    def validate_pos(self, pos):
        """
        :param pos: position
        :return: whether or not the specified position is legal
        """
        if pos is None:
            return False
        return not (pos[0] >= self.shape or pos[0] < 0 or pos[1] >= self.shape or pos[1] < 0)

    def place_chess(self, pos=None, color=None):
        """
        :param pos: position that the chess will place
        :param color: color of that chess
        :return: None
        """
        if not self.validate_color(color) or not self.validate_pos(pos):
            raise ValueError('Pos and Color')
        if self.chessboard[pos] != self.SPACE:
            raise ValueError('Position ' + str(pos) + ' already has a chess')

        hypothesis_cb = self.chessboard.copy()
        hypothesis_cb[pos] = color

        count_breath = self.count_breath(pos=pos, chessboard=hypothesis_cb)

        if count_breath == 0:
            raise ValueError('Cannot suicide')

        print(pos, count_breath)
        self.chessboard[pos] = color
        print(pos, self.count_breath(pos=pos))

    def check_breath_situation(self, chessboard=None):
        """
        :param chessboard: chessboard
        :return: a list contain the breath situation like [white, black]
        """
        if chessboard is None:
            chessboard = self.chessboard

        white_breath = np.zeros_like(chessboard)
        black_breath = np.zeros_like(chessboard)
        ret = [white_breath, black_breath]

        for i in range(self.shape):
            for j in range(self.shape):
                if chessboard[i, j] == self.SPACE:
                    white_breath[i, j] = black_breath[i, j] = -1
                elif chessboard[i, j] == self.BLACK:
                    white_breath[i, j] = -1
                    black_breath[i, j] = self.count_breath(pos=(i, j), color=self.BLACK)
                elif chessboard[i, j] == self.WHITE:
                    white_breath[i, j] = self.count_breath(pos=(i, j), color=self.WHITE)
                    black_breath[i, j] = -1
        return ret

    def count_breath(self, pos=None, color=None, chessboard=None, vis_map=None):
        """
        :param pos: the position that need to be tested
        :param color: the color of the chess of the specified position (optional, used in recurrence)
        :param chessboard: chessboard
        :param vis_map: visit map
        :return: the breath of given chess which at specified position, -1 for space
        """
        if chessboard is None:
            chessboard = self.chessboard
        if color is None:
            color = chessboard[pos]
        if color == self.SPACE:
            return -1
        if not self.validate_pos(pos):
            return 0

        if vis_map is None:
            vis_map = np.zeros_like(chessboard)
        else:
            if vis_map[pos] != 0:
                return 0
            vis_map[pos] = 1

        if chessboard[pos] == self.SPACE:
            return 1
        if chessboard[pos] != color:
            return 0

        return self.count_breath(pos=(pos[0] - 1, pos[1]), color=color, chessboard=chessboard, vis_map=vis_map) + \
               self.count_breath(pos=(pos[0] + 1, pos[1]), color=color, chessboard=chessboard, vis_map=vis_map) + \
               self.count_breath(pos=(pos[0], pos[1] - 1), color=color, chessboard=chessboard, vis_map=vis_map) + \
               self.count_breath(pos=(pos[0], pos[1] + 1), color=color, chessboard=chessboard, vis_map=vis_map)

    def __str__(self):
        """
        :return: str
        """
        black = '●'
        white = '୦'
        space = '.'
        ret = ['  ']

        for i in range(self.shape):
            ret.append('%3d' % i)
        ret.append('\n')

        for i in range(self.shape):
            ret.append('%-4d' % i)
            for j in range(self.shape):
                if self.chessboard[i, j] == self.BLACK:
                    ret.append(black)
                elif self.chessboard[i, j] == self.WHITE:
                    ret.append(white)
                elif self.chessboard[i, j] == self.SPACE:
                    ret.append(space)
                ret.append('  ')
            ret.append('\n')

        return ''.join(ret)


if __name__ == '__main__':
    cb = ChessBoard()
    cb.place_chess((0, 0), cb.WHITE)
    cb.place_chess((1, 0), cb.BLACK)
    cb.place_chess((1, 1), cb.BLACK)
    cb.place_chess((0, 1), cb.BLACK)
    print(cb.count_breath(pos=(0, 0)))
    print(cb)
    for i in cb.check_breath_situation():
        print(i, '\n\n')
