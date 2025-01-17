"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512 #400 is another good option
DIMENSION =  8 #Dimensions of the chess
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #For Animations later on
IMAGES = {}


'''
initialize a global dictionary of images. This will be called excactly once in the main
'''

def loadImages();
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces: 
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #We can access an image by saying something like IMAGES['wP']'