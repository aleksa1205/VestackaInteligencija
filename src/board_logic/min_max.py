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

def evaluate_board(game_state):
    """
    Enhanced heuristic evaluation for your triangle game AI.
    """
    player1_score = game_state.player_points['player1']
    player2_score = game_state.player_points['player2']

    # Base score difference
    score_diff = player2_score - player1_score

    # Early game termination check
    if hasattr(game_state, "is_game_over") and game_state.is_game_over():
        if player2_score > player1_score:
            return 10000
        elif player1_score > player2_score:
            return -10000
        else:
            return 0

    # Heuristic factors
    potential_triangles_p1 = count_potential_triangles(game_state, 'player1')
    potential_triangles_p2 = count_potential_triangles(game_state, 'player2')

    blocking_value_p1 = count_blocking_opportunities(game_state, 'player1')
    blocking_value_p2 = count_blocking_opportunities(game_state, 'player2')

    center_control_p1 = evaluate_center_control(game_state, 'player1')
    center_control_p2 = evaluate_center_control(game_state, 'player2')

    edge_efficiency_p1 = evaluate_edge_efficiency(game_state, 'player1')
    edge_efficiency_p2 = evaluate_edge_efficiency(game_state, 'player2')

    heuristic_value = (
            score_diff * 100 +
            (potential_triangles_p2 - potential_triangles_p1) * 15 +
            (blocking_value_p2 - blocking_value_p1) * 8 +
            (center_control_p2 - center_control_p1) * 5 +
            (edge_efficiency_p2 - edge_efficiency_p1) * 3
    )

    return heuristic_value


def get_player_edges(game_state, player):
    # If you have a method, use it. Otherwise, extract from graph/paths:
    # Assume game_state.graph is {node: set(connected_nodes)}
    edges = set()
    for node, neighbors in game_state.graph.items():
        for neighbor in neighbors:
            # You may need to check ownership if your graph tracks it
            edge = tuple(sorted((node, neighbor)))
            if edge in game_state.paths and game_state.paths[edge] == player:
                edges.add(edge)
    return list(edges)


def count_potential_triangles(game_state, player):
    """Count triangles that need only 1 more edge to complete."""
    potential_count = 0
    player_edges = get_player_edges(game_state, player)
    all_edges = set(tuple(sorted(edge)) for edge in game_state.graph_edges())
    for i in range(len(player_edges)):
        for j in range(i + 1, len(player_edges)):
            edge1, edge2 = player_edges[i], player_edges[j]
            shared = set(edge1) & set(edge2)
            if len(shared) == 1:
                third = tuple(sorted((set(edge1) | set(edge2)) - shared))
                if third in all_edges and third not in player_edges:
                    potential_count += 1
    return potential_count


def count_blocking_opportunities(game_state, player):
    """Count opportunities to block opponent's triangles."""
    opponent = 'player2' if player == 'player1' else 'player1'
    return count_potential_triangles(game_state, opponent)


def evaluate_center_control(game_state, player):
    """Evaluate control of center positions."""
    # For NxN board, center is all positions with both coordinates in the middle half
    size = game_state.board_size
    margin = size // 4
    center_positions = set(
        (x, y)
        for x in range(margin, size - margin)
        for y in range(margin, size - margin)
    )
    player_edges = get_player_edges(game_state, player)
    control = 0
    for edge in player_edges:
        if any(pos in center_positions for pos in edge):
            control += 1
    return control


def evaluate_edge_efficiency(game_state, player):
    """Evaluate how efficiently edges are placed (reusability for triangles)."""
    player_edges = get_player_edges(game_state, player)
    efficiency_score = 0
    for edge in player_edges:
        triangle_participation = 0
        for other in player_edges:
            if edge != other and len(set(edge) & set(other)) == 1:
                triangle_participation += 1
        efficiency_score += triangle_participation
    return efficiency_score

# Helper to get all possible edges on the board
def graph_edges(game_state):
    # If you have a list of all possible edges, use it.
    # Otherwise, generate from pegs:
    edges = set()
    for node, neighbors in game_state.graph.items():
        for neighbor in neighbors:
            edges.add(tuple(sorted((node, neighbor))))
    return edges
