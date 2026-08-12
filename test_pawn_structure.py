from board import Board
from evaluation import evaluate_pawn_structure


def empty_board():

    board = Board()

    board.board = [
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
        ["."] * 8,
    ]

    board.en_passant_target = None

    return board


# ==========================
# TEST 1: White doubled pawns
# ==========================

board = empty_board()

board.board[4][0] = "P"
board.board[5][0] = "P"

# Black pawns block the passed-pawn bonus.
board.board[6][0] = "p"
board.board[6][1] = "p"

score = evaluate_pawn_structure(board)

assert score < 0

print("[PASS] White doubled pawns")


# ==========================
# TEST 2: Black doubled pawns
# ==========================

board = empty_board()

board.board[3][0] = "p"
board.board[2][0] = "p"

# White pawns block the passed-pawn bonus.
board.board[1][0] = "P"
board.board[1][1] = "P"

score = evaluate_pawn_structure(board)

assert score > 0

print("[PASS] Black doubled pawns")


# ==========================
# TEST 3: White isolated pawn
# ==========================

board = empty_board()

board.board[5][3] = "P"

# Black pawn blocks passed-pawn bonus.
board.board[3][3] = "p"

# Give black a neighbouring pawn so it is not isolated.
board.board[3][4] = "p"

score = evaluate_pawn_structure(board)

assert score < 0

print("[PASS] White isolated pawn")


# ==========================
# TEST 4: Black isolated pawn
# ==========================

board = empty_board()

board.board[2][3] = "p"

# White pawn blocks passed-pawn bonus.
board.board[4][3] = "P"

# Give white a neighbouring pawn so it is not isolated.
board.board[4][4] = "P"

score = evaluate_pawn_structure(board)

assert score > 0

print("[PASS] Black isolated pawn")


# ==========================
# TEST 5: White passed pawn
# ==========================

board = empty_board()

# White pawn on e5.
board.board[3][4] = "P"

score = evaluate_pawn_structure(board)

assert score > 0

print("[PASS] White passed pawn")


# ==========================
# TEST 6: Black passed pawn
# ==========================

board = empty_board()

# Black pawn on e4.
board.board[4][4] = "p"

score = evaluate_pawn_structure(board)

assert score < 0

print("[PASS] Black passed pawn")


print()
print("All pawn-structure tests passed.")