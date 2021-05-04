# handles user input and displayes the current game state # 

import pygame as p
import Engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bK', 'bQ', 'bB', 'bN', 'bR', 'bP']

    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")
        
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = Engine.GameState()
    moveMade = False
    validMoves = gameState.getValidMoves()
    #load images only once
    loadImages()
    running = True
    selectedSquare = () # tracks last move
    playerClicks = [] # count mouseclicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x,y
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if selectedSquare == (row, col):
                    selectedSquare = () # undoes the move in progress
                    playerClicks.pop()
                else: 
                    selectedSquare = (row,col)
                    playerClicks.append(selectedSquare) # counts mouseclick
                if len(playerClicks) == 2:
                    move = Engine.Move(playerClicks[0],playerClicks[1], gameState.board)
                    if move in validMoves:
                        print(move.getChessNotation())
                        gameState.makeMove(move)
                        moveMade = True
                    selectedSquare = ()
                    playerClicks = []
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    gameState.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False
        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, gameState)

def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))


if __name__ == "__main__":
    main()

