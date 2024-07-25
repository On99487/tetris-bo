import pygame
import sys
import time
import math

from player import Player, CURRENTPIECE
import tetris as tt
from dev import FPS, POPULATION

pygame.init()
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 127, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
purple = (191, 0, 255)
grey = (127, 127, 127)
white = (255, 255, 255)
screenwidth = 1600
screenheight = 900
background = black
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
playerFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

screen = pygame.display.set_mode((screenwidth, screenheight))

width = 10
height = 20
tetrisgame = None
ppf = 1
gravity = 1
humanplayer = None
aiplayer = False
humanplay = False
fps = 240
# tetrisboard
displayscale = 1
row = 0
colume = 0
blockdimension = 30 * displayscale
outerborderwidth = 5 * displayscale
innerborderwidth = 1 * displayscale
display = False


def displayblock(boardrect: pygame.Rect, player: Player):
    top = boardrect.top
    left = boardrect.left
    block = pygame.Rect((0, 0, blockdimension, blockdimension))
    for y in range(player.height):
        for x in range(player.width):
            block.center = (
                left
                + outerborderwidth
                + blockdimension / 2
                + x * (blockdimension + innerborderwidth),
                top
                + blockdimension / 2
                + (y - 3) * (blockdimension + innerborderwidth),
            )
            piece = player.board[y][x]
            if piece == CURRENTPIECE:
                piece = player.currentpiece
            match piece:
                case 0:
                    pygame.draw.rect(screen, black, block)
                case 1:
                    pygame.draw.rect(screen, yellow, block)
                case 2:
                    pygame.draw.rect(screen, cyan, block)
                case 3:
                    pygame.draw.rect(screen, green, block)
                case 4:
                    pygame.draw.rect(screen, red, block)
                case 5:
                    pygame.draw.rect(screen, orange, block)
                case 6:
                    pygame.draw.rect(screen, blue, block)
                case 7:
                    pygame.draw.rect(screen, purple, block)
                case 8:
                    pygame.draw.rect(screen, grey, block)


