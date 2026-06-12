from utils import chess_to_index
class Board:
    def __init__(self):
        self.turn = "white"
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

        print(f"\nTurn: {self.turn}\n")

        for row in self.board:
            print(" ".join(row))
    def move_piece(self, start, end):

        start_row, start_col = chess_to_index(start)
        end_row, end_col = chess_to_index(end)

        piece = self.board[start_row][start_col]

        if piece == ".":
            print("No piece at", start)
            return
        if self.turn == "white" and piece.islower():
            print("It's White's turn")
            return

        if self.turn == "black" and piece.isupper():
            print("It's Black's turn")
            return
        if piece.lower() == "p":

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
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    def is_valid_pawn_move(self, start_row, start_col, end_row, end_col):

        piece = self.board[start_row][start_col]

        if start_col != end_col:
            return False

        # White pawn
        if piece == "P":

            if end_row == start_row - 1:
                if self.board[end_row][end_col] == ".":
                    return True

            if start_row == 6 and end_row == 4:
                if self.board[5][start_col] == "." and self.board[4][start_col] == ".":
                    return True

        # Black pawn
        elif piece == "p":

            if end_row == start_row + 1:
                if self.board[end_row][end_col] == ".":
                    return True

            if start_row == 1 and end_row == 3:
                if self.board[2][start_col] == "." and self.board[3][start_col] == ".":
                    return True

        return False