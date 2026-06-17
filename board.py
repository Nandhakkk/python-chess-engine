from utils import chess_to_index

from validators import (
    is_valid_pawn_move,
    is_valid_knight_move,
    is_valid_bishop_move,
    is_valid_rook_move,
    is_valid_queen_move,
    is_valid_king_move,
    is_in_check
)


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

        for row_num, row in enumerate(self.board):
            print(8 - row_num, " ".join(row))

        print("  a b c d e f g h")

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

        target = self.board[end_row][end_col]

        if target != ".":

            if piece.isupper() and target.isupper():
                print("Cannot capture your own piece")
                return

            if piece.islower() and target.islower():
                print("Cannot capture your own piece")
                return

        if piece.lower() == "p":

            if not is_valid_pawn_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid pawn move")
                return

        elif piece.lower() == "n":

            if not is_valid_knight_move(
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid knight move")
                return

        elif piece.lower() == "b":

            if not is_valid_bishop_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid bishop move")
                return

        elif piece.lower() == "r":

            if not is_valid_rook_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid rook move")
                return

        elif piece.lower() == "q":

            if not is_valid_queen_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid queen move")
                return

        elif piece.lower() == "k":

            if not is_valid_king_move(
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid king move")
                return

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."
        
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        if is_in_check(self.board, self.turn):
            print(f"{self.turn.capitalize()} is in Check!")