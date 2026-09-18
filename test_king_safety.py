from board import Board
from evaluation import evaluate_king_safety


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
# TEST 1: White pawn shield
# ==========================

board = empty_board()

board.board[7][6] = "K"

board.board[6][5] = "P"
board.board[6][6] = "P"
board.board[6][7] = "P"

score = evaluate_king_safety(board)

assert score > 0

print("[PASS] White king pawn shield")


# ==========================
# TEST 2: Black pawn shield
# ==========================

board = empty_board()

board.board[0][6] = "k"

board.board[1][5] = "p"
board.board[1][6] = "p"
board.board[1][7] = "p"

score = evaluate_king_safety(board)

assert score < 0

print("[PASS] Black king pawn shield")


# ==========================
# TEST 3: White castled king
# ==========================

board = empty_board()

board.board[7][6] = "K"

score = evaluate_king_safety(board)

assert score > 0

print("[PASS] White castled king")


# ==========================
# TEST 4: Black castled king
# ==========================

board = empty_board()

board.board[0][6] = "k"

score = evaluate_king_safety(board)

assert score < 0

print("[PASS] Black castled king")


# ==========================
# TEST 5: White exposed king
# ==========================

board = empty_board()

board.board[5][4] = "K"

score = evaluate_king_safety(board)

assert score < 0

print("[PASS] White exposed king")


# ==========================
# TEST 6: Black exposed king
# ==========================

board = empty_board()

board.board[2][4] = "k"

score = evaluate_king_safety(board)

assert score > 0

print("[PASS] Black exposed king")


print()
print("All king-safety tests passed.")