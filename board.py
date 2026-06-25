from utils import chess_to_index

from validators import (
    is_valid_pawn_move,
    is_valid_knight_move,
    is_valid_bishop_move,
    is_valid_rook_move,
    is_valid_queen_move,
    is_valid_king_move,
    is_in_check,
    copy_board
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
        self.white_king_moved = False
        self.black_king_moved = False

        self.white_rook_a_moved = False
        self.white_rook_h_moved = False

        self.black_rook_a_moved = False
        self.black_rook_h_moved = False
        self.en_passant_target = None
    def display(self):

        print(f"\nTurn: {self.turn}\n")

        for row_num, row in enumerate(self.board):
            print(8 - row_num, " ".join(row))

        print("  a b c d e f g h")

    def would_leave_king_in_check(
    self,
    start_row,
    start_col,
    end_row,
    end_col):

        temp_board = copy_board(self.board)

        piece = temp_board[start_row][start_col]

        temp_board[end_row][end_col] = piece
        temp_board[start_row][start_col] = "."

        color = "white" if piece.isupper() else "black"

        return is_in_check(temp_board, color)
    
    def is_valid_move_for_piece(
    self,
    piece,
    start_row,
    start_col,
    end_row,
    end_col):

        if piece.lower() == "p":
            return is_valid_pawn_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col,
                self.en_passant_target
            )

        elif piece.lower() == "n":
            return is_valid_knight_move(
                start_row,
                start_col,
                end_row,
                end_col
            )

        elif piece.lower() == "b":
            return is_valid_bishop_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col
            )

        elif piece.lower() == "r":
            return is_valid_rook_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col
            )

        elif piece.lower() == "q":
            return is_valid_queen_move(
                self.board,
                start_row,
                start_col,
                end_row,
                end_col
            )

        elif piece.lower() == "k":
            return is_valid_king_move(
                start_row,
                start_col,
                end_row,
                end_col
            )

        return False
    
    def has_any_legal_move(self, color):

        for start_row in range(8):
            for start_col in range(8):

                piece = self.board[start_row][start_col]

                if piece == ".":
                    continue

                if color == "white" and piece.islower():
                    continue

                if color == "black" and piece.isupper():
                    continue

                for end_row in range(8):
                    for end_col in range(8):
                        if start_row == end_row and start_col == end_col:
                            continue
                        target = self.board[end_row][end_col]

                        # Don't capture own piece
                        if target != ".":

                            if piece.isupper() and target.isupper():
                                continue

                            if piece.islower() and target.islower():
                                continue

                        if not self.is_valid_move_for_piece(
                            piece,
                            start_row,
                            start_col,
                            end_row,
                            end_col
                        ):
                            continue

                        if not self.would_leave_king_in_check(
                            start_row,
                            start_col,
                            end_row,
                            end_col
                        ):
                            return True

        return False
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
                end_col,
                self.en_passant_target
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

            # Black kingside castling
            if (
                piece == "k"
                and start_row == 0
                and start_col == 4
                and end_row == 0
                and end_col == 6
            ):

                if self.black_king_moved:
                    print("King already moved")
                    return

                if self.black_rook_h_moved:
                    print("Rook already moved")
                    return

                if self.board[0][5] != "." or self.board[0][6] != ".":
                    print("Path blocked")
                    return

                self.board[0][6] = "k"
                self.board[0][5] = "r"

                self.board[0][4] = "."
                self.board[0][7] = "."

                self.black_king_moved = True
                self.black_rook_h_moved = True

                print("Black castled kingside!")

                self.turn = "white"
                return
            # White kingside castling
            if (
                piece == "K"
                and start_row == 7
                and start_col == 4
                and end_row == 7
                and end_col == 6
            ):

                if self.white_king_moved:
                    print("King already moved")
                    return

                if self.white_rook_h_moved:
                    print("Rook already moved")
                    return

                if self.board[7][5] != "." or self.board[7][6] != ".":
                    print("Path blocked")
                    return

                self.board[7][6] = "K"
                self.board[7][5] = "R"

                self.board[7][4] = "."
                self.board[7][7] = "."

                self.white_king_moved = True
                self.white_rook_h_moved = True
                print("White castled kingside!")
                self.turn = "black"
                return
            # White queenside castling
            if (
                piece == "K"
                and start_row == 7
                and start_col == 4
                and end_row == 7
                and end_col == 2
            ):

                if self.white_king_moved:
                    print("King already moved")
                    return

                if self.white_rook_a_moved:
                    print("Rook already moved")
                    return

                if (
                    self.board[7][1] != "."
                    or self.board[7][2] != "."
                    or self.board[7][3] != "."
                ):
                    print("Path blocked")
                    return

                self.board[7][2] = "K"
                self.board[7][3] = "R"

                self.board[7][4] = "."
                self.board[7][0] = "."

                self.white_king_moved = True
                self.white_rook_a_moved = True

                print("White castled queenside!")

                self.turn = "black"
                return
            # Black queenside castling
            if (
                piece == "k"
                and start_row == 0
                and start_col == 4
                and end_row == 0
                and end_col == 2
            ):

                if self.black_king_moved:
                    print("King already moved")
                    return

                if self.black_rook_a_moved:
                    print("Rook already moved")
                    return

                if (
                    self.board[0][1] != "."
                    or self.board[0][2] != "."
                    or self.board[0][3] != "."
                ):
                    print("Path blocked")
                    return

                self.board[0][2] = "k"
                self.board[0][3] = "r"

                self.board[0][4] = "."
                self.board[0][0] = "."

                self.black_king_moved = True
                self.black_rook_a_moved = True

                print("Black castled queenside!")

                self.turn = "white"
                return
            # Normal king move
            if not is_valid_king_move(
                start_row,
                start_col,
                end_row,
                end_col
            ):
                print("Invalid king move")
                return
            
        if self.would_leave_king_in_check(
            start_row,
            start_col,
            end_row,
            end_col
        ):
            print("Illegal move: king would remain in check")
            return
        
        # Reset en passant target
        self.en_passant_target = None

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = "."

        # En passant capture
        if (
            piece == "P"
            and start_col != end_col
            and target == "."
        ):
            self.board[end_row + 1][end_col] = "."

        elif (
            piece == "p"
            and start_col != end_col
            and target == "."
        ):
            self.board[end_row - 1][end_col] = "."
        # White pawn moved two squares
        if piece == "P" and start_row == 6 and end_row == 4:
            self.en_passant_target = (5, start_col)

        # Black pawn moved two squares
        elif piece == "p" and start_row == 1 and end_row == 3:
            self.en_passant_target = (2, start_col)

        # White pawn promotion
        if piece == "P" and end_row == 0:
            self.board[end_row][end_col] = "Q"
            print("White pawn promoted to Queen!")

        # Black pawn promotion
        if piece == "p" and end_row == 7:
            self.board[end_row][end_col] = "q"
            print("Black pawn promoted to Queen!")
        if piece == "K":
            self.white_king_moved = True

        elif piece == "k":
            self.black_king_moved = True

        elif piece == "R":

            if start_row == 7 and start_col == 0:
                self.white_rook_a_moved = True

            elif start_row == 7 and start_col == 7:
                self.white_rook_h_moved = True

        elif piece == "r":

            if start_row == 0 and start_col == 0:
                self.black_rook_a_moved = True

            elif start_row == 0 and start_col == 7:
                self.black_rook_h_moved = True
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        if is_in_check(self.board, self.turn):

            if not self.has_any_legal_move(self.turn):
                print(f"Checkmate! {'White' if self.turn == 'black' else 'Black'} wins!")
                exit()

            else:
                print(f"{self.turn.capitalize()} is in Check!")

        else:

            if not self.has_any_legal_move(self.turn):
                print("Stalemate! Draw!")
                exit()

        