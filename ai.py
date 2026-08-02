from utils import index_to_chess

from evaluation import evaluate_board
from validators import copy_board_obj

nodes_searched = 0
def minimax(board_obj, depth, maximizing_player):

    # Base case
    if depth == 0:
        return evaluate_board(board_obj.board)

    color = "white" if maximizing_player else "black"

    legal_moves = generate_legal_moves(board_obj, color)

    if not legal_moves:
        return evaluate_board(board_obj.board)

    if maximizing_player:

        best_score = float("-inf")

        for start, end in legal_moves:

            temp = copy_board_obj(board_obj)
            temp.move_piece(start, end, silent=True)

            score = minimax(
                temp,
                depth - 1,
                False
            )

            best_score = max(best_score, score)

        return best_score

    else:

        best_score = float("inf")

        for start, end in legal_moves:

            temp = copy_board_obj(board_obj)
            temp.move_piece(start, end, silent=True)

            score = minimax(
                temp,
                depth - 1,
                True
            )

            best_score = min(best_score, score)

        return best_score

def order_moves(board_obj, moves):
    """
    Order moves using MVV-LVA.

    MVV-LVA:
    Most Valuable Victim - Least Valuable Attacker

    Capturing valuable pieces with cheaper pieces
    gets searched first.
    """

    piece_values = {
        "p": 100,
        "n": 320,
        "b": 330,
        "r": 500,
        "q": 900,
        "k": 20000,
    }

    scored_moves = []

    for start, end in moves:

        start_row = 8 - int(start[1])
        start_col = ord(start[0]) - ord("a")

        end_row = 8 - int(end[1])
        end_col = ord(end[0]) - ord("a")

        attacker = board_obj.board[start_row][start_col]
        victim = board_obj.board[end_row][end_col]

        score = 0

        # Capture
        if victim != ".":
            victim_value = piece_values[victim.lower()]
            attacker_value = piece_values[attacker.lower()]

            score = (
                10 * victim_value
                - attacker_value
            )

        scored_moves.append(
            (score, (start, end))
        )

    scored_moves.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        move
        for score, move in scored_moves
    ]
def alphabeta(board_obj, depth, alpha, beta, maximizing_player):
    global nodes_searched
    nodes_searched += 1 
    if depth == 0:
        return evaluate_board(board_obj.board)

    color = "white" if maximizing_player else "black"

    legal_moves = generate_legal_moves(board_obj, color)

    legal_moves = order_moves(board_obj, legal_moves)

    if not legal_moves:
        return evaluate_board(board_obj.board)

    if maximizing_player:

        value = float("-inf")

        for start, end in legal_moves:

            temp = copy_board_obj(board_obj)
            temp.move_piece(start, end, silent=True)

            score = alphabeta(
                temp,
                depth - 1,
                alpha,
                beta,
                False
            )

            value = max(value, score)
            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:

        value = float("inf")

        for start, end in legal_moves:

            temp = copy_board_obj(board_obj)
            temp.move_piece(start, end, silent=True)

            score = alphabeta(
                temp,
                depth - 1,
                alpha,
                beta,
                True
            )

            value = min(value, score)
            beta = min(beta, value)

            if beta <= alpha:
                break

        return value

def generate_legal_moves(board_obj, color):

    legal_moves = []

    # Scan every square
    for start_row in range(8):
        for start_col in range(8):

            piece = board_obj.board[start_row][start_col]

            if piece == ".":
                continue

            # Only consider pieces of the requested color
            if color == "white" and piece.islower():
                continue

            if color == "black" and piece.isupper():
                continue

            # Try every destination square
            for end_row in range(8):
                for end_col in range(8):

                    if start_row == end_row and start_col == end_col:
                        continue

                    target = board_obj.board[end_row][end_col]

                    # Can't capture your own piece
                    if target != ".":

                        if piece.isupper() and target.isupper():
                            continue

                        if piece.islower() and target.islower():
                            continue

                    # Use your existing move validator
                    if not board_obj.is_valid_move_for_piece(
                        piece,
                        start_row,
                        start_col,
                        end_row,
                        end_col
                    ):
                        continue

                    # Reject moves that leave the king in check
                    if board_obj.would_leave_king_in_check(
                        start_row,
                        start_col,
                        end_row,
                        end_col
                    ):
                        continue

                    start = index_to_chess(start_row, start_col)
                    end = index_to_chess(end_row, end_col)

                    legal_moves.append((start, end))

    return legal_moves

def choose_best_move(board_obj, color, depth=3):

    legal_moves = generate_legal_moves(board_obj, color)

    if not legal_moves:
        return None

    best_move = None

    if color == "white":

        best_score = float("-inf")

        for start, end in legal_moves:

            temp = copy_board_obj(board_obj)
            temp.move_piece(start, end, silent=True)

            score = alphabeta(
                temp,
                depth - 1,
                float("-inf"),
                float("inf"),
                False
            )

            if score > best_score:
                best_score = score
                best_move = (start, end)

    else:

        best_score = float("inf")

        for start, end in legal_moves:

            temp = copy_board_obj(board_obj)
            temp.move_piece(start, end, silent=True)

            score = alphabeta(
                temp,
                depth - 1,
                float("-inf"),
                float("inf"),
                True
            )

            if score < best_score:
                best_score = score
                best_move = (start, end)

    return best_move