def displaybag(boardrect: pygame.Rect, player):
    panel = pygame.Rect(
        boardrect.left + boardrect.width,
        boardrect.top,
        boardrect.width / 2,
        boardrect.height / 2,
    )
    pygame.draw.rect(screen, white, panel)

    for i in range(4):
        center = (
            panel.left + panel.width / 2,
            panel.top + i * panel.height / 4 + panel.height / 8,
        )
        match player.sequel[i]:
            case 1:
                block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block1.center = (
                    center[0] - blockdimension / 2,
                    center[1] - blockdimension / 2,
                )
                block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block2.center = (
                    center[0] + blockdimension / 2,
                    center[1] - blockdimension / 2,
                )
                block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block3.center = (
                    center[0] - blockdimension / 2,
                    center[1] + blockdimension / 2,
                )
                block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block4.center = (
                    center[0] + blockdimension / 2,
                    center[1] + blockdimension / 2,
                )
                pygame.draw.rect(screen, yellow, block1)
                pygame.draw.rect(screen, yellow, block2)
                pygame.draw.rect(screen, yellow, block3)
                pygame.draw.rect(screen, yellow, block4)
            case 2:
                block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block1.center = (center[0] - blockdimension / 2, center[1])
                block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block2.center = (center[0] + blockdimension / 2, center[1])
                block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block3.center = (center[0] - blockdimension * 1.5, center[1])
                block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block4.center = (center[0] + blockdimension * 1.5, center[1])
                pygame.draw.rect(screen, cyan, block1)
                pygame.draw.rect(screen, cyan, block2)
                pygame.draw.rect(screen, cyan, block3)
                pygame.draw.rect(screen, cyan, block4)
            case 3:
                block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block1.center = (center[0], center[1] - blockdimension / 2)
                block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block2.center = (
                    center[0] + blockdimension,
                    center[1] - blockdimension / 2,
                )
                block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block3.center = (center[0], center[1] + blockdimension / 2)
                block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block4.center = (
                    center[0] - blockdimension,
                    center[1] + blockdimension / 2,
                )
                pygame.draw.rect(screen, green, block1)
                pygame.draw.rect(screen, green, block2)
                pygame.draw.rect(screen, green, block3)
                pygame.draw.rect(screen, green, block4)
            case 4:
                block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block1.center = (center[0], center[1] - blockdimension / 2)
                block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block2.center = (
                    center[0] - blockdimension,
                    center[1] - blockdimension / 2,
                )
                block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block3.center = (center[0], center[1] + blockdimension / 2)
                block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block4.center = (
                    center[0] + blockdimension,
                    center[1] + blockdimension / 2,
                )
                pygame.draw.rect(screen, red, block1)
                pygame.draw.rect(screen, red, block2)
                pygame.draw.rect(screen, red, block3)
                pygame.draw.rect(screen, red, block4)
            case 5:
                block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block1.center = (
                    center[0] + blockdimension,
                    center[1] - blockdimension / 2,
                )
                block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block2.center = (
                    center[0] + blockdimension,
                    center[1] + blockdimension / 2,
                )
                block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block3.center = (center[0], center[1] + blockdimension / 2)
                block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block4.center = (
                    center[0] - blockdimension,
                    center[1] + blockdimension / 2,
                )
                pygame.draw.rect(screen, orange, block1)
                pygame.draw.rect(screen, orange, block2)
                pygame.draw.rect(screen, orange, block3)
                pygame.draw.rect(screen, orange, block4)
            case 6:
                block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block1.center = (
                    center[0] - blockdimension,
                    center[1] - blockdimension / 2,
                )
                block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block2.center = (
                    center[0] + blockdimension,
                    center[1] + blockdimension / 2,
                )
                block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block3.center = (center[0], center[1] + blockdimension / 2)
                block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block4.center = (
                    center[0] - blockdimension,
                    center[1] + blockdimension / 2,
                )
                pygame.draw.rect(screen, blue, block1)
                pygame.draw.rect(screen, blue, block2)
                pygame.draw.rect(screen, blue, block3)
                pygame.draw.rect(screen, blue, block4)
            case 7:
                block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block1.center = (center[0], center[1] - blockdimension / 2)
                block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block2.center = (
                    center[0] + blockdimension,
                    center[1] + blockdimension / 2,
                )
                block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block3.center = (center[0], center[1] + blockdimension / 2)
                block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
                block4.center = (
                    center[0] - blockdimension,
                    center[1] + blockdimension / 2,
                )
                pygame.draw.rect(screen, purple, block1)
                pygame.draw.rect(screen, purple, block2)
                pygame.draw.rect(screen, purple, block3)
                pygame.draw.rect(screen, purple, block4)


