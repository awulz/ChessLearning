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
    castling_moves = []  # Castling preview moves

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
                    castling_moves = [] # Clear castling preview
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                
                # Castling preview logic when king is selected
                piece = gs.board[row][col]
                if piece[1] == "K":
                    castling_moves = getCastleMoves(gs, white_to_move)
                else:
                    castling_moves = []  # Clear castling preview
                
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
                        if isValidMove(start_sq, end_sq, gs.board, gs):
                            # Erfolgreichen Zug durchführen
                            gs.board[end_sq[0]][end_sq[1]] = gs.board[start_sq[0]][start_sq[1]]
                            gs.board[start_sq[0]][start_sq[1]] = "--"
                            
                            

                            # Rochade erkennen und ausführen
                            if piece[1] == "K" and abs(start_sq[1] - end_sq[1]) == 2:
                                if end_sq[1] == 6:  # Kingside castling (kurze Rochade)
                                    gs.board[start_sq[0]][5] = gs.board[start_sq[0]][7]  # Turm nach f1/f8
                                    gs.board[start_sq[0]][7] = "--"
                                elif end_sq[1] == 2:  # Queenside castling (lange Rochade)
                                    gs.board[start_sq[0]][3] = gs.board[start_sq[0]][0]  # Turm nach d1/d8
                                    gs.board[start_sq[0]][0] = "--"
                            
                           

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

                            # Überprüfe nach dem Zug auf Schach und Pins
                            gs.in_check, gs.pins, gs.checks = checkForPinsAndChecks(gs, white_to_move)
                            if gs.in_check:
                                print("Check!")

                        else:
                            print("Invalid move!")
                            player_clicks = []
                            sq_selected = ()
                    else:
                        print("Not your turn!")

                    sq_selected = ()  # Zurücksetzen
                    player_clicks = []
                    castling_moves = []  # Clear preview after move
                    
                
        drawGameState(screen, gs, sq_selected, castling_moves)
        clock.tick(MAX_FPS)
        if isCheckmateOrStalemate(gs, white_to_move):
            running = False

        p.display.flip()

# Responsible for all the Graphics in the current game state.
def drawGameState(screen, gs, sq_selected, castling_moves=[]):
    drawBoard(screen, sq_selected, castling_moves)  # These functions will draw the squares on the board
    drawPieces(screen, gs.board)  # Draw pieces on top of those squares

# Top-left squares are always light.
def drawBoard(screen, sq_selected, castling_moves=[]):
    colors = [p.Color("White"), p.Color("Gray")]
    highlight_color = p.Color("Yellow") # Farbe für Castling-Preview
    font = p.font.SysFont("Arial", 12, bold=True) # Schriftart für Koordinaten

    # Reihen- und Spalten-Beschriftungen
    ranks = [str(8 - i) for i in range(8)]  # Zahlen 8 bis 1 für Reihen
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']  # Buchstaben für Spalten

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]

            if sq_selected == (r, c):
                color = p.Color("Blue")

            if(r,c) in castling_moves:
                color = highlight_color # Highlight Castling-Moves

            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
            if c == 0:
                rank_text = font.render(ranks[r], True, p.Color("Black"))
                screen.blit(rank_text, (5, r * SQ_SIZE + 5))
            if r == 7:
                file_text = font.render(files[c], True, p.Color("Black"))
                screen.blit(file_text, (c * SQ_SIZE + SQ_SIZE - 12, r * SQ_SIZE + 0))

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

