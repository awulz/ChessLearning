"""
This Section is where we store all the data and information about the current state of the Game. It will also be responsible for determening the valid Moves of the current state.
It will also keep a move log.
"""
class GameState():
    def __init__(self):
        #The Board is a 8x8 2d list, each Element of the List hast 2 characters.
        #The First character represents the, color of the piece "w" or "b", the second character represents the Type of the piece.
        #The string "--" represents an empty scare with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []