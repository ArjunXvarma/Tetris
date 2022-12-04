import pygame
import random
 
# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARS
screenWidth = 800
screenHeight = 700
playWidth = 300  # meaning 300 // 10 = 30 width per block
playHeight = 600  # meaning 600 // 20 = 20 height per block
blockSize = 30
 
topLeftX = (screenWidth - playWidth) // 2
topLeftY = screenHeight - playHeight
 
 
# SHAPE FORMATS
 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shapeColours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
 
class Piece(object):
    def __init__(self, x, y, shape) -> None:
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = shapeColours[shapes.index(shape)]
        self.rotation = 0
 
def createGrid(lockedPositions={}):
    grid = [[(0, 0, 0) for _ in range(10)]for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in lockedPositions:
                colour = lockedPositions[(j, i)]
                grid[i][j] = colour
    return grid

 
def convertShapeFormat(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] # Gives the rotation of the current shape eg 1 % 4 = 1, so rotation is 1

    for i, line in enumerate(format):
        row = list(line)

        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # Add in the offset

    return positions

 
def validSpace(shape, grid):
    acceptedPos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    acceptedPos = [j for sub in acceptedPos for j in sub]

    formatted = convertShapeFormat(shape)

    for pos in formatted:
        if pos not in acceptedPos:
            if pos[1] > -1:
                return False
    return True

 
def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
        
    return False
 
def getShape() -> Piece:
    return Piece(5, 0, random.choice(shapes))
 
 
def drawTextMiddle(text, size, color, surface):
    pass
   
def drawGrid(surface, grid) -> None:
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (topLeftX, topLeftY + i * blockSize), (topLeftX + playWidth, topLeftY + i * blockSize))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (topLeftX + j * blockSize, topLeftY), (topLeftX + j * blockSize, topLeftY + playHeight))

 
def clearRows(grid, locked):
    inc = 0

    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]

        if (0, 0, 0) not in row: # No black squares in our row
            inc += 1
            ind = i

            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key= lambda x : x[1])[::-1]:
            x, y = key
            if y < ind: 
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    


 
def drawNextShape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    startX = topLeftX + playWidth + 50
    startY = topLeftY + playHeight / 2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)

        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.colour, (startX + j * blockSize, startY + i * blockSize, blockSize, blockSize))

    surface.blit(label, (startX + 10, startY - 30))


def drawWindow(surface, grid) -> None:
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    
    surface.blit(label, (topLeftX + playWidth / 2 - (label.get_width() / 2), 30))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (topLeftX + j * blockSize, topLeftY + i * blockSize, blockSize, blockSize), 0)

    pygame.draw.rect(surface, (255, 0, 0), (topLeftX, topLeftY, playWidth, playHeight), 4)

    drawGrid(surface, grid)

 
def main():
    lockedPositions = {}
    grid = createGrid(lockedPositions)

    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    fallTime = 0
    fallSpeed = 0.27

    while run:
        grid = createGrid(lockedPositions)
        fallTime += clock.get_rawtime()
        clock.tick()

        if fallTime / 1000 > fallSpeed:
            fallTime = 0
            currentPiece.y += 1

            if not(validSpace(currentPiece, grid)) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1

                    if not validSpace(currentPiece, grid):
                        currentPiece.x += 1

                if event.key == pygame.K_RIGHT:
                    currentPiece.x += 1

                    if not validSpace(currentPiece, grid):
                        currentPiece.x -= 1

                if event.key == pygame.K_DOWN:
                    currentPiece.y += 1

                    if not validSpace(currentPiece, grid):
                        currentPiece.y -= 1

                if event.key == pygame.K_UP:
                    currentPiece.rotation += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.rotation -= 1

        shapePos = convertShapeFormat(currentPiece)

        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.colour

        if changePiece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                lockedPositions[p] = currentPiece.colour
            
            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False
            clearRows(grid, lockedPositions)
        
        drawWindow(win, grid)
        drawNextShape(nextPiece, win)

        pygame.display.update()

        if checkLost(lockedPositions):
            run = False

    pygame.display.quit()

 
def mainMenu():
    pass
 
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Tetris')

main()
#mainMenu(win)  # start game
