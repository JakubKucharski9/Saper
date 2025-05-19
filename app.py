import random
import sys
import pygame
from pygame.locals import *
import time

# Game settings
FPS = 30  # Frames per second for game loop
GAMENAME = "SAPER GAME" # Name of the game

# Board sizes for different difficulties
EASY_SIZE = 7    # 7x7 grid for easy mode
MEDIUM_SIZE = 10 # 10x10 grid for medium mode
HARD_SIZE = 15   # 15x15 grid for hard mode

# Game difficulty settings - number of bombs for each level
EASY = 7    # 7 bombs for easy mode
MEDIUM = 20 # 20 bombs for medium mode
HARD = 50   # 50 bombs for hard mode

# Visual settings
CELLSIZE = 30  # Size of each cell in pixels
WINDOWWIDTH = 800   # Fixed window width
WINDOWHEIGHT = 650  # Fixed window height
BUTTONWIDTH = 160 # Width of the buttons
BUTTONHEIGHT = 40 # Height of the buttons

# Game constants
BOMBVALUE = -1  # Value representing a bomb in the game board

# Best times for each difficulty (in seconds)
# Initialize with infinity to ensure first completion becomes the best time
best_times = {
    EASY: float('inf'),
    MEDIUM: float('inf'),
    HARD: float('inf')
}

# Colors R G B
BLACK   = (    0,   0,  0)
WHITE   = (  255, 255,  255)
RED     = (  255,   0,  0)
GREEN   = (    0, 255,  0)
BLUE    = (    0,   0,  255)
PINK    = (  255, 192,  203)
YELLOW  = ( 255, 255, 0)
TEAL    = ( 0, 128, 128)
CYAN    = ( 220, 255, 255)
MAROON  = ( 128, 0, 0)


