"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from ChessEngine import GameState

WIDTH = HEIGHT = 512  # 400 is another good option
DIMENSION = 8  # Dimensions of the chess
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For Animations later on
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main function.
'''
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # We can access an image by saying something like IMAGES['wP']

# The main Driver for our code. This will handle user input and updating the Graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = GameState()  # Hier wurde die Instanziierung korrigiert
    loadImages()  # Only do this once, before the while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# Responsible for all the Graphics in the current game state.
def drawGameState(screen, gs):
    drawBoard(screen)  # These functions will draw the squares on the board
    drawPieces(screen, gs.board)  # Draw pieces on top of those squares

# Top-left squares are always light.
def drawBoard(screen):
    colors = [p.Color("White"), p.Color("Gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Will draw pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Check for empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
