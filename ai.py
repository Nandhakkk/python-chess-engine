from utils import index_to_chess

from evaluation import evaluate_board
from validators import copy_board_obj
from zobrist import compute_zobrist_hash
import time
nodes_searched = 0
transposition_table = {}
tt_hits = 0

killer_moves = {}
history_scores = {}

TT_EXACT = 0
TT_LOWERBOUND = 1
TT_UPPERBOUND = 2

class SearchTimeout(Exception):
    pass

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
    Order moves using:

    1. Captures → MVV-LVA
    2. Quiet moves → History Heuristic
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

        # -------------------------
        # Capture: MVV-LVA
        # -------------------------

        if victim != ".":

            victim_value = (
                piece_values[victim.lower()]
            )

            attacker_value = (
                piece_values[attacker.lower()]
            )

            score = (
                10 * victim_value
                - attacker_value
            )

        # -------------------------
        # Quiet move: History
        # -------------------------

        else:

            score = history_scores.get(
                (start, end),
                0
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

def quiescence(
    board_obj,
    alpha,
    beta,
    maximizing_player,
    q_depth=4
):
    """
    Continue searching tactical capture moves after
    the normal search depth reaches zero.

    This helps reduce the horizon effect.
    """

    global nodes_searched
    nodes_searched += 1

    stand_pat = evaluate_board(board_obj.board)
    # Prevent quiescence search from becoming too deep
    if q_depth == 0:
        return stand_pat
    # White is maximizing
    if maximizing_player:

        if stand_pat >= beta:
            return beta

        if stand_pat > alpha:
            alpha = stand_pat

    # Black is minimizing
    else:

        if stand_pat <= alpha:
            return alpha

        if stand_pat < beta:
            beta = stand_pat

    color = "white" if maximizing_player else "black"

    legal_moves = generate_legal_moves(
        board_obj,
        color
    )

    # Keep useful captures only
    capture_moves = []

    piece_values = {
        "p": 100,
        "n": 320,
        "b": 330,
        "r": 500,
        "q": 900,
        "k": 20000,
    }

    for start, end in legal_moves:

        start_row = 8 - int(start[1])
        start_col = ord(start[0]) - ord("a")

        end_row = 8 - int(end[1])
        end_col = ord(end[0]) - ord("a")

        attacker = board_obj.board[start_row][start_col]
        victim = board_obj.board[end_row][end_col]

        if victim == ".":
            continue

        attacker_value = piece_values[attacker.lower()]
        victim_value = piece_values[victim.lower()]

        # Search captures where the victim is at least
        # as valuable as the attacking piece.
        if victim_value >= attacker_value:
            capture_moves.append((start, end))

    # Search valuable captures first
    capture_moves = order_moves(
        board_obj,
        capture_moves
    )

    if maximizing_player:

        for start, end in capture_moves:

            temp = copy_board_obj(board_obj)

            temp.move_piece(
                start,
                end,
                silent=True
            )

            score = quiescence(
                temp,
                alpha,
                beta,
                False,
                q_depth - 1
            )

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        return alpha

    else:

        for start, end in capture_moves:

            temp = copy_board_obj(board_obj)

            temp.move_piece(
                start,
                end,
                silent=True
            )

            score = quiescence(
                temp,
                alpha,
                beta,
                True,
                q_depth - 1
            )

            if score <= alpha:
                return alpha

            if score < beta:
                beta = score

        return beta

def get_position_key(board_obj, maximizing_player):
    """
    Create a compact position key using
    64-bit Zobrist hashing.
    """

    zobrist_hash = compute_zobrist_hash(board_obj)

    return (
        zobrist_hash,
        maximizing_player
    )


def get_ordered_moves_with_killers(
    board_obj,
    legal_moves,
    depth,
    tt_move=None
):
    """
    Order moves using:

    1. TT best move
    2. Killer moves
    3. MVV-LVA / History Heuristic
    """

    moves = order_moves(
        board_obj,
        legal_moves
    )

    # -------------------------
    # TT best move
    # -------------------------

    if tt_move is not None and tt_move in moves:

        moves.remove(tt_move)
        moves.insert(0, tt_move)

    # -------------------------
    # Killer moves
    # -------------------------

    killers = killer_moves.get(
        depth,
        []
    )

    for killer in reversed(killers):

        if killer in moves:

            moves.remove(killer)
            moves.insert(0, killer)

    # Make sure TT move remains first
    if tt_move is not None and tt_move in moves:

        moves.remove(tt_move)
        moves.insert(0, tt_move)

    return moves
def alphabeta(
    board_obj,
    depth,
    alpha,
    beta,
    maximizing_player
):

    global nodes_searched
    global tt_hits

    if time.time() >= search_deadline:
        raise SearchTimeout

    nodes_searched += 1

    # -------------------------
    # Save original alpha/beta
    # -------------------------

    original_alpha = alpha
    original_beta = beta

    # -------------------------
    # Position key
    # -------------------------

    key = get_position_key(
        board_obj,
        maximizing_player
    )

    # -------------------------
    # Transposition Table lookup
    # -------------------------

    tt_move = None

    if key in transposition_table:

        (
            stored_depth,
            stored_score,
            stored_flag,
            stored_best_move
        ) = transposition_table[key]

        # Always retrieve the stored best move
        if stored_best_move is not None:
            tt_move = stored_best_move

        # Use stored score only if
        # searched deeply enough
        if stored_depth >= depth:

            if stored_flag == TT_EXACT:

                tt_hits += 1

                return stored_score

            elif stored_flag == TT_LOWERBOUND:

                alpha = max(
                    alpha,
                    stored_score
                )

            elif stored_flag == TT_UPPERBOUND:

                beta = min(
                    beta,
                    stored_score
                )

            # Bound caused a cutoff
            if alpha >= beta:

                tt_hits += 1

                return stored_score

    # -------------------------
    # Quiescence search
    # -------------------------

    if depth == 0:

        return quiescence(
            board_obj,
            alpha,
            beta,
            maximizing_player
        )

    # -------------------------
    # Generate legal moves
    # -------------------------

    color = (
        "white"
        if maximizing_player
        else "black"
    )

    legal_moves = generate_legal_moves(
        board_obj,
        color
    )

    if not legal_moves:

        return evaluate_board(
            board_obj.board
        )

    # -------------------------
    # Move ordering
    # -------------------------

    legal_moves = get_ordered_moves_with_killers(
        board_obj,
        legal_moves,
        depth,
        tt_move
    )

    # -------------------------
    # Maximizing player
    # -------------------------

    if maximizing_player:

        value = float("-inf")
        best_move = None

        for start, end in legal_moves:

            temp = copy_board_obj(
                board_obj
            )

            temp.move_piece(
                start,
                end,
                silent=True
            )

            score = alphabeta(
                temp,
                depth - 1,
                alpha,
                beta,
                False
            )

            # Found a better move
            if score > value:

                value = score

                best_move = (
                    start,
                    end
                )

            alpha = max(
                alpha,
                value
            )

            # -------------------------
            # Beta cutoff
            # -------------------------

            if alpha >= beta:

                move = (
                    start,
                    end
                )

                # Killer move
                if move not in killer_moves.get(
                    depth,
                    []
                ):

                    killer_moves.setdefault(
                        depth,
                        []
                    ).insert(
                        0,
                        move
                    )

                    killer_moves[depth] = (
                        killer_moves[depth][:2]
                    )

                # History heuristic
                history_scores[
                    move
                ] = (
                    history_scores.get(
                        move,
                        0
                    )
                    + depth * depth
                )

                break

    # -------------------------
    # Minimizing player
    # -------------------------

    else:

        value = float("inf")
        best_move = None

        for start, end in legal_moves:

            temp = copy_board_obj(
                board_obj
            )

            temp.move_piece(
                start,
                end,
                silent=True
            )

            score = alphabeta(
                temp,
                depth - 1,
                alpha,
                beta,
                True
            )

            # Found a better move
            if score < value:

                value = score

                best_move = (
                    start,
                    end
                )

            beta = min(
                beta,
                value
            )

            # -------------------------
            # Alpha cutoff
            # -------------------------

            if beta <= alpha:

                move = (
                    start,
                    end
                )

                # Killer move
                if move not in killer_moves.get(
                    depth,
                    []
                ):

                    killer_moves.setdefault(
                        depth,
                        []
                    ).insert(
                        0,
                        move
                    )

                    killer_moves[depth] = (
                        killer_moves[depth][:2]
                    )

                # History heuristic
                history_scores[
                    move
                ] = (
                    history_scores.get(
                        move,
                        0
                    )
                    + depth * depth
                )

                break

    # -------------------------
    # Determine TT flag
    # -------------------------

    if value <= original_alpha:

        flag = TT_UPPERBOUND

    elif value >= original_beta:

        flag = TT_LOWERBOUND

    else:

        flag = TT_EXACT

    # -------------------------
    # Store in TT
    # -------------------------

    transposition_table[key] = (
        depth,
        value,
        flag,
        best_move
    )

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

def choose_best_move(
    board_obj,
    color,
    depth=3,
    time_limit=5.0
):

    global nodes_searched
    global search_deadline

    legal_moves = generate_legal_moves(
        board_obj,
        color
    )

    if not legal_moves:
        return None

    # -------------------------
    # Search setup
    # -------------------------

    best_move = legal_moves[0]

    depth_nodes = {}

    # Set search deadline
    search_deadline = (
        time.time() + time_limit
    )

    # -------------------------
    # Iterative deepening
    # -------------------------

    for current_depth in range(
        1,
        depth + 1
    ):

        print(
            f"Searching depth "
            f"{current_depth}..."
        )

        nodes_before = nodes_searched

        current_best_move = None

        try:

            # -------------------------
            # Root move ordering
            # -------------------------

            ordered_moves = (
                legal_moves.copy()
            )

            # Previous iteration's best
            # move goes first.
            if (
                best_move is not None
                and best_move in ordered_moves
            ):

                ordered_moves.remove(
                    best_move
                )

                ordered_moves.insert(
                    0,
                    best_move
                )

            # -------------------------
            # Search current depth
            # -------------------------

            if color == "white":

                best_score = float("-inf")

                for start, end in ordered_moves:

                    temp = copy_board_obj(
                        board_obj
                    )

                    temp.move_piece(
                        start,
                        end,
                        silent=True
                    )

                    score = alphabeta(
                        temp,
                        current_depth - 1,
                        float("-inf"),
                        float("inf"),
                        False
                    )

                    if score > best_score:

                        best_score = score

                        current_best_move = (
                            start,
                            end
                        )

            else:

                best_score = float("inf")

                for start, end in ordered_moves:

                    temp = copy_board_obj(
                        board_obj
                    )

                    temp.move_piece(
                        start,
                        end,
                        silent=True
                    )

                    score = alphabeta(
                        temp,
                        current_depth - 1,
                        float("-inf"),
                        float("inf"),
                        True
                    )

                    if score < best_score:

                        best_score = score

                        current_best_move = (
                            start,
                            end
                        )

        except SearchTimeout:

            print(
                f"Time limit reached "
                f"during depth {current_depth}."
            )

            break

        # -------------------------
        # Completed depth
        # -------------------------

        nodes_for_depth = (
            nodes_searched
            - nodes_before
        )

        depth_nodes[
            current_depth
        ] = nodes_for_depth

        print(
            f"Depth {current_depth} nodes: "
            f"{nodes_for_depth}"
        )

        # IMPORTANT:
        # Only accept a move from a
        # completely finished depth.
        if current_best_move is not None:

            best_move = (
                current_best_move
            )

        print(
            f"Depth {current_depth}: "
            f"{best_move}"
        )

    return best_move