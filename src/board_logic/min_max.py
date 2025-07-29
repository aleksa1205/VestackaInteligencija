from src.board_logic.game_state import GameState
from math import inf

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

# Proceni tablu za heurističku vrednost
def evaluate_board(game_state: GameState):
    player1_score = game_state.player_points['player1']
    player2_score = game_state.player_points['player2']

    # Razlika u poenima
    score_diff = player2_score - player1_score

    # Forsira izlaz iz rekurzije ako je igra gotova
    if game_state.is_game_over():
        if player2_score > player1_score:
            return 10000
        elif player1_score > player2_score:
            return -10000
        else:
            return 0

    # Heuristika
    potential_triangles = count_potential_triangles(game_state)

    center_control = evaluate_center_control(game_state)

    edge_efficiency = evaluate_edge_efficiency(game_state,)

    heuristic_value = (
            score_diff * 100 +
            potential_triangles * 15 +
            center_control * 5 +
            edge_efficiency * 3
    )

    return heuristic_value


# Broji potencijalne trouglice kojima traba samo jedna gumiaca da bi bili formirani
def count_potential_triangles(game_state: GameState):
    potential_count = 0
    all_edges = list(game_state.graph_edges())  # Pretvori u listu zbog indeksiranja
    all_edges_set = set(all_edges)
    for i in range(len(all_edges)):
        for j in range(i + 1, len(all_edges)):
            edge1, edge2 = all_edges[i], all_edges[j]
            shared = set(edge1) & set(edge2)
            if len(shared) == 1:
                third = tuple(sorted((set(edge1) | set(edge2)) - shared))
                if third in all_edges_set and third not in (edge1, edge2):
                    potential_count += 1
    return potential_count // 3  # Svaki trougao se broji 3 puta

# Evaluira kontrolu centra
# Centar je definisan kao sve grane koje u srednjem delu table
def evaluate_center_control(game_state: GameState):
    size = game_state.board_size
    # // deljenje bez ostatka
    margin = size // 4
    center_positions = set(
        (x, y)
        for x in range(margin, size - margin)
        for y in range(margin, size - margin)
    )
    all_edges = game_state.graph_edges()
    control = 0
    for edge in all_edges:
        if any(pos in center_positions for pos in edge):
            control += 1
    return control


# Evaluira efikasnost svih grana (reusability for triangles)
def evaluate_edge_efficiency(game_state):
    all_edges = list(game_state.graph_edges())
    efficiency_score = 0
    for edge in all_edges:
        triangle_participation = 0
        for other in all_edges:
            if edge != other and len(set(edge) & set(other)) == 1:
                triangle_participation += 1
        efficiency_score += triangle_participation
    return efficiency_score
