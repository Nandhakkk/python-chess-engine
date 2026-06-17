from board import Board

board = Board()

while True:
    board.display()

    move = input("Enter move (example: e2 e4): ").strip()

    if not move:
        print("Please enter a move")
        continue

    parts = move.split()

    if len(parts) != 2:
        print("Enter moves like: e2 e4")
        continue

    start, end = parts

    board.move_piece(start, end)

    print()