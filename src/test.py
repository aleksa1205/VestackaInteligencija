from src.board_logic.board_utility import get_right_peg, get_bot_right_peg, get_bot_left_peg

def get_end_peg(board_size, start, direction):
    curr_peg = start
    path = [start]

    for i in range(3):
        curr_peg = direction(board_size, curr_peg)
        # if i > (board_size - 1) * 2: return False, False
        # if i < board_size and (j < 0 or j >= board_size + i): return False, False
        # if i >= board_size and (j < 0 or j >= board_size + abs(i - (board_size - 1) * 2)): return False, False
        if not check_index_range(board_size, curr_peg): return False, False
        path.append(curr_peg)

    return tuple(path), curr_peg

def check_index_range(board_size, peg_index):
    i, j = peg_index
    max_i = (board_size - 1) * 2
    max_j_top = board_size + i
    max_j_bot = board_size + abs(i - (board_size - 1) * 2)
    min_j = 0

    if i > max_i: return False

    if i < board_size and (j < min_j or j >= max_j_top): return False
    if i >= board_size and (j < min_j or j >= max_j_bot): return False

    return True

pegs = []
b_size = 8

for i in range(2 * b_size - 1):
    for j in range(2 * b_size - 1 - abs(b_size - 1 - i)):
        pegs.append((i, j))

for peg in pegs:
    print(peg.__str__() + ': ')

    path, end_peg = get_end_peg(b_size, peg, get_right_peg)
    if not path: print('Ne moze desno')

    path, end_peg = get_end_peg(b_size, peg, get_bot_right_peg)
    if not path: print('Ne moze dole desno')

    path, end_peg = get_end_peg(b_size, peg, get_bot_left_peg)
    if not path: print('Ne moze dole levo')

    print()