def displayhold(boardrect: pygame.Rect, player):
    panel = pygame.Rect(
        boardrect.left - boardrect.width / 3,
        boardrect.top,
        boardrect.width / 3,
        boardrect.height / 4,
    )
    pygame.draw.rect(screen, white, panel)
    center = (
        panel.left + panel.width / 2,
        panel.top + panel.height / 2,
    )
    match player.holdpiece:
        case 1:
            block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block1.center = (
                center[0] - blockdimension / 2,
                center[1] - blockdimension / 2,
            )
            block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block2.center = (
                center[0] + blockdimension / 2,
                center[1] - blockdimension / 2,
            )
            block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block3.center = (
                center[0] - blockdimension / 2,
                center[1] + blockdimension / 2,
            )
            block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block4.center = (
                center[0] + blockdimension / 2,
                center[1] + blockdimension / 2,
            )
            pygame.draw.rect(screen, yellow, block1)
            pygame.draw.rect(screen, yellow, block2)
            pygame.draw.rect(screen, yellow, block3)
            pygame.draw.rect(screen, yellow, block4)
        case 2:
            block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block1.center = (center[0] - blockdimension / 2, center[1])
            block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block2.center = (center[0] + blockdimension / 2, center[1])
            block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block3.center = (center[0] - blockdimension * 1.5, center[1])
            block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block4.center = (center[0] + blockdimension * 1.5, center[1])
            pygame.draw.rect(screen, cyan, block1)
            pygame.draw.rect(screen, cyan, block2)
            pygame.draw.rect(screen, cyan, block3)
            pygame.draw.rect(screen, cyan, block4)
        case 3:
            block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block1.center = (center[0], center[1] - blockdimension / 2)
            block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block2.center = (
                center[0] + blockdimension,
                center[1] - blockdimension / 2,
            )
            block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block3.center = (center[0], center[1] + blockdimension / 2)
            block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block4.center = (
                center[0] - blockdimension,
                center[1] + blockdimension / 2,
            )
            pygame.draw.rect(screen, green, block1)
            pygame.draw.rect(screen, green, block2)
            pygame.draw.rect(screen, green, block3)
            pygame.draw.rect(screen, green, block4)
        case 4:
            block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block1.center = (center[0], center[1] - blockdimension / 2)
            block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block2.center = (
                center[0] - blockdimension,
                center[1] - blockdimension / 2,
            )
            block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block3.center = (center[0], center[1] + blockdimension / 2)
            block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block4.center = (
                center[0] + blockdimension,
                center[1] + blockdimension / 2,
            )
            pygame.draw.rect(screen, red, block1)
            pygame.draw.rect(screen, red, block2)
            pygame.draw.rect(screen, red, block3)
            pygame.draw.rect(screen, red, block4)
        case 5:
            block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block1.center = (
                center[0] + blockdimension,
                center[1] - blockdimension / 2,
            )
            block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block2.center = (
                center[0] + blockdimension,
                center[1] + blockdimension / 2,
            )
            block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block3.center = (center[0], center[1] + blockdimension / 2)
            block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block4.center = (
                center[0] - blockdimension,
                center[1] + blockdimension / 2,
            )
            pygame.draw.rect(screen, orange, block1)
            pygame.draw.rect(screen, orange, block2)
            pygame.draw.rect(screen, orange, block3)
            pygame.draw.rect(screen, orange, block4)
        case 6:
            block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block1.center = (
                center[0] - blockdimension,
                center[1] - blockdimension / 2,
            )
            block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block2.center = (
                center[0] + blockdimension,
                center[1] + blockdimension / 2,
            )
            block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block3.center = (center[0], center[1] + blockdimension / 2)
            block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block4.center = (
                center[0] - blockdimension,
                center[1] + blockdimension / 2,
            )
            pygame.draw.rect(screen, blue, block1)
            pygame.draw.rect(screen, blue, block2)
            pygame.draw.rect(screen, blue, block3)
            pygame.draw.rect(screen, blue, block4)
        case 7:
            block1 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block1.center = (center[0], center[1] - blockdimension / 2)
            block2 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block2.center = (
                center[0] + blockdimension,
                center[1] + blockdimension / 2,
            )
            block3 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block3.center = (center[0], center[1] + blockdimension / 2)
            block4 = pygame.Rect((0, 0, blockdimension, blockdimension))
            block4.center = (
                center[0] - blockdimension,
                center[1] + blockdimension / 2,
            )
            pygame.draw.rect(screen, purple, block1)
            pygame.draw.rect(screen, purple, block2)
            pygame.draw.rect(screen, purple, block3)
            pygame.draw.rect(screen, purple, block4)


def displaystat(boardrect: pygame.Rect, player):
    displaylabel(
        player.vsscore,
        "VS ",
        boardrect=boardrect,
        topleft=(
            boardrect.width,
            boardrect.height * 15 / 16,
        ),
        size=playerFont,
    )
    displaylabel(
        player.totalpiece,
        "piece",
        boardrect=boardrect,
        topleft=(-100, boardrect.height * 15 / 16),
        size=playerFont,
    )
    displaylabel(
        player.pps,
        "pps",
        boardrect=boardrect,
        topleft=(-100, boardrect.height * 14 / 16),
        size=playerFont,
    )


def displaylabel(
    content,
    title,
    topleft=None,
    center=None,
    color=white,
    boardrect=None,
    size=largeFont,
    background=False,
):
    label = size.render("{}{}".format(title, content), True, color, None)
    labelRect = label.get_rect()
    if boardrect == None:
        if topleft != None:
            labelRect.topleft = topleft
        else:
            labelRect.center = center
    else:
        if topleft != None:
            labelRect.topleft = (
                boardrect.topleft[0] + topleft[0],
                boardrect.topleft[1] + topleft[1],
            )
        else:
            labelRect.center = center
    if background:
        pygame.draw.rect(screen, black, labelRect)

    screen.blit(label, labelRect)


