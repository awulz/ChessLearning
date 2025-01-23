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

    sq_selected = () # Keine Auswahl am Anfang, speichert den zuletzt geklickten Ort
    player_clicks = [] # Enthält zwei Klicks (Start- und Endposition)

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y)-Koordinaten der Maus
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sq_selected == (row, col): # Doppelklick auf das gleiche Feld
                    sq_selected = () # Auswahl zurücksetzen
                    player_clicks = [] # Klicks zurücksetzen
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                
                if len(player_clicks) == 2: # Nach zwei Klicks versuchen, die Figur zu bewegen
                    move = (player_clicks[0], player_clicks[1])
                    print(f"Move: {move}") # Debugging-Ausgabe
                    gs.board[player_clicks[1][0]][player_clicks[1][1]] = gs.board[player_clicks[0][0]][player_clicks[0][1]]
                    gs.board[player_clicks[0][0]][player_clicks[0][1]] = "--"
                    sq_selected = ()  # Zurücksetzen
                    player_clicks = []

        drawGameState(screen, gs, sq_selected)
        clock.tick(MAX_FPS)
        p.display.flip()

# Responsible for all the Graphics in the current game state.
def drawGameState(screen, gs, sq_selected):
    drawBoard(screen, sq_selected)  # These functions will draw the squares on the board
    drawPieces(screen, gs.board)  # Draw pieces on top of those squares

# Top-left squares are always light.
def drawBoard(screen, sq_selected):
    colors = [p.Color("White"), p.Color("Gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Highlight selected square
    if sq_selected != ():
        r, c = sq_selected
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # Transparenz
        s.fill(p.Color("Blue"))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


# Will draw pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # Check for empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def isValidMove(start_sq, end_sq, board):
    start_piece = board[start_sq[0]][start_sq[1]]
    end_piece = board[end_sq[0]][end_sq[1]]

    if start_piece == "--":
        return False  # Leeres Feld kann nicht bewegt werden
    if start_piece[0] == end_piece[0]:
        return False  # Gleiche Farbe kann nicht angegriffen werden

    # Weitere Regeln für verschiedene Figuren einfügen

    return True


if __name__ == "__main__":
    main()
