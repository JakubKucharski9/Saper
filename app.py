import random
import sys
import pygame
from pygame.locals import *

FPS = 30

NUMROWS = 10
NUMCOLS = 10

CELLSIZE = 40

FIELDWIDTH = NUMCOLS * CELLSIZE
FIELDHEIGHT = NUMROWS * CELLSIZE
WINDOWWIDTH = FIELDWIDTH + 200
WINDOWHEIGHT = FIELDHEIGHT + 200
XMARGIN = int((WINDOWWIDTH - FIELDWIDTH) // 2)
YMARGIN = int((WINDOWHEIGHT - FIELDHEIGHT) // 2)

BUTTONWIDTH = 160
BUTTONHEIGHT = 40

#            R    G    B
BLACK   = (    0,   0,  0)
WHITE   = (  255, 255,  255)
RED     = (  255,   0,  0)
GREEN   = (    0, 255,  0)
BLUE    = (    0,   0,  255)
PINK    = (  255, 192,  203)
YELLOW = ( 255, 255, 0)

GAMENAME = "SAPER GAME"

EASY = 5
MEDIUM = 15
HARD = 25

BOMBVALUE = -1


def game():
    global FPSCLOCK, DISPLAYSURF, FONT
    pygame.init()
    FONT = pygame.font.SysFont(None, 24)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(GAMENAME)

    resetGame = False
    hasLost = False
    game = False
    difficulty = 0
    while True:

        if not game:
            DISPLAYSURF.fill(BLACK)
            easyRect, midRect, hardRect = drawInputBox()

            while not game:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if easyRect.collidepoint(event.pos):
                            difficulty = EASY
                        elif midRect.collidepoint(event.pos):
                            difficulty = MEDIUM
                        elif hardRect.collidepoint(event.pos):
                            difficulty = HARD
                if difficulty != 0:
                    game = True
                pygame.display.flip()
                FPSCLOCK.tick(FPS)


        elif game:
            DISPLAYSURF.fill(BLACK)
            resetButtonWidth, resetButtonHeight, resetButtonX, resetButtonY = drawButtons()
            clickedCells = [[0] * NUMCOLS for _ in range(NUMROWS)]
            board = drawBoard(NUMCOLS, NUMROWS, difficulty)
            drawGrid()
            while game:

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mousex, mousey = event.pos
                            if pygame.Rect(resetButtonX-(resetButtonWidth/2), resetButtonY-(resetButtonHeight/2), resetButtonWidth, resetButtonHeight).collidepoint(mousex, mousey):
                                resetGame = True
                            else:
                                row, col = getCellAtPixel(mousex, mousey)
                                if row is not None and col is not None:
                                    revealCell(row, col, clickedCells, board)
                        elif event.button == 3:
                            mousex, mousey = event.pos
                            row, col = getCellAtPixel(mousex, mousey)
                            if row is not None and col is not None:
                                if clickedCells[row][col] == 0:
                                    clickedCells[row][col] = 2
                                elif clickedCells[row][col] == 2:
                                    clickedCells[row][col] = 0

                if hasLost:
                    hasLostScreen()

                else:
                    hasLost = drawCells(clickedCells, board)
                    hasWon(board, clickedCells, difficulty)
                    showFlagCounter(clickedCells, difficulty)

                if resetGame:
                    resetGame = False
                    hasLost = False
                    game = False
                    difficulty = 0

                pygame.display.flip()
                FPSCLOCK.tick(FPS)


def drawInputBox():
    DISPLAYSURF.fill(BLACK)

    easyRect = pygame.Rect((WINDOWWIDTH//2)-(BUTTONWIDTH//2), (WINDOWHEIGHT//4)-(BUTTONHEIGHT//2), BUTTONWIDTH, BUTTONHEIGHT)
    pygame.draw.rect(DISPLAYSURF, GREEN, easyRect)

    easyText = FONT.render('EASY', 1, BLACK)
    easyRectText = easyText.get_rect()
    easyRectText.center = (WINDOWWIDTH // 2, WINDOWHEIGHT//4)
    DISPLAYSURF.blit(easyText, easyRectText)

    midRect = pygame.Rect((WINDOWWIDTH//2)-(BUTTONWIDTH//2), (2*WINDOWHEIGHT//4)-(BUTTONHEIGHT//2), BUTTONWIDTH, BUTTONHEIGHT)
    pygame.draw.rect(DISPLAYSURF, YELLOW, midRect)

    midText = FONT.render('MEDIUM', 1, BLACK)
    midRectText = midText.get_rect()
    midRectText.center = (WINDOWWIDTH // 2, 2 * WINDOWHEIGHT // 4)
    DISPLAYSURF.blit(midText, midRectText)

    hardRect = pygame.Rect((WINDOWWIDTH // 2) - (BUTTONWIDTH // 2), (3 * WINDOWHEIGHT // 4) - (BUTTONHEIGHT // 2), BUTTONWIDTH, BUTTONHEIGHT)
    pygame.draw.rect(DISPLAYSURF, RED, hardRect)

    hardText = FONT.render('HARD', 1, BLACK)
    hardRectText = hardText.get_rect()
    hardRectText.center = (WINDOWWIDTH // 2, 3 * WINDOWHEIGHT // 4)
    DISPLAYSURF.blit(hardText, hardRectText)

    return easyRect, midRect, hardRect


def drawBoard(rows, columns, difficulty):
    flatten = [0] * (rows * columns)
    bombsIdxs = random.sample(range(rows * columns), difficulty)
    for index in bombsIdxs:
        flatten[index] = BOMBVALUE
    board = [flatten[i * columns:(i + 1) * columns] for i in range(rows)]

    for row in range(rows):
        for column in range(columns):
            if board[row][column] == BOMBVALUE:
                continue
            bombCount = 0
            for drow in (-1, 0, 1):
                for dcol in (-1, 0, 1):
                    if drow == 0 and dcol == 0:
                        continue

                    neighbourRow = row + drow
                    neighbourCol = column + dcol

                    if not (0 <= neighbourRow < rows and 0 <= neighbourCol < columns):
                        continue

                    if board[neighbourRow][neighbourCol] == BOMBVALUE:
                        bombCount += 1

            board[row][column] = bombCount
    return board


def getCellClicked(mousex, mousey):
    if mousex <= FIELDWIDTH and mousey <= FIELDHEIGHT:
        x = mousex // CELLSIZE
        y = mousey // CELLSIZE
        return x, y

    return None


def drawGrid():
    for c in range(NUMCOLS):
        for r in range(NUMROWS):
            x, y = XMARGIN + c * CELLSIZE, YMARGIN + r * CELLSIZE
            pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE), 1)


def flood_fill(row, col, clickedBoard, board):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nr, nc = row + dr, col + dc
            if 0 <= nr < NUMROWS and 0 <= nc < NUMCOLS and clickedBoard[nr][nc] == 0:
                clickedBoard[nr][nc] = 1
                if board[nr][nc] == 0:
                    flood_fill(nr, nc, clickedBoard, board)


def getCellAtPixel(mx, my):
    if XMARGIN <= mx < XMARGIN + FIELDWIDTH and YMARGIN <= my < YMARGIN + FIELDHEIGHT:
        col = (mx - XMARGIN) // CELLSIZE
        row = (my - YMARGIN) // CELLSIZE
        return row, col
    return None, None


def revealCell(row, col, clickedBoard, board):
    if clickedBoard[row][col] == 1 or clickedBoard[row][col] == 2:
        return
    clickedBoard[row][col] = 1
    if board[row][col] == 0:
        flood_fill(row, col, clickedBoard, board)


def drawCells(clickedBoard, board):
    hasLost = False
    for r in range(NUMROWS):
        for c in range(NUMCOLS):
            x, y = XMARGIN + c * CELLSIZE, YMARGIN + r * CELLSIZE
            if clickedBoard[r][c] == 0:
                pygame.draw.rect(DISPLAYSURF, GREEN, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
            elif clickedBoard[r][c] == 1:
                val = board[r][c]
                if val == 0:
                    pygame.draw.rect(DISPLAYSURF, BLUE, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
                elif val > 0:
                    pygame.draw.rect(DISPLAYSURF, BLUE, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
                    text = FONT.render(str(val), 1, WHITE)
                    tx = x + CELLSIZE // 2 - text.get_width() // 2
                    ty = y + CELLSIZE // 2 - text.get_height() // 2
                    DISPLAYSURF.blit(text, (tx, ty))
                elif val == BOMBVALUE:
                    hasLost = True

            elif clickedBoard[r][c] == 2:
                pygame.draw.rect(DISPLAYSURF, PINK, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
                flagImg = pygame.image.load("finish-flag.png")
                flagX = x + (CELLSIZE - flagImg.get_rect().width) // 2
                flagY = y + (CELLSIZE - flagImg.get_rect().height) // 2
                DISPLAYSURF.blit(flagImg, (flagX, flagY))
    return hasLost


def hasWon(board, clickedBoard, difficulty):
    flagMatching = 0
    for rowBoard, rowClicked in zip(board, clickedBoard):
        for valBoard, valClicked in zip(rowBoard, rowClicked):
            if valBoard == -1 and valClicked == 2:
                flagMatching += 1

    flagPlaced = 0
    for rowClicked in clickedBoard:
        for valClicked in rowClicked:
            if valClicked == 2:
                flagPlaced += 1

    if flagMatching == difficulty and flagPlaced == difficulty and not any(0 in row for row in clickedBoard):
        DISPLAYSURF.fill(BLACK)
        drawButtons()
        gameWinText = FONT.render('GAME WON!!!', 1, WHITE)
        gameWinRect = gameWinText.get_rect()
        gameWinRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
        DISPLAYSURF.blit(gameWinText, gameWinRect)
        pygame.display.flip()


def hasLostScreen():
    DISPLAYSURF.fill(BLACK)
    drawButtons()
    gameOverText = FONT.render('GAME OVER', 1, WHITE)
    gameOverRect = gameOverText.get_rect()
    gameOverRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(gameOverText, gameOverRect)
    pygame.display.flip()


def drawButtons():
    resetText = FONT.render('RESET', 1, WHITE)
    resetRect = resetText.get_rect()
    resetRect.center = (WINDOWWIDTH // 2, FIELDHEIGHT + (WINDOWHEIGHT - FIELDHEIGHT)//3*2)
    DISPLAYSURF.blit(resetText, resetRect)
    return resetRect.width, resetRect.height, WINDOWWIDTH / 2, FIELDHEIGHT + (WINDOWHEIGHT - FIELDHEIGHT)/3*2


def showFlagCounter(clickedBoard, difficulty):
    placedFlags = sum(row.count(2) for row in clickedBoard)
    placedFlagsText = FONT.render(f'FLAG PLACED: {placedFlags}/{difficulty}', 1, WHITE)
    placedFlagsRect = placedFlagsText.get_rect()
    placedFlagsRect.center = (WINDOWWIDTH // 2, (WINDOWHEIGHT - FIELDHEIGHT) // 3)
    DISPLAYSURF.fill(BLACK, placedFlagsRect)
    DISPLAYSURF.blit(placedFlagsText, placedFlagsRect)


if __name__ == '__main__':
    game()
