import player
from dev import (
    GENERATION_PIECE,
    MUTATION_RATE,
    MUTATION_BAD_TO_KEEP,
    MUTATION_CUT_OFF,
    MUTATION_MIXING_RATE,
    MUTATION_MODIFY_CHANCE,
    POPULATION,
)
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Tetrisgame:
    def __init__(self, boardwidth, boardheight, ppf=30, gravity=60, tolerant=120):
        self.frame = 0
        self.gravityframe = 0
        self.gravity = gravity
        self.tolerant = tolerant
        self.width = boardwidth
        self.height = boardheight
        self.ppf = ppf
        self.winner = None
        self.playerleft = 1
        self.player = []
        self.alive = []
        self.generationframe = GENERATION_PIECE
        self.generation = 0
        self.ypoint = []
        self.xpoint = []
        self.frame = 0
        self.drawpieces()
        self.target()
        self.generation += 1
        self.start()

    def start(self):
        data = None

        for x in range(POPULATION):
            self.addplayer()
            if x == 0 and data != None:
                print("save1")
                a = data["a"]
                b = data["b"]
                c = data["c"]
                self.player[x].nnet.loaddata(a, b, c)
            elif x == 1 and data != None:
                print("save2")
                a = data["d"]
                b = data["e"]
                c = data["f"]
                self.player[x].nnet.loaddata(a, b, c)

    def animate(self):
        plt.cla()
        plt.plot(self.xpoint, self.ypoint)

    def reset(self):
        self.playerleft = len(self.player)
        max = 0
        for player in self.player:
            if player.totalpiece > max:
                max = player.totalpiece
        if self.generation > 3:
            self.generationframe = max * 2 + 50
        self.frame = 0
        self.evolve_population()
        self.alive = []
        for player in self.player:
            player.reset()
            self.alive.append(player)
        self.drawpieces()
        self.target()
        self.ypoint.append(self.generation)
        self.generation += 1

    def gamestep(self):
        self.frame += 1
        self.playerleft = len(self.alive)
        for player in self.alive:
            player.gamestep()
        if self.playerleft <= 0:
            for player in self.alive:
                self.winner = player
                print(self.winner)
            print("winreset")
            self.reset()
        elif self.frame == self.generationframe:
            print("maxpiecereset")
            self.reset()

    def drawpieces(self):
        bag = []
        drawed = []
        for x in range(7):
            ran = random.randint(1, 7)
            repeated = False
            for piece in drawed:
                if ran == piece:
                    repeated = True
            while repeated == True:
                repeated = False
                ran = random.randint(1, 7)
                for piece in drawed:
                    if ran == piece:
                        repeated = True
            bag.append(ran)
            drawed.append(ran)
        for player in self.alive:
            player.sequel.extend(bag)
        return

    def target(self):
        if len(self.player) == 2:
            self.player[0].target = self.player[1]
            self.player[1].target = self.player[0]
        elif len(self.player) > 2:
            for player1 in self.alive:
                while player1.target == None:
                    playerchosen = random.choice(self.player)
                    if (
                        player1 == playerchosen
                        or playerchosen.targeted
                        or playerchosen.target == player1
                    ):
                        continue
                    else:
                        player1.target = playerchosen

    def topout(self, player):
        if player in self.alive:
            self.alive.remove(player)
        self.target()

    def addplayer(self, ishuman=False):
        if ishuman:
            newplayer = player.Player(self)
            self.player.append(newplayer)
            self.alive.append(newplayer)
            return newplayer
        else:
            newplayer = player.Player(self)
            self.player.append(newplayer)
            self.alive.append(newplayer)
            return newplayer

    def evolve_population(self):
        for b in self.player:
            b.fitness = (
                b.totalpiece
                + b.linesent * 10
                + b.garbagecleared * 10
                + b.linesclear * 10
            )
        self.player.sort(key=lambda x: x.fitness, reverse=True)
        self.xpoint.append(self.player[0].fitness)
        for i, b in enumerate(self.player[0:5]):
            print("fitness:", b.fitness)
        a = self.player[0]
        b = self.player[1]
        """np.savez(
            "test.npz",
            a=a.nnet.weight_input_hidden1,  
            b=a.nnet.weight_hidden1_hidden2,
            c=a.nnet.weight_hidden2_output,
            d=b.nnet.weight_input_hidden1,
            e=b.nnet.weight_hidden1_hidden2,
            f=b.nnet.weight_hidden2_output,
        )
        """
        cut_off = int(len(self.player) * MUTATION_CUT_OFF)
        good_player = self.player[0:cut_off]
        bad_player = self.player[cut_off:]
        num_bad_to_take = int(len(self.player) * MUTATION_BAD_TO_KEEP)

        for b in bad_player:
            b.nnet.modify_weights()

        new_players = []

        idx_bad_to_take = np.random.choice(
            np.arange(len(bad_player)), num_bad_to_take, replace=False
        )

        for index in idx_bad_to_take:
            new_players.append(bad_player[index])

        new_players.extend(good_player)

        children_needed = len(self.player) - len(new_players)

        while len(new_players) < len(self.player):
            idx_to_breed = np.random.choice(
                np.arange(len(good_player)), 2, replace=False
            )
            if idx_to_breed[0] != idx_to_breed[1]:
                new_player = player.create_offspring(
                    good_player[idx_to_breed[0]], good_player[idx_to_breed[1]], self
                )
                if random.random() < MUTATION_MODIFY_CHANCE:
                    new_player.nnet.modify_weights_offspring()
                new_players.append(new_player)
        self.player = new_players


