# min-max logic
from src.board_logic.game_state import GameState
from math import inf

def evaluate_board(game_state: GameState):
    min_points = game_state.player_points['player1']
    max_points = game_state.player_points['player2']
    return max_points - min_points


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