# min-max logic
from src.board_logic.game_state import GameState
from math import inf

def evaluate_board(game_state):
    # Points difference
    points = game_state.player_points['player2'] - game_state.player_points['player1']

    # Triangle difference
    triangles = len(game_state.player_triangles['player2']) - len(game_state.player_triangles['player1'])

    # Mobility (number of possible moves)
    original_player = game_state.current_player
    game_state.current_player = 1
    player1_moves = len(game_state.generate_all_possible_states())
    game_state.current_player = 2
    player2_moves = len(game_state.generate_all_possible_states())
    game_state.current_player = original_player
    mobility = player2_moves - player1_moves

    # Weighted sum (tune these weights as needed)
    return 10 * points + 5 * triangles + 2 * mobility


def max_player(game_state: GameState, depth, alpha, beta):
    best_score = -inf
    best_path = []

    for state in game_state.generate_all_possible_states():
        score, path = minmax(state, depth - 1, alpha, beta, is_max=False)
        if score > best_score:
            best_score = score
            best_path = [state.last_move] + path

        alpha = max(alpha, best_score)

        if beta <= alpha:
            break

    return best_score, best_path


def min_player(game_state: GameState, depth, alpha, beta):
    best_score = inf
    best_path = []

    for state in game_state.generate_all_possible_states():
        score, path = minmax(state, depth - 1, alpha, beta, is_max=True)
        if score < best_score:
            best_score = score
            best_path = [state.last_move] + path

        beta = min(beta, best_score)

        if beta <= alpha:
            break
    return best_score, best_path


def minmax(game_state: GameState, depth, alpha, beta, is_max: bool):
    if depth <= 0:
        return evaluate_board(game_state), []

    if is_max:
        return max_player(game_state, depth, alpha, beta)
    else:
        return min_player(game_state, depth, alpha, beta)