def chess_to_index(position):

    col = ord(position[0]) - ord("a")
    row = 8 - int(position[1])

    return row, col

def index_to_chess(row, col):

    file = chr(col + ord("a"))
    rank = str(8 - row)

    return file + rank