def format_time(seconds):
    """Convert seconds to MM:SS format for display"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def game():
    """Main game function that handles the game loop and state"""
    global FPSCLOCK, DISPLAYSURF, FONT, NUMROWS, NUMCOLS, FIELDWIDTH, FIELDHEIGHT, XMARGIN, YMARGIN
    pygame.init()
    FONT = pygame.font.SysFont(None, 24)

    # Initialize display and clock
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption(GAMENAME)
    pygame.display.set_icon(pygame.image.load('cactus.png'))

    # Game state variables
    resetGame = False
    hasLost = False
    game = False
    difficulty = 0
    firstClick = True
    board = None
    start_time = None
    current_time = 0

    while True:
        # Main menu state
        if not game:
            DISPLAYSURF.fill(BLACK)
            easyRect, midRect, hardRect = drawInputBox()

            while not game:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        # Handle difficulty selection
                        if easyRect.collidepoint(event.pos):
                            difficulty = EASY
                            NUMROWS = NUMCOLS = EASY_SIZE
                        elif midRect.collidepoint(event.pos):
                            difficulty = MEDIUM
                            NUMROWS = NUMCOLS = MEDIUM_SIZE
                        elif hardRect.collidepoint(event.pos):
                            difficulty = HARD
                            NUMROWS = NUMCOLS = HARD_SIZE
                if difficulty != 0:
                    # Initialize game board dimensions
                    FIELDWIDTH = NUMCOLS * CELLSIZE
                    FIELDHEIGHT = NUMROWS * CELLSIZE
                    XMARGIN = int((WINDOWWIDTH - FIELDWIDTH) // 2)
                    YMARGIN = int((WINDOWHEIGHT - FIELDHEIGHT) // 2)
                    game = True
                    firstClick = True
                    start_time = None
                    current_time = 0
                pygame.display.flip()
                FPSCLOCK.tick(FPS)

        # Game play state
        elif game:
            DISPLAYSURF.fill(BLACK)
            resetButtonWidth, resetButtonHeight, resetButtonX, resetButtonY = drawButtons()
            clickedCells = [[0] * NUMCOLS for _ in range(NUMROWS)]
            if board is None:
                board = drawBoard(NUMCOLS, NUMROWS, difficulty)
            drawGrid()
            while game:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            mousex, mousey = event.pos
                            # Check if reset button was clicked
                            if pygame.Rect(resetButtonX-(resetButtonWidth/2), resetButtonY-(resetButtonHeight/2), resetButtonWidth, resetButtonHeight).collidepoint(mousex, mousey):
                                resetGame = True
                            else:
                                # Handle cell click
                                row, col = getCellAtPixel(mousex, mousey)
                                if row is not None and col is not None:
                                    if firstClick:
                                        # Ensure first click is safe
                                        board = drawBoard(NUMCOLS, NUMROWS, difficulty, row, col)
                                        firstClick = False
                                        start_time = time.time()
                                    revealCell(row, col, clickedCells, board)
                        elif event.button == 3:  # Right click - place/remove flag
                            mousex, mousey = event.pos
                            row, col = getCellAtPixel(mousex, mousey)
                            if row is not None and col is not None:
                                if clickedCells[row][col] == 0:
                                    clickedCells[row][col] = 2  # Place flag
                                elif clickedCells[row][col] == 2:
                                    clickedCells[row][col] = 0  # Remove flag

                # Update game state
                if hasLost:
                    hasLostScreen()
                else:
                    hasLost = drawCells(clickedCells, board)
                    if not hasLost:
                        if start_time is not None:
                            current_time = time.time() - start_time
                        showTimer(current_time, best_times[difficulty])
                    hasWon(board, clickedCells, difficulty, current_time)
                    showFlagCounter(clickedCells, difficulty)

                # Handle game reset
                if resetGame:
                    resetGame = False
                    hasLost = False
                    game = False
                    difficulty = 0
                    board = None
                    firstClick = True
                    start_time = None
                    current_time = 0

                pygame.display.flip()
                FPSCLOCK.tick(FPS)

def drawInputBox():
    """Draw the difficulty selection menu"""
    DISPLAYSURF.fill(BLACK)

    # Draw Easy button
    easyRect = pygame.Rect((WINDOWWIDTH//2)-(BUTTONWIDTH//2), (WINDOWHEIGHT//4)-(BUTTONHEIGHT//2), BUTTONWIDTH, BUTTONHEIGHT)
    pygame.draw.rect(DISPLAYSURF, GREEN, easyRect)
    easyText = FONT.render('EASY', 1, BLACK)
    easyRectText = easyText.get_rect()
    easyRectText.center = (WINDOWWIDTH // 2, WINDOWHEIGHT//4)
    DISPLAYSURF.blit(easyText, easyRectText)

    # Draw Medium button
    midRect = pygame.Rect((WINDOWWIDTH//2)-(BUTTONWIDTH//2), (2*WINDOWHEIGHT//4)-(BUTTONHEIGHT//2), BUTTONWIDTH, BUTTONHEIGHT)
    pygame.draw.rect(DISPLAYSURF, YELLOW, midRect)
    midText = FONT.render('MEDIUM', 1, BLACK)
    midRectText = midText.get_rect()
    midRectText.center = (WINDOWWIDTH // 2, 2 * WINDOWHEIGHT // 4)
    DISPLAYSURF.blit(midText, midRectText)

    # Draw Hard button
    hardRect = pygame.Rect((WINDOWWIDTH // 2) - (BUTTONWIDTH // 2), (3 * WINDOWHEIGHT // 4) - (BUTTONHEIGHT // 2), BUTTONWIDTH, BUTTONHEIGHT)
    pygame.draw.rect(DISPLAYSURF, RED, hardRect)
    hardText = FONT.render('HARD', 1, BLACK)
    hardRectText = hardText.get_rect()
    hardRectText.center = (WINDOWWIDTH // 2, 3 * WINDOWHEIGHT // 4)
    DISPLAYSURF.blit(hardText, hardRectText)

    return easyRect, midRect, hardRect

def drawBoard(rows, columns, difficulty, firstClickRow=None, firstClickCol=None):
    """Create and initialize the game board with bombs and numbers"""
    flatten = [0] * (rows * columns)
    bombsIdxs = random.sample(range(rows * columns), difficulty)
    
    # Ensure first click is safe
    if firstClickRow is not None and firstClickCol is not None:
        firstClickIdx = firstClickRow * columns + firstClickCol
        if firstClickIdx in bombsIdxs:
            bombsIdxs.remove(firstClickIdx)
            safePositions = [i for i in range(rows * columns) if i not in bombsIdxs]
            if safePositions:
                newBombPos = random.choice(safePositions)
                bombsIdxs.append(newBombPos)
    
    # Place bombs
    for index in bombsIdxs:
        flatten[index] = BOMBVALUE
    board = [flatten[i * columns:(i + 1) * columns] for i in range(rows)]

    # Calculate numbers for each cell
    for row in range(rows):
        for column in range(columns):
            if board[row][column] == BOMBVALUE:
                continue
            bombCount = 0
            # Check all 8 surrounding cells
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

def getCellAtPixel(mx, my):
    """Convert pixel coordinates to cell coordinates"""
    if XMARGIN <= mx < XMARGIN + FIELDWIDTH and YMARGIN <= my < YMARGIN + FIELDHEIGHT:
        col = (mx - XMARGIN) // CELLSIZE
        row = (my - YMARGIN) // CELLSIZE
        return row, col
    return None, None

def drawGrid():
    """Draw the grid lines for the game board"""
    for c in range(NUMCOLS):
        for r in range(NUMROWS):
            x, y = XMARGIN + c * CELLSIZE, YMARGIN + r * CELLSIZE
            pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE), 1)

def flood_fill(row, col, clickedBoard, board):
    """Recursively reveal empty cells and their neighbors"""
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nr, nc = row + dr, col + dc
            if 0 <= nr < NUMROWS and 0 <= nc < NUMCOLS and clickedBoard[nr][nc] == 0:
                clickedBoard[nr][nc] = 1
                if board[nr][nc] == 0:
                    flood_fill(nr, nc, clickedBoard, board)

def revealCell(row, col, clickedBoard, board):
    """Handle cell revelation when clicked"""
    if clickedBoard[row][col] == 1 or clickedBoard[row][col] == 2:
        return
    clickedBoard[row][col] = 1
    if board[row][col] == 0:
        flood_fill(row, col, clickedBoard, board)

def drawCells(clickedBoard, board):
    """Draw all cells based on their state"""
    hasLost = False
    for r in range(NUMROWS):
        for c in range(NUMCOLS):
            x, y = XMARGIN + c * CELLSIZE, YMARGIN + r * CELLSIZE
            if clickedBoard[r][c] == 0:  # Unrevealed cell
                pygame.draw.rect(DISPLAYSURF, GREEN, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
            elif clickedBoard[r][c] == 1:  # Revealed cell
                val = board[r][c]
                if val == 0:  # Empty cell
                    pygame.draw.rect(DISPLAYSURF, BLUE, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
                elif val > 0:  # Number cell
                    pygame.draw.rect(DISPLAYSURF, BLUE, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
                    # Choose color based on number
                    match val:
                        case 1: color = CYAN
                        case 2: color = RED
                        case 3: color = YELLOW
                        case 4: color = GREEN
                        case 5: color = PINK
                        case 6: color = TEAL
                        case 7: color = TEAL
                        case 8: color = WHITE
                        case _: color = None

                    text = FONT.render(str(val), 1, color)
                    tx = x + CELLSIZE // 2 - text.get_width() // 2
                    ty = y + CELLSIZE // 2 - text.get_height() // 2
                    DISPLAYSURF.blit(text, (tx, ty))
                elif val == BOMBVALUE:  # Bomb cell
                    hasLost = True

            elif clickedBoard[r][c] == 2:  # Flagged cell
                pygame.draw.rect(DISPLAYSURF, PINK, (x + 1, y + 1, CELLSIZE - 2, CELLSIZE - 2))
                flagImg = pygame.image.load("finish-flag.png")
                flagImg = pygame.transform.scale(flagImg, (CELLSIZE - 4, CELLSIZE - 4))
                flagX = x + (CELLSIZE - flagImg.get_rect().width) // 2
                flagY = y + (CELLSIZE - flagImg.get_rect().height) // 2
                DISPLAYSURF.blit(flagImg, (flagX, flagY))
    return hasLost

def hasWon(board, clickedBoard, difficulty, current_time):
    """Check if the player has won the game"""
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

    # Check win conditions
    if flagMatching == difficulty and flagPlaced == difficulty and not any(0 in row for row in clickedBoard):
        global best_times
        # Update best time if current time is better
        if current_time < best_times[difficulty]:
            best_times[difficulty] = current_time
        DISPLAYSURF.fill(BLACK)
        drawButtons()
        gameWinText = FONT.render('GAME WON!!!', 1, WHITE)
        gameWinRect = gameWinText.get_rect()
        gameWinRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
        DISPLAYSURF.blit(gameWinText, gameWinRect)
        pygame.display.flip()

def hasLostScreen():
    """Display game over screen"""
    DISPLAYSURF.fill(BLACK)
    drawButtons()
    gameOverText = FONT.render('GAME OVER', 1, WHITE)
    gameOverRect = gameOverText.get_rect()
    gameOverRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(gameOverText, gameOverRect)
    pygame.display.flip()

def drawButtons():
    """Draw the reset button"""
    resetText = FONT.render('RESET', 1, WHITE)
    resetRect = resetText.get_rect()
    resetRect.center = (WINDOWWIDTH // 2, FIELDHEIGHT + (WINDOWHEIGHT - FIELDHEIGHT)//3*2)
    DISPLAYSURF.blit(resetText, resetRect)
    return resetRect.width, resetRect.height, WINDOWWIDTH / 2, FIELDHEIGHT + (WINDOWHEIGHT - FIELDHEIGHT)/3*2

def showFlagCounter(clickedBoard, difficulty):
    """Display the number of flags placed"""
    placedFlags = sum(row.count(2) for row in clickedBoard)
    placedFlagsText = FONT.render(f'FLAG PLACED: {placedFlags}/{difficulty}', 1, WHITE)
    placedFlagsRect = placedFlagsText.get_rect()
    placedFlagsRect.center = (WINDOWWIDTH // 2, (WINDOWHEIGHT - FIELDHEIGHT) // 3)
    DISPLAYSURF.fill(BLACK, placedFlagsRect)
    DISPLAYSURF.blit(placedFlagsText, placedFlagsRect)

def showTimer(current_time, best_time):
    """Display current time and best time"""
    # Display current time
    time_text = FONT.render(f'Time: {format_time(current_time)}', 1, WHITE)
    time_rect = time_text.get_rect()
    time_rect.center = (WINDOWWIDTH // 2, (WINDOWHEIGHT - FIELDHEIGHT) // 3 - 30)
    DISPLAYSURF.fill(BLACK, time_rect)
    DISPLAYSURF.blit(time_text, time_rect)

    # Display best time if it exists
    if best_time != float('inf'):
        best_time_text = FONT.render(f'Best: {format_time(best_time)}', 1, WHITE)
        best_time_rect = best_time_text.get_rect()
        best_time_rect.center = (WINDOWWIDTH // 2, (WINDOWHEIGHT - FIELDHEIGHT) // 3 - 50)
        DISPLAYSURF.fill(BLACK, best_time_rect)
        DISPLAYSURF.blit(best_time_text, best_time_rect)

if __name__ == '__main__':
    game()
