from piece_square_tables import (
    WHITE_PAWN_TABLE,
    BLACK_PAWN_TABLE,
    WHITE_KNIGHT_TABLE,
    BLACK_KNIGHT_TABLE,
    WHITE_BISHOP_TABLE,
    BLACK_BISHOP_TABLE,
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

            # Base material value
            score += piece_values[piece]

            # White Pawn
            if piece == "P":
                score += WHITE_PAWN_TABLE[row][col]

            # Black Pawn
            elif piece == "p":
                score -= BLACK_PAWN_TABLE[row][col]

            # White Knight
            elif piece == "N":
                score += WHITE_KNIGHT_TABLE[row][col]

            # Black Knight
            elif piece == "n":
                score -= BLACK_KNIGHT_TABLE[row][col]

            # White Bishop
            elif piece == "B":
                score += WHITE_BISHOP_TABLE[row][col]

            # Black Bishop
            elif piece == "b":
                score -= BLACK_BISHOP_TABLE[row][col]

    return score