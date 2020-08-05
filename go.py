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
        self.black_removed = 0
        self.white_removed = 0

    def _validate_color(self, color):
        """
        :param color: color
        :return: whether or not the specified color is legal
        """
        if color in self.valid_color:
            return True
        return False

    def _validate_pos(self, pos):
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
        :param color: color of the chess
        :return: None
        """
        if not self._validate_color(color) or not self._validate_pos(pos):
            raise ValueError('Position or Color')
        if self.chessboard[pos] != self.SPACE:
            raise ValueError('Position ' + str(pos) + ' already has a chess')
        #  The position is space
        #  Check whether it can remove another color's chess
        ori_cb = self.chessboard

        hypothesis_cb = ori_cb.copy()
        hypothesis_cb[pos] = color

        hyp_breath_situation = self.check_breath_situation(chessboard=hypothesis_cb)

        if color == self.WHITE:
            black_hyp = hyp_breath_situation[1]

            if np.sum(black_hyp == 0) != 0:
                self.black_removed += np.sum(black_hyp == 0)
                self.chessboard[black_hyp == 0] = self.SPACE
                self.chessboard[pos] = color
            else:  # check whether the white chess tries to suicide
                count_breath = self.count_breath(pos=pos, chessboard=hypothesis_cb)
                if count_breath == 0:
                    raise ValueError('Cannot suicide')
                self.chessboard[pos] = color
        elif color == self.BLACK:
            white_hyp = hyp_breath_situation[0]

            if np.sum(white_hyp == 0) != 0:
                self.white_removed += np.sum(white_hyp == 0)
                self.chessboard[white_hyp == 0] = self.SPACE
                self.chessboard[pos] = color
            else:  # check whether the black chess tries to suicide
                count_breath = self.count_breath(pos=pos, chessboard=hypothesis_cb)
                if count_breath == 0:
                    raise ValueError('Cannot suicide')
                self.chessboard[pos] = color

        # print(pos, count_breath)
        # print(pos, self.count_breath(pos=pos))

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
                    black_breath[i, j] = self.count_breath(pos=(i, j), color=self.BLACK, chessboard=chessboard)
                elif chessboard[i, j] == self.WHITE:
                    white_breath[i, j] = self.count_breath(pos=(i, j), color=self.WHITE, chessboard=chessboard)
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
        if not self._validate_pos(pos):
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

    def calculate_area(self, color=None, chessboard=None):
        # TODO: Finish this function
        pass

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

    while True:
        b = tuple([int(i) for i in input('B: ').split()])
        print(b)
        cb.place_chess(b, cb.BLACK)
        print(cb)

        w = tuple([int(i) for i in input('W: ').split()])
        print(w)
        cb.place_chess(w, cb.WHITE)
        print(cb)

    cb.place_chess((0, 0), cb.BLACK)
    cb.place_chess((1, 0), cb.WHITE)
    cb.place_chess((1, 1), cb.WHITE)
    cb.place_chess((0, 1), cb.WHITE)

    print(cb.count_breath(pos=(0, 0)))
    print(cb)
    # for i in cb.check_breath_situation():
    #     print(i, '\n\n')

