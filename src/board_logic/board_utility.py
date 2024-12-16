def coordinates_to_pixel(board, coordinates):
    x = coordinates[0]
    y = coordinates[1]
    return board.x_start + abs(board.board_size - 1 - x) * board.d / 2 + y * board.d, board.y_start + x * board.h