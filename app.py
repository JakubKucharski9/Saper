import random
import sys
import numpy as np
import pygame
from pygame.locals import *

FPS = 30

NUMROWS     = 10
NUMCOLS     = 10
NUMBOMBS    = 10

CELLSIZE        = 40
WINDOWWIDTH     = 600
WINDOWHEIGHT    = 600
FIELDWIDTH      = NUMCOLS * CELLSIZE
FIELDHEIGHT     = NUMROWS * CELLSIZE
XMARGIN         = int((WINDOWWIDTH-FIELDWIDTH)//2)
YMARGIN         = int((WINDOWHEIGHT-FIELDHEIGHT)//2)

#            R    G    B
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)

GAMENAME = "SAPER GAME"

EASY    = 1
MEDIUM  = 2
HARD    = 3

BOMBVALUE = -1


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    font = pygame.font.SysFont(None, 24)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(GAMENAME)

    board = drawBoard(NUMCOLS, NUMROWS)
    clickedCells = [[0] * NUMCOLS for _ in range(NUMROWS)]

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mousex, mousey = event.pos
                row, col = getCellAtPixel(mousex, mousey)
                if row is not None and col is not None:
                    revealCell(row, col, clickedCells, board)

        DISPLAYSURF.fill(BLACK)
        drawCells(clickedCells, board, font)
        drawGrid()
        pygame.display.flip()
        FPSCLOCK.tick(FPS)


def drawBoard(rows, columns):
    flatten = [0] * (rows * columns)
    bombsIdxs = random.sample(range(rows * columns), NUMBOMBS)
    for index in bombsIdxs:
        flatten[index] = BOMBVALUE
    board = [flatten[i*columns:(i+1)*columns] for i in range(rows)]

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
        x = mousex//CELLSIZE
        y = mousey//CELLSIZE
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
    if XMARGIN <= mx < XMARGIN+FIELDWIDTH and YMARGIN <= my < YMARGIN+FIELDHEIGHT:
        col = (mx - XMARGIN) // CELLSIZE
        row = (my - YMARGIN) // CELLSIZE
        return row, col
    return None, None


def revealCell(row, col, clickedBoard, board):
    if clickedBoard[row][col] == 1:
        return
    clickedBoard[row][col] = 1
    if board[row][col] == 0:
        flood_fill(row, col, clickedBoard, board)


def drawCells(clickedBoard, board, font):
    for r in range(NUMROWS):
        for c in range(NUMCOLS):
            x, y = XMARGIN + c * CELLSIZE, YMARGIN + r * CELLSIZE
            if clickedBoard[r][c] == 0:
                pygame.draw.rect(DISPLAYSURF, GREEN, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
            elif clickedBoard[r][c] == 1:
                val = board[r][c]
                pygame.draw.rect(DISPLAYSURF, BLUE, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
                if val > 0:
                    text = font.render(str(val), 1, WHITE)
                    tx = x + CELLSIZE//2 - text.get_width()//2
                    ty = y + CELLSIZE//2 - text.get_height()//2
                    DISPLAYSURF.blit(text, (tx, ty))
                elif val == BOMBVALUE:
                    pygame.draw.rect(DISPLAYSURF, RED, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))

if __name__ == '__main__':
    main()
