from board import Board


def print_result(name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")


def test_white_kingside():
    board = Board()

    board.board[7][5] = "."
    board.board[7][6] = "."

    board.turn = "white"

    result = board.move_piece("e1", "g1", silent=True)

    print_result(
        "White Kingside Castling",
        result is True
    )


def test_white_queenside():
    board = Board()

    board.board[7][1] = "."
    board.board[7][2] = "."
    board.board[7][3] = "."

    board.turn = "white"

    result = board.move_piece("e1", "c1", silent=True)

    print_result(
        "White Queenside Castling",
        result is True
    )


def test_black_kingside():
    board = Board()

    board.board[0][5] = "."
    board.board[0][6] = "."

    board.turn = "black"

    result = board.move_piece("e8", "g8", silent=True)

    print_result(
        "Black Kingside Castling",
        result is True
    )


def test_black_queenside():
    board = Board()

    board.board[0][1] = "."
    board.board[0][2] = "."
    board.board[0][3] = "."

    board.turn = "black"

    result = board.move_piece("e8", "c8", silent=True)

    print_result(
        "Black Queenside Castling",
        result is True
    )


if __name__ == "__main__":
    print("===== CASTLING TESTS =====\n")

    test_white_kingside()
    test_white_queenside()
    test_black_kingside()
    test_black_queenside()