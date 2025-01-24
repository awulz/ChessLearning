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
    white_to_move = True


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
                    start_sq = player_clicks[0]
                    end_sq = player_clicks[1]

                    piece = gs.board[start_sq[0]][start_sq[1]]

                    if piece == "--":
                        print("Error: Can't move an empty square!")
                        sq_selected = () #Auswahl zurücksetzen
                        player_clicks = []
                        continue
                    
                    # Überprüfe, ob der richtige Spieler am Zug ist
                    if(white_to_move and piece [0] == 'w') or (not white_to_move and piece[0] == 'b'):
                        if isValidMove(start_sq, end_sq, gs.board):

                            # Rochade erkennen und ausführen
                            if piece[1] == "K" and abs(start_sq[1] - end_sq[1]) == 2:
                                if end_sq[1] == 6:  # Kingside castling (kurze Rochade)
                                    gs.board[start_sq[0]][5] = gs.board[start_sq[0]][7]  # Turm nach f1/f8
                                    gs.board[start_sq[0]][7] = "--"
                                elif end_sq[1] == 2:  # Queenside castling (lange Rochade)
                                    gs.board[start_sq[0]][3] = gs.board[start_sq[0]][0]  # Turm nach d1/d8
                                    gs.board[start_sq[0]][0] = "--"
                            
                            # König oder Turm an neue Position setzen
                            gs.board[end_sq[0]][end_sq[1]] = gs.board[start_sq[0]][start_sq[1]]
                            gs.board[start_sq[0]][start_sq[1]] = "--"

                            # Rochade-Berechtigungen entfernen
                            if piece[1] == "K":
                                if white_to_move:
                                    gs.white_king_moved = True
                                else:
                                    gs.black_king_moved = True
                            if piece[1] == "R":
                                if start_sq[1] == 0:  # Turm auf der a-Linie (Queenside)
                                    if white_to_move:
                                        gs.white_rook_queen_moved = True
                                    else:
                                        gs.black_rook_queen_moved = True
                                elif start_sq[1] == 7:  # Turm auf der h-Linie (Kingside)
                                    if white_to_move:
                                        gs.white_rook_king_moved = True
                                    else:
                                        gs.black_rook_king_moved = True

                            white_to_move = not white_to_move # Spielerwechsel nach erfolgreichem Zug
                            print("Move successful. Next player!")
                       
                        else:
                            print("Invalid move!")
                    else:
                        print("Not your turn!")

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
    start_row, start_col = start_sq
    end_row, end_col = end_sq
    piece = board[start_row][start_col]
    target_piece = board[end_row][end_col]

    if target_piece != "--" and piece[0] == target_piece[0]:
        print("Invalid move: Cannot capture own piece!")
        return False

    if piece == "--":
        return False  # Leeres Feld kann nicht bewegt werden
    
    piece_type = piece[1] # Zweites Zeichen gibt die Art der Figur an

    if piece_type == "P": # Bauer
        return isValidPawnMove(start_sq, end_sq, board, piece[0])
    elif piece_type == "R": # Turm
        return isValidRookMove(start_sq, end_sq, board)
    elif piece_type == "N": # Springer
        return isValidKnightMove(start_sq, end_sq)
    elif piece_type == "B": # Läufer
        return isValidBishopMove(start_sq, end_sq, board)
    elif piece_type == "Q": # Dame
        return isValidQueenMove(start_sq, end_sq, board)
    elif piece_type == "K": # König
        return isValidKingMove(start_sq, end_sq, board)
    
    return False # Standardmässig ungültiger Zug

def canCastleKingside(board, isWhite):
    row = 7 if isWhite else 0

    if isWhite and (gs.white_king_moved or gs.white_rook_king_moved):
        return False
    if not isWhite and (gs.black_king_moved or gs.black_rook_king_moved):
        return False

    # Prüfen, ob Felder zwischen König und Turm frei sind
    if board[row][5] == "--" and board[row][6] == "--":
        return True
    return False


def canCastleQueenside(board, isWhite):
    row = 7 if isWhite else 0

    if isWhite and (gs.white_king_moved or gs.white_rook_queen_moved):
        return False
    if not isWhite and (gs.black_king_moved or gs.black_rook_queen_moved):
        return False

    # Prüfen, ob Felder zwischen König und Turm frei sind
    if board[row][1] == "--" and board[row][2] == "--" and board[row][3] == "--":
        return True
    return False
  
def isValidPawnMove (start_sq, end_sq, board, color):
    start_row, start_col = start_sq
    end_row, end_col = end_sq

    direction = -1 if color == "w" else 1 # Weiß bewegt sich nach oben, Schwarz nach unten
    
    # Normaler Bauerzug (ein Feld nach vorne)
    if start_col == end_col and board[end_row][end_col] == "--":
        if end_row == start_row + direction:
            return True
        # Doppelschritt aus der Startposition
        if (color == "w" and start_row == 6) or (color == "b" and start_row == 1):
            if end_row == start_row + 2 * direction and board[start_row + direction][start_col] == "--":
                return True
    
    # Schlagen diagonal
    if abs(start_col - end_col) == 1 and end_row == start_row + direction:
        if board[end_row][end_col] != "--" and board[end_row][end_col][0] !=color:
            return True
    
    #En Passant Schlag
    if abs(start_col - end_col) == 1 and end_row == start_row + direction:
        if board[start_row][end_col] == ("bP" if color == "w" else "wP") and board[end_row][end_col] == "--":
            return True

    return False

def isValidKnightMove(start_sq, end_sq):
    start_row, start_col = start_sq
    end_row, end_col = end_sq

    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)

    # Springer bewegt sich in L-Form (2-1 oder 1-2 Felder)
    return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

def isValidRookMove(start_sq, end_sq, board):
    start_row, start_col = start_sq
    end_row, end_col = end_sq

    if start_row == end_row:  # Gleiche Zeile, überprüfe Spaltenbewegung
        for c in range(min(start_col, end_col) + 1, max(start_col, end_col)):
            if board[start_row][c] != "--":
                return False
        return True

    if start_col == end_col:  # Gleiche Spalte, überprüfe Zeilenbewegung
        for r in range(min(start_row, end_row) + 1, max(start_row, end_row)):
            if board[r][start_col] != "--":
                return False
        return True
    
def isValidBishopMove(start_sq, end_sq, board):
    start_row, start_col = start_sq
    end_row, end_col = end_sq

    if abs(start_row - end_row) == abs(start_col - end_col): # Überprüfung auf diagonale Bewegung
        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1

        r, c = start_row + step_row, start_col + step_col
        while r != end_row and c != end_col:
             if board[r][c] != "--":  # Falls ein anderes Stück im Weg ist
                 return False
             r += step_row
             c += step_col
        return True
    
    return False
    
def isValidQueenMove(start_sq, end_sq, board):
    return isValidRookMove(start_sq, end_sq, board) or isValidBishopMove(start_sq, end_sq, board)



def isValidKingMove(start_sq, end_sq, board):
    start_row, start_col = start_sq
    end_row, end_col = end_sq

    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)

    # Der König darf sich maximal 1 Feld in jede Richtung bewegen
    if row_diff <= 1 and col_diff <= 1:
        # Stelle sicher, dass das Zielfeld nicht von derselben Farbe ist
        if board[end_row][end_col] == "--" or board[end_row][end_col][0] != board[start_row][start_col][0]:
            return True
    return False






if __name__ == "__main__":
    main()
