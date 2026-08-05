import random


# Fixed seed makes the generated numbers
# identical every time the engine starts.
random.seed(42)


PIECES = [
    "P", "N", "B", "R", "Q", "K",
    "p", "n", "b", "r", "q", "k"
]


# Random 64-bit number for:
# piece × square
ZOBRIST_TABLE = {}

for piece in PIECES:

    ZOBRIST_TABLE[piece] = []

    for square in range(64):

        random_number = random.getrandbits(64)

        ZOBRIST_TABLE[piece].append(
            random_number
        )


# Random number representing side to move
SIDE_TO_MOVE = random.getrandbits(64)

# Castling rights
CASTLING_RIGHTS = {
    "white_kingside": random.getrandbits(64),
    "white_queenside": random.getrandbits(64),
    "black_kingside": random.getrandbits(64),
    "black_queenside": random.getrandbits(64),
}


# En passant files: a-h
EN_PASSANT_FILES = [
    random.getrandbits(64)
    for _ in range(8)
]


def compute_zobrist_hash(board_obj):
    """
    Calculate a 64-bit Zobrist hash for the
    complete chess position state.
    """

    hash_value = 0

    # -------------------------
    # Piece positions
    # -------------------------

    for row in range(8):
        for col in range(8):

            piece = board_obj.board[row][col]

            if piece == ".":
                continue

            square = row * 8 + col

            hash_value ^= ZOBRIST_TABLE[piece][square]

    # -------------------------
    # Side to move
    # -------------------------

    if board_obj.turn == "black":
        hash_value ^= SIDE_TO_MOVE

    # -------------------------
    # Castling rights
    # -------------------------

    if (
        not board_obj.white_king_moved
        and not board_obj.white_rook_h_moved
    ):
        hash_value ^= CASTLING_RIGHTS["white_kingside"]

    if (
        not board_obj.white_king_moved
        and not board_obj.white_rook_a_moved
    ):
        hash_value ^= CASTLING_RIGHTS["white_queenside"]

    if (
        not board_obj.black_king_moved
        and not board_obj.black_rook_h_moved
    ):
        hash_value ^= CASTLING_RIGHTS["black_kingside"]

    if (
        not board_obj.black_king_moved
        and not board_obj.black_rook_a_moved
    ):
        hash_value ^= CASTLING_RIGHTS["black_queenside"]

    # -------------------------
    # En passant
    # -------------------------

    if board_obj.en_passant_target is not None:

        target = board_obj.en_passant_target

        # If stored as chess notation, e.g. "e3"
        if isinstance(target, str):
            file_index = ord(target[0]) - ord("a")

        # If stored as (row, col)
        else:
            _, file_index = target

        hash_value ^= EN_PASSANT_FILES[file_index]

    return hash_value