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


def get_piece_mobility(board_obj, color):

    board = board_obj.board

    mobility = {
        "p": 0,
        "n": 0,
        "b": 0,
        "r": 0,
        "q": 0,
        "k": 0,
    }

    for row in range(8):
        for col in range(8):

            piece = board[row][col]

            if piece == ".":
                continue

            if color == "white" and piece.islower():
                continue

            if color == "black" and piece.isupper():
                continue

            piece_type = piece.lower()

            # Reuse the optimized move-generation logic
            # from your current mobility function.

            if piece_type == "p":

                direction = -1 if piece == "P" else 1
                new_row = row + direction

                if 0 <= new_row < 8:

                    if board[new_row][col] == ".":
                        mobility["p"] += 1

                        starting_row = (
                            6 if piece == "P" else 1
                        )

                        if row == starting_row:

                            two_row = row + 2 * direction

                            if (
                                0 <= two_row < 8
                                and board[two_row][col] == "."
                            ):
                                mobility["p"] += 1

                    for dc in (-1, 1):

                        new_col = col + dc

                        if not (
                            0 <= new_col < 8
                            and 0 <= new_row < 8
                        ):
                            continue

                        target = board[
                            new_row
                        ][
                            new_col
                        ]

                        if target != ".":

                            if (
                                piece == "P"
                                and target.islower()
                            ):
                                mobility["p"] += 1

                            elif (
                                piece == "p"
                                and target.isupper()
                            ):
                                mobility["p"] += 1

                        elif (
                            board_obj.en_passant_target
                            == (new_row, new_col)
                        ):
                            mobility["p"] += 1

            elif piece_type == "n":

                offsets = [
                    (-2, -1), (-2, 1),
                    (-1, -2), (-1, 2),
                    (1, -2), (1, 2),
                    (2, -1), (2, 1),
                ]

                for dr, dc in offsets:

                    new_row = row + dr
                    new_col = col + dc

                    if not (
                        0 <= new_row < 8
                        and 0 <= new_col < 8
                    ):
                        continue

                    target = board[
                        new_row
                    ][
                        new_col
                    ]

                    if target == ".":
                        mobility["n"] += 1

                    elif (
                        piece.isupper()
                        and target.islower()
                    ):
                        mobility["n"] += 1

                    elif (
                        piece.islower()
                        and target.isupper()
                    ):
                        mobility["n"] += 1

            elif piece_type in ("b", "r", "q"):

                if piece_type == "b":
                    directions = [
                        (-1, -1), (-1, 1),
                        (1, -1), (1, 1),
                    ]

                elif piece_type == "r":
                    directions = [
                        (-1, 0), (1, 0),
                        (0, -1), (0, 1),
                    ]

                else:
                    directions = [
                        (-1, -1), (-1, 1),
                        (1, -1), (1, 1),
                        (-1, 0), (1, 0),
                        (0, -1), (0, 1),
                    ]

                for dr, dc in directions:

                    new_row = row + dr
                    new_col = col + dc

                    while (
                        0 <= new_row < 8
                        and 0 <= new_col < 8
                    ):

                        target = board[
                            new_row
                        ][
                            new_col
                        ]

                        if target == ".":
                            mobility[piece_type] += 1

                        else:

                            if (
                                piece.isupper()
                                and target.islower()
                            ):
                                mobility[piece_type] += 1

                            elif (
                                piece.islower()
                                and target.isupper()
                            ):
                                mobility[piece_type] += 1

                            break

                        new_row += dr
                        new_col += dc

            elif piece_type == "k":

                offsets = [
                    (-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1),
                ]

                for dr, dc in offsets:

                    new_row = row + dr
                    new_col = col + dc

                    if not (
                        0 <= new_row < 8
                        and 0 <= new_col < 8
                    ):
                        continue

                    target = board[
                        new_row
                    ][
                        new_col
                    ]

                    if target == ".":
                        mobility["k"] += 1

                    elif (
                        piece.isupper()
                        and target.islower()
                    ):
                        mobility["k"] += 1

                    elif (
                        piece.islower()
                        and target.isupper()
                    ):
                        mobility["k"] += 1

    return mobility


def evaluate_pawn_structure(board_obj):

    board = board_obj.board
    score = 0

    # ==========================
    # Pawn files
    # ==========================

    white_pawn_files = [0] * 8
    black_pawn_files = [0] * 8

    for row in range(8):
        for col in range(8):

            piece = board[row][col]

            if piece == "P":
                white_pawn_files[col] += 1

            elif piece == "p":
                black_pawn_files[col] += 1

    # ==========================
    # Doubled pawns
    # ==========================

    for col in range(8):

        if white_pawn_files[col] > 1:
            extra = white_pawn_files[col] - 1
            score -= 10 * extra

        if black_pawn_files[col] > 1:
            extra = black_pawn_files[col] - 1
            score += 10 * extra

    # ==========================
    # Isolated pawns
    # ==========================

    for col in range(8):

        if white_pawn_files[col] > 0:

            left_has_pawn = (
                col > 0
                and white_pawn_files[col - 1] > 0
            )

            right_has_pawn = (
                col < 7
                and white_pawn_files[col + 1] > 0
            )

            if not left_has_pawn and not right_has_pawn:
                score -= 10

        if black_pawn_files[col] > 0:

            left_has_pawn = (
                col > 0
                and black_pawn_files[col - 1] > 0
            )

            right_has_pawn = (
                col < 7
                and black_pawn_files[col + 1] > 0
            )

            if not left_has_pawn and not right_has_pawn:
                score += 10

    # ==========================
    # Passed pawns
    # ==========================

    for row in range(8):
        for col in range(8):

            # --------------------------
            # White pawn
            # --------------------------

            if board[row][col] == "P":

                passed = True

                # Black pawns must not exist
                # ahead on the same or adjacent files.
                for check_col in range(
                    max(0, col - 1),
                    min(8, col + 2)
                ):

                    for check_row in range(0, row):

                        if board[
                            check_row
                        ][
                            check_col
                        ] == "p":

                            passed = False
                            break

                    if not passed:
                        break

                if passed:
                    score += 20

            # --------------------------
            # Black pawn
            # --------------------------

            elif board[row][col] == "p":

                passed = True

                # White pawns must not exist
                # ahead on the same or adjacent files.
                for check_col in range(
                    max(0, col - 1),
                    min(8, col + 2)
                ):

                    for check_row in range(
                        row + 1,
                        8
                    ):

                        if board[
                            check_row
                        ][
                            check_col
                        ] == "P":

                            passed = False
                            break

                    if not passed:
                        break

                if passed:
                    score -= 20

    return score


def evaluate_board(board_obj):

    board = board_obj.board

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

    # ==========================
    # MOBILITY
    # ==========================

    white_mobility = get_piece_mobility(
        board_obj,
        "white"
    )

    black_mobility = get_piece_mobility(
        board_obj,
        "black"
    )

    mobility_weights = {
        "p": 1,
        "n": 4,
        "b": 4,
        "r": 2,
        "q": 1,
        "k": 1,
    }

    mobility_score = 0

    for piece_type, weight in mobility_weights.items():

        mobility_score += (
            white_mobility[piece_type]
            * weight
        )

        mobility_score -= (
            black_mobility[piece_type]
            * weight
        )

    score += mobility_score
    # ==========================
    # PAWN STRUCTURE
    # ==========================

    score += evaluate_pawn_structure(
        board_obj
    )

    return score