class Singleplayer:
    def __init__(self, boardwidth, boardheight, gravity=60, tolerant=120):
        self.frame = 0
        self.ppf = 1
        self.gravity = gravity
        self.tolerant = tolerant
        self.width = boardwidth
        self.height = boardheight
        self.player = []
        self.alive = []
        self.drawpieces()
        self.playercount = 2
        self.playerleft = 0

    def reset(self):
        self.playerleft = len(self.player)
        self.frame = 0
        self.alive = []
        for player in self.player:
            player.reset()
            self.alive.append(player)
            self.target()
        self.drawpieces()

    def gamestep(self):
        self.frame += 1
        self.playerleft = len(self.alive)
        for player in self.alive:
            player.gamestep()
        if self.playerleft <= 0:
            for player in self.alive:
                self.winner = player
                print(self.winner)
            print("winreset")
            self.reset()

    def drawpieces(self):
        bag = []
        drawed = []
        for x in range(7):
            ran = random.randint(1, 7)
            repeated = False
            for piece in drawed:
                if ran == piece:
                    repeated = True
            while repeated == True:
                repeated = False
                ran = random.randint(1, 7)
                for piece in drawed:
                    if ran == piece:
                        repeated = True
            bag.append(ran)
            drawed.append(ran)
        for player in self.alive:
            player.sequel.extend(bag)
        return

    def target(self):
        if len(self.player) == 2:
            self.player[0].target = self.player[1]
            self.player[1].target = self.player[0]
        elif len(self.player) > 2:
            for player1 in self.alive:
                while player1.target == None:
                    playerchosen = random.choice(self.player)
                    if (
                        player1 == playerchosen
                        or playerchosen.targeted
                        or playerchosen.target == player1
                    ):
                        continue
                    else:
                        player1.target = playerchosen

    def topout(self, player):
        if player in self.alive:
            self.alive.remove(player)
        self.target()

    def addplayer(self, ishuman=False):
        if ishuman:
            newplayer = player.Player(self)
            self.player.append(newplayer)
            self.alive.append(newplayer)
            return newplayer
        else:
            newplayer = player.Player(self)
            self.player.append(newplayer)
            self.alive.append(newplayer)
            return newplayer
