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

    for row in board:
        for piece in row:

            if piece in piece_values:
                score += piece_values[piece]

    return score