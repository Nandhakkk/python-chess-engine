def is_valid_knight_move(start_row, start_col, end_row, end_col):

    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)

    return (
        (row_diff == 2 and col_diff == 1)
        or
        (row_diff == 1 and col_diff == 2)
    )

def is_valid_pawn_move(
    board,
    start_row,
    start_col,
    end_row,
    end_col
):

    piece = board[start_row][start_col]

    # White pawn
    if piece == "P":

        if start_col == end_col:

            if end_row == start_row - 1:
                if board[end_row][end_col] == ".":
                    return True

            if start_row == 6 and end_row == 4:
                if (
                    board[5][start_col] == "."
                    and board[4][start_col] == "."
                ):
                    return True

        if end_row == start_row - 1 and abs(end_col - start_col) == 1:

            target = board[end_row][end_col]

            if target != "." and target.islower():
                return True

    # Black pawn
    elif piece == "p":

        if start_col == end_col:

            if end_row == start_row + 1:
                if board[end_row][end_col] == ".":
                    return True

            if start_row == 1 and end_row == 3:
                if (
                    board[2][start_col] == "."
                    and board[3][start_col] == "."
                ):
                    return True

        if end_row == start_row + 1 and abs(end_col - start_col) == 1:

            target = board[end_row][end_col]

            if target != "." and target.isupper():
                return True

    return False
def is_valid_bishop_move(
    board,
    start_row,
    start_col,
    end_row,
    end_col
):

    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)

    if row_diff != col_diff:
        return False

    row_step = 1 if end_row > start_row else -1
    col_step = 1 if end_col > start_col else -1

    current_row = start_row + row_step
    current_col = start_col + col_step

    while current_row != end_row:

        if board[current_row][current_col] != ".":
            return False

        current_row += row_step
        current_col += col_step

    return True
def is_valid_rook_move(
    board,
    start_row,
    start_col,
    end_row,
    end_col
):

    # Must move in a straight line
    if start_row != end_row and start_col != end_col:
        return False

    # Vertical movement
    if start_col == end_col:

        step = 1 if end_row > start_row else -1

        current_row = start_row + step

        while current_row != end_row:

            if board[current_row][start_col] != ".":
                return False

            current_row += step

    # Horizontal movement
    if start_row == end_row:

        step = 1 if end_col > start_col else -1

        current_col = start_col + step

        while current_col != end_col:

            if board[start_row][current_col] != ".":
                return False

            current_col += step

    return True