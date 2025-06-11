def coordinates_to_pixel(board, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    return board.x_start + abs(board.board_size - 1 - x) * board.d / 2 + y * board.d, board.y_start + x * board.h

def get_right_peg(board_size, coordinates):
    return coordinates[0], coordinates[1] + 1

def get_bot_right_peg(board_size, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    return x + 1, y if x >= board_size - 1 else y + 1

def get_bot_left_peg(board_size, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    return x + 1, y - 1 if x >= board_size - 1 else y