from piece_square_tables import (
    WHITE_PAWN_TABLE,
    BLACK_PAWN_TABLE,
    WHITE_KNIGHT_TABLE,
    BLACK_KNIGHT_TABLE,
    WHITE_BISHOP_TABLE,
    BLACK_BISHOP_TABLE,
    WHITE_ROOK_TABLE,
    BLACK_ROOK_TABLE,
    WHITE_QUEEN_TABLE,
    BLACK_QUEEN_TABLE,
    WHITE_KING_TABLE,
    BLACK_KING_TABLE,
)
from piece_square_tables import WHITE_PAWN_TABLE, BLACK_PAWN_TABLE
piece_values = {
    "P": 100,
    "N": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 20000,

    "p": -100,
    "n": -320,
    "b": -330,
    "r": -500,
    "q": -900,
    "k": -20000
}


def evaluate_board(board):

    score = 0

    piece_values = {
        "P": 100,
        "N": 320,
        "B": 330,
        "R": 500,
        "Q": 900,
        "K": 20000,

        "p": -100,
        "n": -320,
        "b": -330,
        "r": -500,
        "q": -900,
        "k": -20000,
    }

    for row in range(8):
        for col in range(8):

            piece = board[row][col]

            if piece == ".":
                continue

            # Material value
            score += piece_values[piece]

            # ==========================
            # WHITE PIECES
            # ==========================

            if piece == "P":
                score += WHITE_PAWN_TABLE[row][col]

            elif piece == "N":
                score += WHITE_KNIGHT_TABLE[row][col]

            elif piece == "B":
                score += WHITE_BISHOP_TABLE[row][col]

            elif piece == "R":
                score += WHITE_ROOK_TABLE[row][col]

            elif piece == "Q":
                score += WHITE_QUEEN_TABLE[row][col]

            elif piece == "K":
                score += WHITE_KING_TABLE[row][col]

            # ==========================
            # BLACK PIECES
            # ==========================

            elif piece == "p":
                score -= BLACK_PAWN_TABLE[row][col]

            elif piece == "n":
                score -= BLACK_KNIGHT_TABLE[row][col]

            elif piece == "b":
                score -= BLACK_BISHOP_TABLE[row][col]

            elif piece == "r":
                score -= BLACK_ROOK_TABLE[row][col]

            elif piece == "q":
                score -= BLACK_QUEEN_TABLE[row][col]

            elif piece == "k":
                score -= BLACK_KING_TABLE[row][col]

    return score