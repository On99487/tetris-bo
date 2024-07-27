import random
import numpy as np
import math
from training import Nnet
from tetris import Tetrisgame

CURRENTPIECE = 100
O = np.array([[1, 1], [1, 1]])
I = np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]])
S = np.array([[0, 1, 1], [1, 1, 0], [0, 0, 0]])
Z = np.array([[1, 1, 0], [0, 1, 1], [0, 0, 0]])
L = np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]])
J = np.array([[1, 0, 0], [1, 1, 1], [0, 0, 0]])
T = np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]])


class Player:
    def __init__(
        self,
        Tetrisgame: Tetrisgame,
    ):
        self.Tetrisgame = Tetrisgame
        self.width = Tetrisgame.width
        self.height = Tetrisgame.height + 3
        self.ppf = Tetrisgame.ppf
        self.gravity = Tetrisgame.gravity
        self.tolerant = Tetrisgame.tolerant
        self.human = False
        self.toppedout = False
        # static
        self.frame = 0
        self.linesclear = 0
        self.totalpiece = 0
        self.linesent = 0
        self.garbagecleared = 0
        self.vsscore = 0
        self.pps = 0
        # start
        self.reset()
        self.nnet = Nnet(239, 10, 10, 10 + 4)

    def reset(self):
        self.board = np.zeros((self.height, self.width)).tolist()
        self.currentpiece = None
        self.rotation = None
        self.position = None
        self.holdpiece = None
        self.sequel = []
        self.btb = 0
        self.combo = 0
        self.garbagebar = 0
        self.tspin = False
        self.minitspin = False
        self.toppedout = False
        self.target = None
        self.targeted = False
        # static
        self.frame = 0
        self.gravityframe = 1
        self.tolerantframe = 1
        self.aiframe = 1
        self.totalpiece = 0
        self.linesent = 0
        self.linesclear = 0
        self.garbagecleared = 0
        self.vsscore = 0
        self.opponent = None
        self.fitness = 0

    def gamestep(self, gravity=False, input=None):
        # 1 if no piece, get piece
        self.frame += 1

        if self.currentpiece == None:
            self.getpiece()
        # 2 if no current piece spawnpiece
        if self.position == None:
            self.spawnpiece()
        # 3 gravity
        if not self.checkdrop():
            self.gravityframe += 1
        else:
            self.tolerantframe += 1
        if self.tolerantframe % self.tolerant == 0:
            self.gravityfall()
        # if self.gravityframe % self.gravity == 0:
        #    self.gravityfall()
        self.aiframe += 1
        # 4 take input
        # match input:
        if not self.human and self.aiframe % self.ppf == 0:
            self.aimove()
            self.updateposition()
            if self.checkdrop():

                self.drop()
        #    case
        # 5 update piece and board
        else:
            self.updateposition()
        self.vsscore = round(
            ((self.linesent + self.garbagecleared) / (self.frame / 60)) * 100, 2
        )
        self.pps = round(self.totalpiece / (self.frame / 60), 2)

    def getpiece(self):
        if len(self.sequel) < 100:
            self.Tetrisgame.drawpieces()
        self.currentpiece = self.sequel.pop(0)

    def spawnpiece(self):

        piece = self.currentpiece
        self.rotation = 1
        match piece:
            case 1:
                self.position = (
                    round(self.width / 2) - 1,
                    23 - self.height,
                )

            case 2:
                self.position = (
                    round(self.width / 2) - 2,
                    23 - self.height,
                )

            case 3:
                self.position = (
                    round(self.width / 2) - 2,
                    23 - self.height,
                )

            case 4:
                self.position = (
                    round(self.width / 2) - 2,
                    23 - self.height,
                )

            case 5:
                self.position = (
                    round(self.width / 2) - 2,
                    23 - self.height,
                )

            case 6:
                self.position = (
                    round(self.width / 2) - 2,
                    23 - self.height,
                )

            case 7:
                self.position = (
                    round(self.width / 2) - 2,
                    23 - self.height,
                )
        y = self.position[1]
        x = self.position[0]
        # checktopout
        match self.currentpiece:
            case 1:
                matrix = O
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if self.board[y + i][x + j] != 0 and matrix[i][j] == 1:
                            self.topout()
                            break
            case 2:
                matrix = I
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if self.board[y + i][x + j] != 0 and matrix[i][j] == 1:
                            self.topout()
                            break
            case 3:
                matrix = S
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if self.board[y + i][x + j] != 0 and matrix[i][j] == 1:
                            self.topout()
                            break
            case 4:
                matrix = Z
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if self.board[y + i][x + j] != 0 and matrix[i][j] == 1:
                            self.topout()
                            break
            case 5:
                matrix = L
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if self.board[y + i][x + j] != 0 and matrix[i][j] == 1:
                            self.topout()
                            break
            case 6:
                matrix = J
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if self.board[y + i][x + j] != 0 and matrix[i][j] == 1:
                            self.topout()
                            break
            case 7:
                matrix = T
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if self.board[y + i][x + j] != 0 and matrix[i][j] == 1:
                            self.topout()
                            break
        self.updateposition()

    def updateposition(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == CURRENTPIECE:
                    self.board[y][x] = 0
        y = self.position[1]
        x = self.position[0]
        match self.currentpiece:
            case 1:
                matrix = np.rot90(O, self.rotation - 1, (1, 0))
            case 2:
                matrix = np.rot90(I, self.rotation - 1, (1, 0))
            case 3:
                matrix = np.rot90(S, self.rotation - 1, (1, 0))
            case 4:
                matrix = np.rot90(Z, self.rotation - 1, (1, 0))
            case 5:
                matrix = np.rot90(L, self.rotation - 1, (1, 0))
            case 6:
                matrix = np.rot90(J, self.rotation - 1, (1, 0))
            case 7:
                matrix = np.rot90(T, self.rotation - 1, (1, 0))
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i, j] != 0:
                    self.board[y + i][x + j] = CURRENTPIECE

    def gravityfall(self):
        if self.checkdrop():
            self.drop()
        else:
            self.position = (self.position[0], self.position[1] + 1)
            self.updateposition()

    def checkdrop(self, position=None, rotation=None):
        piece = self.currentpiece
        if position == None:
            position = self.position
        if rotation == None:
            rotation = self.rotation
        y = position[1]
        x = position[0]
        match piece:
            case 1:
                if self.height - 1 - y == 1:
                    return True
                if not (
                    (self.board[y + 2][x] == 0) and (self.board[y + 2][x + 1] == 0)
                ):
                    return True
            case 2:
                match rotation:
                    case 1:
                        if self.height - 1 - y == 1:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                            and (self.board[y + 2][x + 3] == 0)
                        ):
                            return True
                    case 2:
                        if self.height - 1 - y == 3:
                            return True
                        if not ((self.board[y + 4][x + 2] == 0)):
                            return True
                    case 3:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                            and (self.board[y + 3][x + 2] == 0)
                            and (self.board[y + 3][x + 3] == 0)
                        ):
                            return True
                    case 4:
                        if self.height - 1 - y == 3:
                            return True
                        if not ((self.board[y + 4][x + 1] == 0)):
                            return True
            case 3:
                match rotation:
                    case 1:
                        if self.height - 1 - y == 1:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 1][x + 2] == 0)
                        ):
                            return True
                    case 2:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 3][x + 2] == 0)
                        ):
                            return True
                    case 3:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                        ):
                            return True
                    case 4:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                        ):
                            return True
            case 4:
                match rotation:
                    case 1:
                        if self.height - 1 - y == 1:
                            return True
                        if not (
                            (self.board[y + 2][x + 2] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 1][x] == 0)
                        ):
                            return True
                    case 2:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 2][x + 2] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                        ):
                            return True
                    case 3:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x + 2] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                            and (self.board[y + 2][x] == 0)
                        ):
                            return True
                    case 4:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 3][x] == 0)
                        ):
                            return True
            case 5:
                match rotation:
                    case 1:
                        if self.height - 1 - y == 1:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                        ):
                            return True
                    case 2:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x + 1] == 0)
                            and (self.board[y + 3][x + 2] == 0)
                        ):
                            return True
                    case 3:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                        ):
                            return True
                    case 4:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 1][x] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                        ):
                            return True
            case 6:
                match rotation:
                    case 1:
                        if self.height - 1 - y == 1:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                        ):
                            return True
                    case 2:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x + 1] == 0)
                            and (self.board[y + 1][x + 2] == 0)
                        ):
                            return True
                    case 3:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x + 2] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 2][x] == 0)
                        ):
                            return True
                    case 4:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                        ):
                            return True
            case 7:
                match rotation:
                    case 1:
                        if self.height - 1 - y == 1:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 2][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                        ):
                            return True
                    case 2:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 3][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                        ):
                            return True
                    case 3:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                            and (self.board[y + 2][x + 2] == 0)
                        ):
                            return True
                    case 4:
                        if self.height - 1 - y == 2:
                            return True
                        if not (
                            (self.board[y + 2][x] == 0)
                            and (self.board[y + 3][x + 1] == 0)
                        ):
                            return True

    def lowestpossiblemove(self, colume, rotation):
        x = -1
        match self.currentpiece:
            case 1:
                x = colume
                if colume > 10 - 2:
                    x = 10 - 2
            case 2:
                match rotation:
                    case 1:
                        x = colume
                        if colume > 10 - 4:
                            x = 10 - 4
                    case 2:
                        x = colume - 2
                    case 3:
                        x = colume
                        if colume > 10 - 4:
                            x = 10 - 4
                    case 4:
                        x = colume - 1
            case 3 | 4 | 5 | 6 | 7:
                match rotation:
                    case 1:
                        x = colume
                        if colume > 10 - 3:
                            x = 10 - 3
                    case 2:
                        x = colume - 1
                        if colume > 10 - 2:
                            x = 10 - 2
                    case 3:
                        x = colume
                        if colume > 10 - 3:
                            x = 10 - 3
                    case 4:
                        x = colume
                        if colume > 10 - 2:
                            x = 10 - 2
        y = 23
        while y > -2:
            if self.checkvalidmove(
                position=(x, y), rotation=rotation, piece=self.currentpiece
            ) and self.checkdrop((x, y), rotation):
                self.position = (x, y)
                self.rotation = rotation

            y -= 1

    def drop(self):
        # drop
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == CURRENTPIECE:
                    self.board[y][x] = self.currentpiece
        self.currentpiece = None
        self.position = None
        self.rotation = None
        # aftermath
        cleared = []
        for i, row in enumerate(self.board):
            if not 0 in row:
                cleared.append(i)
        cleared.reverse()
        for y in cleared:
            if self.board[y][0] == 8 == self.board[y][1]:
                self.garbagecleared += 1
            for i in range(y + 1):
                if y - i - 1 >= 0:
                    self.board[y - i] = self.board[y - i - 1]
                else:
                    self.board[y - i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(len(cleared)):
                cleared[i] += 1
        if len(cleared) > 0:
            self.lineclear(len(cleared))
            self.combo += 1
            if len(cleared) == 4 or self.tspin or self.minitspin:
                self.btb += 1
                print("btb", self.btb)
            else:
                self.btb = 0
        else:
            self.combo = 0
            self.countgarbage()
        self.tspin = False
        self.minitspin = False
        self.totalpiece += 1
        self.gravityframe = 1
        self.tolerantframe = 1
        self.getpiece()
        self.spawnpiece()

    def topout(self):
        self.Tetrisgame.topout(self)
        self.toppedout = True

    ##input
    def left(self):
        y = self.position[1]
        x = self.position[0]
        if self.checkvalidmove((x - 1, y), self.rotation):
            self.position = (self.position[0] - 1, self.position[1])
            self.updateposition()

    def right(self):
        y = self.position[1]
        x = self.position[0]
        if self.checkvalidmove((x + 1, y), self.rotation):
            self.position = (self.position[0] + 1, self.position[1])
            self.updateposition()

    def clockwiserotate(self):
        if self.checkvalidmove(self.position, self.rotation + 1):
            self.rotation += 1
            if self.currentpiece == 7:
                x = self.position[0]
                y = self.position[1]
                corner = 0
                if 0 != self.board[y][x] != CURRENTPIECE:
                    corner += 1
                if 0 != self.board[y + 2][x] != CURRENTPIECE:
                    corner += 1
                if 0 != self.board[y][x + 2] != CURRENTPIECE:
                    corner += 1
                if 0 != self.board[y + 2][x + 2] != CURRENTPIECE:
                    corner += 1
                if corner > 2:
                    self.tspin = True
        else:
            x = self.position[0]
            y = self.position[1]
            match self.currentpiece:
                case 3 | 4 | 5 | 6 | 7:
                    match self.rotation + 1:
                        case 2:
                            if self.checkvalidmove((x - 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if x == -1:
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            self.minitspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.minitspin = True
                            elif self.checkvalidmove((x - 1, y - 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y - 1)
                            elif self.checkvalidmove((x, y + 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x, y + 2)
                            elif self.checkvalidmove((x - 1, y + 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y + 2)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if y == -1:
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            self.tspin = True
                                    elif y == self.width - 2:
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            self.tspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.tspin = True
                        case 3:
                            if self.checkvalidmove((x + 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y)
                            elif self.checkvalidmove((x + 1, y + 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y + 1)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if y == -1:
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            self.tspin = True
                                    elif y == self.width - 2:
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            self.tspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.tspin = True
                            elif self.checkvalidmove((x, y - 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x, y - 2)
                            elif self.checkvalidmove((x + 1, y - 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y - 2)
                        case 4:
                            if self.checkvalidmove((x + 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y)
                            elif self.checkvalidmove((x + 1, y - 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y - 1)
                            elif self.checkvalidmove((x, y + 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x, y + 2)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if y == -1:
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            self.minitspin = True
                                    elif y == self.width - 2:
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            self.minitspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.minitspin = True
                            elif self.checkvalidmove((x + 1, y + 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y + 2)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if y == -1:
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            self.tspin = True
                                    elif y == self.width - 2:
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            self.tspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.tspin = True
                        case 5:
                            if self.checkvalidmove((x - 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y)
                            elif self.checkvalidmove((x - 1, y + 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y + 1)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if y == self.height - 2:
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            self.minitspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.minitspin = True
                            elif self.checkvalidmove((x, y - 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x, y - 2)
                            elif self.checkvalidmove((x - 1, y - 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y - 2)
                case 2:
                    match self.rotation + 1:
                        case 2:
                            if self.checkvalidmove((x - 2, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 2, y)
                            elif self.checkvalidmove((x + 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y)
                            elif self.checkvalidmove((x - 2, y + 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 2, y + 1)
                            elif self.checkvalidmove((x + 1, y - 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y - 2)
                        case 3:
                            if self.checkvalidmove((x - 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y)
                            elif self.checkvalidmove((x + 2, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 2, y)
                            elif self.checkvalidmove((x - 1, y - 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y - 2)
                            elif self.checkvalidmove((x + 2, y + 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 2, y + 1)
                        case 4:
                            if self.checkvalidmove((x + 2, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 2, y)
                            elif self.checkvalidmove((x - 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y)
                            elif self.checkvalidmove((x + 2, y - 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 2, y - 1)
                            elif self.checkvalidmove((x - 1, y + 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 1, y + 2)
                        case 5:
                            if self.checkvalidmove((x + 1, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y)
                            elif self.checkvalidmove((x - 2, y), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 2, y)
                            elif self.checkvalidmove((x + 1, y + 2), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x + 1, y + 2)
                            elif self.checkvalidmove((x - 2, y - 1), self.rotation + 1):
                                self.rotation += 1
                                self.position = (x - 2, y - 1)
        # check tspin

        if self.rotation > 4:
            self.rotation = 1
        self.updateposition()

    def anticlockwiserotate(self):
        if self.checkvalidmove(self.position, self.rotation - 1):
            self.rotation -= 1
            if self.currentpiece == 7:
                x = self.position[0]
                y = self.position[1]
                corner = 0
                if 0 != self.board[y][x] != CURRENTPIECE:
                    corner += 1
                if 0 != self.board[y + 2][x] != CURRENTPIECE:
                    corner += 1
                if 0 != self.board[y][x + 2] != CURRENTPIECE:
                    corner += 1
                if 0 != self.board[y + 2][x + 2] != CURRENTPIECE:
                    corner += 1
                if corner > 2:
                    self.tspin = True
        else:
            x = self.position[0]
            y = self.position[1]
            match self.currentpiece:
                case 3 | 4 | 5 | 6 | 7:
                    match self.rotation - 1:
                        case 1:
                            if self.checkvalidmove((x + 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y)

                            elif self.checkvalidmove((x + 1, y + 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y + 1)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if y == self.height - 2:
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            self.minitspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.minitspin = True
                            elif self.checkvalidmove((x, y - 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x, y - 2)
                            elif self.checkvalidmove((x + 1, y - 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y - 2)

                        case 2:
                            if self.checkvalidmove((x - 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y)

                            elif self.checkvalidmove((x - 1, y - 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y - 1)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    corner = 0
                                    if 0 != self.board[y][x] != CURRENTPIECE:
                                        corner += 1
                                    if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                        corner += 1
                                    if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                        corner += 1
                                    if 0 != self.board[y + 2][x + 2] != CURRENTPIECE:
                                        corner += 1
                                    if corner > 2:
                                        self.minitspin = True
                            elif self.checkvalidmove((x, y + 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x, y + 2)
                            elif self.checkvalidmove((x - 1, y + 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y + 2)

                        case 3:
                            if self.checkvalidmove((x - 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y)
                            elif self.checkvalidmove((x - 1, y + 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y + 1)
                            elif self.checkvalidmove((x, y - 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x, y - 2)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if x == -1:
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            self.minitspin = True
                                    elif x == self.width - 2:
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            self.minitspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.minitspin = True
                            elif self.checkvalidmove((x - 1, y - 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y - 2)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    if x == -1:
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            self.tspin = True
                                    elif x == self.width - 2:
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            self.tspin = True
                                    else:
                                        corner = 0
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.tspin = True
                        case 0:
                            if self.checkvalidmove((x + 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y)
                                if self.currentpiece == 7:
                                    x = self.position[0]
                                    y = self.position[1]
                                    corner = 0
                                    if x < self.width - 1:
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            self.minitspin = True
                                    else:
                                        if 0 != self.board[y][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y + 2][x] != CURRENTPIECE:
                                            corner += 1
                                        if 0 != self.board[y][x + 2] != CURRENTPIECE:
                                            corner += 1
                                        if (
                                            0
                                            != self.board[y + 2][x + 2]
                                            != CURRENTPIECE
                                        ):
                                            corner += 1
                                        if corner > 2:
                                            self.minitspin = True
                            elif self.checkvalidmove((x + 1, y - 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y - 1)
                            elif self.checkvalidmove((x, y + 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x, y + 2)
                            elif self.checkvalidmove((x + 1, y + 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y + 2)
                case 2:
                    match self.rotation - 1:
                        case 1:
                            if self.checkvalidmove((x + 2, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 2, y)
                            elif self.checkvalidmove((x - 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y)
                            elif self.checkvalidmove((x + 2, y - 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 2, y - 1)
                            elif self.checkvalidmove((x - 1, y + 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y + 2)
                        case 2:
                            if self.checkvalidmove((x + 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y)
                            elif self.checkvalidmove((x - 2, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 2, y)
                            elif self.checkvalidmove((x + 1, y + 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y + 2)
                            elif self.checkvalidmove((x - 2, y - 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 2, y - 1)
                        case 3:
                            if self.checkvalidmove((x - 2, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 2, y)
                            elif self.checkvalidmove((x + 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y)
                            elif self.checkvalidmove((x - 2, y + 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 2, y + 1)
                            elif self.checkvalidmove((x + 1, y - 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 1, y - 2)
                        case 4:
                            if self.checkvalidmove((x - 1, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y)
                            elif self.checkvalidmove((x + 2, y), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 2, y)
                            elif self.checkvalidmove((x - 1, y - 2), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x - 1, y - 2)
                            elif self.checkvalidmove((x + 2, y + 1), self.rotation - 1):
                                self.rotation -= 1
                                self.position = (x + 2, y + 1)
        if self.rotation < 1:
            self.rotation = 4
        self.updateposition()

    def spin180(self):
        rotation = self.rotation + 2
        if rotation > 4:
            rotation = rotation % 4
        if self.checkvalidmove(self.position, rotation):
            self.rotation += 2
        else:
            x = self.position[0]
            y = self.position[1]
            match rotation:
                case 3:
                    if self.checkvalidmove((x, y - 1), rotation):
                        self.rotation += 2
                        self.position = (x, y - 1)
                    elif self.checkvalidmove((x + 1, y - 1), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y - 1)
                    elif self.checkvalidmove((x - 1, y - 1), rotation):
                        self.rotation += 2
                        self.position = (x - 1, y - 1)
                    elif self.checkvalidmove((x + 1, y), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y)
                    elif self.checkvalidmove((x - 1, y), rotation):
                        self.rotation += 2
                        self.position = (x - 1, y)
                case 1:
                    if self.checkvalidmove((x, y + 1), rotation):
                        self.rotation += 2
                        self.position = (x, y + 1)
                    elif self.checkvalidmove((x + 1, y + 1), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y + 1)
                    elif self.checkvalidmove((x + 1, y + 1), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y + 1)
                    elif self.checkvalidmove((x - 1, y), rotation):
                        self.rotation += 2
                        self.position = (x - 1, y)
                    elif self.checkvalidmove((x + 1, y), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y)
                case 4:
                    if self.checkvalidmove((x + 1, y), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y)
                    elif self.checkvalidmove((x + 1, y - 2), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y - 2)
                    elif self.checkvalidmove((x + 1, y - 1), rotation):
                        self.rotation += 2
                        self.position = (x + 1, y - 1)
                    elif self.checkvalidmove((x, y - 2), rotation):
                        self.rotation += 2
                        self.position = (x, y - 2)
                    elif self.checkvalidmove((x, y - 1), rotation):
                        self.rotation += 2
                        self.position = (x, y - 1)
                case 2:
                    if self.checkvalidmove((x - 1, y), rotation):
                        self.rotation += 2
                        self.position = (x - 1, y)
                    elif self.checkvalidmove((x - 1, y - 2), rotation):
                        self.rotation += 2
                        self.position = (x - 1, y - 2)
                    elif self.checkvalidmove((x - 1, y - 1), rotation):
                        self.rotation += 2
                        self.position = (x - 1, y - 1)
                    elif self.checkvalidmove((x, y - 2), rotation):
                        self.rotation += 2
                        self.position = (x, y - 2)
                    elif self.checkvalidmove((x, y - 1), rotation):
                        self.rotation += 2
                        self.position = (x, y - 1)

        if self.rotation > 4:
            self.rotation = self.rotation % 4
        self.updateposition()

    def checkvalidmove(self, position, rotation, piece=None):
        if rotation > 4:
            rotation = 1
        if rotation < 1:
            rotation = 4
        if piece == None:
            piece = self.currentpiece
        x = position[0]
        y = position[1]
        if y < self.position[1]:
            return False
        match piece:
            case 1:
                matrix = np.rot90(O, rotation - 1, (1, 0))
            case 2:
                matrix = np.rot90(I, rotation - 1, (1, 0))
            case 3:
                matrix = np.rot90(S, rotation - 1, (1, 0))
            case 4:
                matrix = np.rot90(Z, rotation - 1, (1, 0))
            case 5:
                matrix = np.rot90(L, rotation - 1, (1, 0))
            case 6:
                matrix = np.rot90(J, rotation - 1, (1, 0))
            case 7:
                matrix = np.rot90(T, rotation - 1, (1, 0))
        lbound = None
        rbound = None
        dbound = None
        match piece:
            case 1:
                lbound = 0
                rbound = 1
                dbound = 1
            case 2:
                match rotation:
                    case 1:
                        lbound = 0
                        rbound = 3
                        dbound = 1
                    case 2:
                        lbound = 2
                        rbound = 2
                        dbound = 3
                    case 3:
                        lbound = 0
                        rbound = 3
                        dbound = 2
                    case 4:
                        lbound = 1
                        rbound = 1
                        dbound = 3
            case 3:
                match rotation:
                    case 1:
                        lbound = 0
                        rbound = 2
                        dbound = 1
                    case 2:
                        lbound = 1
                        rbound = 2
                        dbound = 2
                    case 3:
                        lbound = 0
                        rbound = 2
                        dbound = 2
                    case 4:
                        lbound = 0
                        rbound = 1
                        dbound = 2
            case 4:
                match rotation:
                    case 1:
                        lbound = 0
                        rbound = 2
                        dbound = 1
                    case 2:
                        lbound = 1
                        rbound = 2
                        dbound = 2
                    case 3:
                        lbound = 0
                        rbound = 2
                        dbound = 2
                    case 4:
                        lbound = 0
                        rbound = 1
                        dbound = 2
            case 5:
                match rotation:
                    case 1:
                        lbound = 0
                        rbound = 2
                        dbound = 1
                    case 2:
                        lbound = 1
                        rbound = 2
                        dbound = 2
                    case 3:
                        lbound = 0
                        rbound = 2
                        dbound = 2
                    case 4:
                        lbound = 0
                        rbound = 1
                        dbound = 2
            case 6:
                match rotation:
                    case 1:
                        lbound = 0
                        rbound = 2
                        dbound = 1
                    case 2:
                        lbound = 1
                        rbound = 2
                        dbound = 2
                    case 3:
                        lbound = 0
                        rbound = 2
                        dbound = 2
                    case 4:
                        lbound = 0
                        rbound = 1
                        dbound = 2
            case 7:
                match rotation:
                    case 1:
                        lbound = 0
                        rbound = 2
                        dbound = 1
                    case 2:
                        lbound = 1
                        rbound = 2
                        dbound = 2
                    case 3:
                        lbound = 0
                        rbound = 2
                        dbound = 2
                    case 4:
                        lbound = 0
                        rbound = 1
                        dbound = 2
        if (0 - lbound > (x) or (x) > self.width - 1 - rbound) or (
            (y) > self.height - 1 - dbound
        ):
            return False
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 1:
                    if (
                        0 > (x + j)
                        or (x + j) > self.width - 1
                        or (y + i) > self.height - 1
                    ):
                        continue
                    if not (
                        self.board[y + i][x + j] == CURRENTPIECE
                        or self.board[y + i][x + j] == 0
                    ):

                        return False
        return True

    def hold(self):
        if self.holdpiece != None:
            x = self.currentpiece
            self.currentpiece = self.holdpiece
            self.holdpiece = x
            self.rotation = 1
            self.updateposition()

        else:
            self.holdpiece = self.currentpiece
            self.getpiece()
            for y in range(self.height):
                for x in range(self.width):
                    if self.board[y][x] == CURRENTPIECE:
                        self.board[y][x] = 0
            self.spawnpiece()

    def softdrop(self):
        yposition = self.position[1]
        xposition = self.position[0]
        for y in range(len(self.board)):
            if self.checkdrop(position=(xposition, yposition + y)):
                yposition += y
                self.position = (xposition, yposition)
                break
        self.updateposition()

    def harddrop(self):
        yposition = self.position[1]
        xposition = self.position[0]
        for y in range(len(self.board)):
            if self.checkdrop(position=(xposition, yposition + y)):
                yposition += y
                self.position = (xposition, yposition)
                break
        self.updateposition()
        self.drop()

    def randommove(self):
        attempt = 0
        self.aiframe = 1
        while attempt < 1000:
            attempt += 1
            position = (
                random.randint(0, self.width - 1),
                random.randint(self.position[1], self.height - 1),
            )
            rotation = random.randint(1, 4)
            if self.checkvalidmove(
                position=position, rotation=rotation, piece=self.currentpiece
            ):
                self.position = position
                self.rotation = rotation
                break

    ##multiPlayer
    def receivegarbage(self, lines):
        self.garbagebar += lines

    def lineclear(self, lines):
        power = 0
        linesend = 0
        # check pc
        pc = True
        for y in range(self.height):
            for x in range(self.width):
                if 0 != self.board[y][x] != CURRENTPIECE:
                    pc = False
                    break
        match self.btb:
            case num if num in range(0, 1):
                btb = 0
            case num if num in range(1, 3):
                btb = 1
            case num if num in range(3, 8):
                btb = 2
            case num if num in range(8, 24):
                btb = 3
            case num if num in range(24, 67):
                btb = 4
            case num if num in range(67, 185):
                btb = 5
            case num if num in range(185, 504):
                btb = 6
        if self.tspin:
            match lines:
                case 1:
                    power = 2 + btb
                    print("tspin single", power, self.btb)
                case 2:
                    power = 4 + btb
                    print("tspin double", power, self.btb)
                case 3:
                    power = 6 + btb
                    print("tspin triple", power, self.btb)
        elif self.minitspin:
            match lines:
                case 1:
                    power = 0 + btb
                    print("mini tspin single", power, self.btb)
                case 2:
                    power = 1 + btb
                    print("mini tspin double", power, self.btb)
        else:
            print("clearline")
            match lines:
                case 1:
                    power = 0
                    print("single")
                case 2:
                    power = 1
                    print("double")
                case 3:
                    power = 2
                    print("triple")
                case 4:
                    power = 4 + btb
                    print("quad", power, self.btb)
        if power != 0:
            linesend = math.floor(power * (1 + 0.25 * self.combo))
        else:
            match self.combo:
                case 0 | 1:
                    linesend = 0
                case 2 | 3 | 4 | 5:
                    linesend = 1
                case 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15:
                    linesend = 2
                case 16 | 17 | 18 | 19 | 20:
                    linesend = 3
        linesend += pc * 10
        if self.garbagebar != 0:
            if self.garbagebar >= linesend:
                self.garbagebar -= linesend
                linesend = 0
            elif self.garbagebar < linesend:
                linesend -= self.garbagebar
                self.garbagebar = 0
        print("linesended", linesend)
        self.linesclear += lines
        if linesend > 0:
            self.sendline(self.target, linesend)

    def sendline(self, target: "Player", lines):
        self.linesent += lines
        print(self.linesent)
        # target.receivegarbage(lines)

    def countgarbage(self):
        if 0 < self.garbagebar <= 8:
            place = random.randint(0, self.width - 1)
            # spawn
            garbage = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
            garbage[place] = 0
            for i in range(self.garbagebar):
                for y in range(self.height):
                    if y + 1 < self.height:
                        self.board[y] = self.board[y + 1]
                self.board[self.height - 1] = garbage
            self.garbagebar = 0
        if self.garbagebar > 8:
            place = random.randint(0, self.width - 1)
            # spawn
            garbage = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
            garbage[place] = 0
            for i in range(8):
                for y in range(self.height):
                    if y + 1 < self.height:
                        self.board[y] = self.board[y + 1]
                self.board[self.height - 1] = garbage
            self.garbagebar -= 8

    def aimove(self):
        self.aiframe = 1
        inputs = self.getinputs()
        self.receiveoutputs(self.nnet.get_outputs(inputs))

    def getinputs(self):
        boardarray = np.array(self.board.copy()).flatten()
        for num in boardarray:
            if CURRENTPIECE != num != 0:
                num = 1
            else:
                num = 0
        piecearray = [0, 0, 0, 0, 0, 0, 0]
        piecearray[self.currentpiece - 1] = 1
        match self.btb:
            case num if num in range(0, 1):
                btb = 0
            case num if num in range(1, 3):
                btb = 1 / 36
            case num if num in range(3, 8):
                btb = 4 / 36
            case num if num in range(8, 24):
                btb = 9 / 36
            case num if num in range(24, 67):
                btb = 16 / 36
            case num if num in range(67, 185):
                btb = 25 / 36
            case num if num in range(185, 504):
                btb = 1
        garbage = max(self.garbagebar, 40) / 40
        inputs = []
        inputs.extend(boardarray)
        inputs.extend(piecearray)
        inputs.append(btb)
        inputs.append(garbage)
        return inputs

    def receiveoutputs(self, outputarray):
        width = outputarray[0 : self.width]
        rotation = outputarray[self.width :]
        x = np.where(width == max(width))[0][0]
        r = np.where(rotation == max(rotation))[0][0] + 1
        self.lowestpossiblemove(x, r)


def create_offspring(p1, p2, tetrisgame):
    new_player = Player(tetrisgame)
    new_player.nnet.create_mixed_weights(net1=p1.nnet, net2=p2.nnet)
    return new_player
