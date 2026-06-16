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