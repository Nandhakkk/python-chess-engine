from utils import chess_to_index
class Board:
    def __init__(self):
        self.board = [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"]
        ]

    def display(self):
        for row in self.board:
            print(" ".join(row))
    def move_piece(self, start, end):

        start_row, start_col = chess_to_index(start)
        end_row, end_col = chess_to_index(end)

        piece = self.board[start_row][start_col]

        if piece == ".":
            print("No piece at", start)
            return

        if piece == "P":

            if not self.is_valid_pawn_move(
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid pawn move")
                return

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."
    def is_valid_pawn_move(self, start_row, start_col, end_row, end_col):

        if start_col != end_col:
            return False

        # one-square move
        if end_row == start_row - 1:
            if self.board[end_row][end_col] == ".":
                return True

        # two-square move from starting position
        if start_row == 6 and end_row == 4:

            if self.board[5][start_col] == "." and self.board[4][start_col] == ".":
                return True

        return False