from board import Board
from ai import choose_best_move
import time
import ai
board = Board()

print("===================================")
print("      Python Chess Engine")
print("===================================")
print("You are White.")
print("AI is Black.")
print("Type 'quit' to exit.\n")

while True:

    board.display()

    # ------------------------
    # Human (White)
    # ------------------------
    if board.turn == "white":

        move = input("Enter your move (example: e2 e4): ").strip()

        if move.lower() == "quit":
            print("Goodbye!")
            break

        parts = move.split()

        if len(parts) != 2:
            print("Enter moves like: e2 e4")
            continue

        start, end = parts

        try:
            result = board.move_piece(start, end)

            if result == "checkmate":
                board.display()
                print("Checkmate!")
                break

            if result == "stalemate":
                board.display()
                print("Stalemate!")
                break

        except Exception as e:
            print("Error:", e)

    # ------------------------
    # AI (Black)
    # ------------------------
    else:

        print("\nAI is thinking...")

        ai.nodes_searched = 0

        ai.tt_hits = 0
        ai.transposition_table.clear()

        start_time = time.time()

        best = choose_best_move(
            board,
            board.turn,
            depth=10,
            time_limit=5.0
        )

        end_time = time.time()

        print("Nodes searched:", ai.nodes_searched)
        print("TT hits:", ai.tt_hits)
        print("TT entries:", len(ai.transposition_table))
        print(f"Search time: {end_time - start_time:.3f} seconds")
        if best is None:
            print("AI has no legal moves.")
            break

        start, end = best

        print(f"AI plays: {start} {end}")

        try:
            result = board.move_piece(start, end, silent=True)

            if result == "checkmate":
                board.display()
                print("Checkmate!")
                break

            if result == "stalemate":
                board.display()
                print("Stalemate!")
                break

        except Exception as e:
            print("AI Error:", e)

        print()