def checkForPinsAndChecks(gs, isWhite):
    pins = []  # Gefesselte Figuren
    checks = []  # Schachbedrohungen
    in_check = False

    # Position des Königs finden
    king_row, king_col = None, None
    for r in range(8):
        for c in range(8):
            if gs.board[r][c] == ('wK' if isWhite else 'bK'):
                king_row, king_col = r, c
                break

    # Richtungen für potenzielle Angreifer (Türme, Läufer, Dame)
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Vertikal und horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]

    for d in directions:
        possible_pin = None
        for i in range(1, 8):
            end_row, end_col = king_row + d[0] * i, king_col + d[1] * i
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                piece = gs.board[end_row][end_col]
                if piece != "--":
                    if piece[0] == ('w' if isWhite else 'b'):
                        if possible_pin is None:
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break  # Zweite eigene Figur -> kein Pin
                    else:
                        piece_type = piece[1]
                        if (piece_type == "R" and d in directions[:4]) or \
                           (piece_type == "B" and d in directions[4:]) or \
                           (piece_type == "Q") or \
                           (piece_type == "P" and i == 1 and ((isWhite and d in [(-1, -1), (-1, 1)]) or (not isWhite and d in [(1, -1), (1, 1)]))) or \
                           (piece_type == "K" and i == 1):
                            if possible_pin is None:
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                            else:
                                pins.append(possible_pin)
                            break
                        else:
                            break
            else:
                break

    return in_check, pins, checks


def isValidMove(start_sq, end_sq, board, gs):
    start_row, start_col = start_sq
    end_row, end_col = end_sq
    piece = board[start_row][start_col]
    target_piece = board[end_row][end_col]

    # Überprüfen, ob das Startfeld leer ist
    if piece == "--":
        return False  # Leeres Feld kann nicht bewegt werden

    # Prüfen, ob ein eigenes Stück angegriffen wird
    if target_piece != "--" and piece[0] == target_piece[0]:
        if not hasattr(gs, 'invalid_move_logged'):
            print(f"Invalid move: Cannot capture own piece at {end_sq}")
            gs.invalid_move_logged = True
        return False

    # Überprüfen, ob das Feld festgesetzt ist (Pins)
    for pin in gs.pins:
        if pin[0] == start_row and pin[1] == start_col:
            print(f"Pin detected: {start_sq} -> {end_sq}, allowed direction: {(pin[2], pin[3])}")
            if (end_row - start_row, end_col - start_col) != (pin[2], pin[3]):
                print("Invalid move: Piece is pinned!")
                return False  # Bewegung nicht erlaubt aufgrund der Fesselung

    # Überprüfen, ob der Zug den König im Schach lässt
def doesMoveLeaveKingInCheck(start_sq, end_sq, board, gs):
    temp_board = [row[:] for row in board]  # Kopie des Spielfelds erstellen
    temp_board[end_sq[0]][end_sq[1]] = temp_board[start_sq[0]][start_sq[1]]
    temp_board[start_sq[0]][start_sq[1]] = "--"

    king_color = "wK" if board[start_sq[0]][start_sq[1]][0] == 'w' else "bK"
    
    # Königslage suchen
    king_pos = None
    for r in range(8):
        for c in range(8):
            if temp_board[r][c] == king_color:
                king_pos = (r, c)
                break

    if king_pos is None:
        print("FEHLER: König nicht gefunden auf dem Brett!")
        return True

    # Prüfen, ob der König im Schach steht
    in_check, _, _ = checkForPinsAndChecks(gs, king_color[0] == 'w')
    if in_check:
        print(f"König bleibt im Schach nach {start_sq} -> {end_sq}")
    return in_check



def canCastleKingside(board, isWhite, gs):
    row = 7 if isWhite else 0

    if isWhite and (gs.white_king_moved or gs.white_rook_king_moved):
        return False
    if not isWhite and (gs.black_king_moved or gs.black_rook_king_moved):
        return False

    # Prüfen, ob Felder zwischen König und Turm frei sind
    if board[row][5] == "--" and board[row][6] == "--":
        return True
    return False


def canCastleQueenside(board, isWhite, gs):
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



def isValidKingMove(start_sq, end_sq, board, isWhite, gs):
    start_row, start_col = start_sq
    end_row, end_col = end_sq

    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)

    # Der König darf sich maximal 1 Feld in jede Richtung bewegen
    if row_diff <= 1 and col_diff <= 1:
        # Stelle sicher, dass das Zielfeld nicht von derselben Farbe ist
        if board[end_row][end_col] == "--" or board[end_row][end_col][0] != board[start_row][start_col][0]:
            return True
    
    if col_diff == 2 and row_diff == 0:
        if end_col == 6 and canCastleKingside(board, isWhite, gs):  # kurze Rochade
            return True
        elif end_col == 2 and canCastleQueenside(board, isWhite, gs):  # lange Rochade
            return True

    return False