# timer
dt = 0
clock = pygame.time.Clock()
gametime = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                humanplayer.harddrop()
            if event.key == pygame.K_a:
                humanplayer.left()
            if event.key == pygame.K_d:
                humanplayer.right()
            if event.key == pygame.K_j:
                humanplayer.anticlockwiserotate()
            if event.key == pygame.K_k:
                humanplayer.clockwiserotate()
            if event.key == pygame.K_i:
                humanplayer.spin180()
            if event.key == pygame.K_s:
                humanplayer.softdrop()
            if event.key == pygame.K_l:
                humanplayer.hold()
            if event.key == pygame.K_r:
                tetrisgame.reset()
            if event.key == pygame.K_t:
                if display == True:
                    display = False
                    fps = 240
                else:
                    display = True
                    fps = 10
    screen.fill(background)
    dt = clock.tick(fps)
    gametime += dt
    # region framework display
    displaylabel(
        "Tetris",
        "",
        center=((screen.get_width() / 2), (screen.get_height() / 20)),
        size=moveFont,
    )
    displaylabel(round(1000 / dt, -1), "fps", topleft=(0, 0), size=mediumFont)

    # endregion
    if not (aiplayer or humanplay):

        # region play button
        humanbutton = pygame.Rect(
            (screen.get_width() / 15),
            (screen.get_height() / 10),
            screenwidth * 6 / 15,
            screen.get_height() / 16,
        )
        playhuman = mediumFont.render("Play as human", True, black)
        playhumanRect = playhuman.get_rect()
        playhumanRect.center = humanbutton.center
        pygame.draw.rect(screen, white, humanbutton)
        screen.blit(playhuman, playhumanRect)
        aibutton = pygame.Rect(
            (screen.get_width() * 8 / 15),
            (screen.get_height() / 10),
            screenwidth * 6 / 15,
            screen.get_height() / 16,
        )
        playai = mediumFont.render("Play as ai", True, black)
        playaiRect = playai.get_rect()
        playaiRect.center = aibutton.center
        pygame.draw.rect(screen, white, aibutton)
        screen.blit(playai, playaiRect)
        # endregion
        # clickhandel
        click, _, _ = pygame.mouse.get_pressed()
        if click:
            mouse = pygame.mouse.get_pos()
            if humanbutton.collidepoint(mouse):
                humanplay = True
                if tetrisgame == None:
                    tetrisgame = tt.Tetrisgame(width, height, ppf=ppf, gravity=gravity)
                    for player in range(POPULATION):
                        if player == 0:
                            humanplayer = tetrisgame.addplayer(True)
                        else:
                            tetrisgame.addplayer()

                starttime = pygame.time.get_ticks()
                currenttime = pygame.time.get_ticks()
    elif humanplay:
        aiplayer = False
        if tetrisgame.playerleft <= 0:
            tetrisgame.gamestep()
            continue
        row = round(math.sqrt(tetrisgame.playerleft))
        colume = round(math.sqrt(tetrisgame.playerleft) + 0.49)
        displayscale = 1 / round(math.sqrt(tetrisgame.playerleft))
        playerFont = pygame.font.Font("OpenSans-Regular.ttf", round(40 * displayscale))
        blockdimension = round(30 * displayscale)
        outerborderwidth = round(5 * displayscale)
        innerborderwidth = round(1 * displayscale)
        if display:
            for i, player in enumerate(tetrisgame.alive):
                boardRect = pygame.Rect(
                    0,
                    0,
                    (blockdimension + innerborderwidth) * tetrisgame.width
                    - innerborderwidth
                    + 2 * outerborderwidth,
                    (blockdimension + innerborderwidth) * (tetrisgame.height)
                    - innerborderwidth
                    + outerborderwidth,
                )
                boardRect.center = (
                    screenwidth * (i % colume + 0.5) / colume,
                    screenheight * (round(i / colume - 0.01) % row + 0.5) / row,
                )
                pygame.draw.rect(screen, white, boardRect)

                displayblock(boardRect, player)
                if len(player.sequel) > 4:
                    displaybag(boardRect, player)
                displayhold(boardRect, player)
                displaystat(boardRect, player)
        tetrisgame.gamestep()
        displaylabel(
            round(tetrisgame.frame / 60, 1),
            "Time",
            topleft=(0, 40),
            size=mediumFont,
            background=True,
        )
        displaylabel(
            tetrisgame.playerleft,
            "Player left:",
            topleft=(0, 80),
            size=mediumFont,
            background=True,
        )
        displaylabel(
            tetrisgame.generation,
            "generation:",
            topleft=(0, 120),
            size=mediumFont,
            background=True,
        )
    # if humanplay:
    pygame.display.update()
