"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from ChessEngine import GameState

WIDTH = HEIGHT = 512 #400 is another good option
DIMENSION =  8 #Dimensions of the chess
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #For Animations later on
IMAGES = {}
 
 
'''
initialize a global dictionary of images. This will be called excactly once in the main
'''
 
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #We can access an image by saying something like IMAGES['wP']'
 
    #The main Driver for our code. THis will hanle user Input and updating the Graphics
 
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs =  GameState
    loadImages() #only do this once, before the while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                drawGameState(screen,gs)
                clock.tick(MAX_FPS)
                p.display.flip()
 
 
#Responsible for all the Graphics in the current game state.
 
 
def drawGameState(screen, gs):
    drawBoard(screen) #These Function will draw the Squares on the board
    drawPices(screen, gs.board) #Draw pices on top of those Squares
 
#top left squares are always light.
 
def drawBoard(screen):
    colors = [p.Color("White"), p.Color("Gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
 

 
   
 
 
#Will draw pieces on the Board using the Current GameState.Board
def drawPices(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "__" : #not empty square
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
 
 
 
 
 
    if __name__ == "__main__":
        main()              
 
