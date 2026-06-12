from board import Board

board = Board()

while True:
    board.display()

    move = input("Enter move (example: e2 e4): ")

    start, end = move.split()

    board.move_piece(start, end)

    print()