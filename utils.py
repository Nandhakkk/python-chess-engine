def chess_to_index(position):

    col = ord(position[0]) - ord("a")
    row = 8 - int(position[1])

    return row, col