def getCastleMoves(gs, isWhite):
    moves = []
    row = 7 if isWhite else 0

    # Prüfen, ob Rochade möglich ist
    if canCastleKingside(gs.board, isWhite, gs):
        moves.append((row, 6))  # King-Side Castling (g1 / g8)

    if canCastleQueenside(gs.board, isWhite, gs):
        moves.append((row, 2))  # Queen-Side Castling (c1 / c8)

    return moves

def checkForPinsAndChecks(gs, isWhite):
    pins = []  # Gefesselte Figuren
    checks = []  # Schachbedrohungen
    in_check = False

    # Finde die Position des Königs
    king_row, king_col = None, None
    for r in range(8):
        for c in range(8):
            if gs.board[r][c] == ('wK' if isWhite else 'bK'):
                king_row, king_col = r, c
                break

    # Richtungen für mögliche Angriffe (Turm, Läufer, Dame)
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Vertikal, horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]

    for d in directions:
        possible_pinned_piece = None
        for i in range(1, 8):
            end_row, end_col = king_row + d[0] * i, king_col + d[1] * i
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                piece = gs.board[end_row][end_col]
                if piece != "--":
                    if piece[0] == ('w' if isWhite else 'b'):
                        if possible_pinned_piece is None:
                            possible_pinned_piece = (end_row, end_col, d[0], d[1])
                        else:
                            break  # Zweite eigene Figur -> kein Pin
                    else:
                        # Gegnerische Figur -> prüfen, ob Angriff möglich ist
                        piece_type = piece[1]
                        if (piece_type == "R" and d in directions[:4]) or \
                           (piece_type == "B" and d in directions[4:]) or \
                           (piece_type == "Q") or \
                           (piece_type == "P" and i == 1 and ((isWhite and d in [(-1, -1), (-1, 1)]) or (not isWhite and d in [(1, -1), (1, 1)]))) or \
                           (piece_type == "K" and i == 1):
                            if possible_pinned_piece is None:
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                            else:
                                pins.append(possible_pinned_piece)
                            break
                        else:
                            break
            else:
                break  # Außerhalb des Bretts

    return in_check, pins, checks

def isCheckmateOrStalemate(gs, isWhite):
    gs.in_check, gs.pins, gs.checks = checkForPinsAndChecks(gs, isWhite)
    
    legal_moves_exist = False
    for r in range(8):
        for c in range(8):
            if gs.board[r][c][0] == ('w' if isWhite else 'b'):
                for row in range(8):
                    for col in range(8):
                        if isValidMove((r, c), (row, col), gs.board, gs):
                            if not doesMoveLeaveKingInCheck((r, c), (row, col), gs.board, gs):
                                legal_moves_exist = True
                                break
                    if legal_moves_exist:
                        break
            if legal_moves_exist:
                break

    print(f"Legal moves exist: {legal_moves_exist}, In check: {gs.in_check}")

    if legal_moves_exist:
        return False  # Es gibt noch legale Züge

    if gs.in_check:
        print("Checkmate detected!")
    else:
        print("Stalemate detected!")

    return True  # Wenn keine legalen Züge mehr vorhanden sind, ist es Schachmatt oder Patt




def doesMoveLeaveKingInCheck(start_sq, end_sq, board, gs):
    temp_board = [row[:] for row in board]  # Kopiere das aktuelle Board
    temp_board[end_sq[0]][end_sq[1]] = temp_board[start_sq[0]][start_sq[1]]
    temp_board[start_sq[0]][start_sq[1]] = "--"

    # Bestimme, wessen König wir überprüfen müssen
    king_color = "wK" if board[start_sq[0]][start_sq[1]][0] == 'w' else "bK"

    # Finde die Position des Königs
    king_pos = None
    for r in range(8):
        for c in range(8):
            if temp_board[r][c] == king_color:
                king_pos = (r, c)
                break

    if king_pos is None:
        return True  # König ist nicht auf dem Brett (Fehler)

    # Prüfe, ob der König nach dem Zug im Schach steht
    in_check, _, _ = checkForPinsAndChecks(gs, king_color[0] == 'w')
    return in_check





if __name__ == "__main__":
    main()
