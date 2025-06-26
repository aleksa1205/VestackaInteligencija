import copy

from src.board_logic.board_utility import get_right_peg, get_bot_left_peg, get_bot_right_peg


# TODO
# 1. funkcija koja generise stablo za sve poteze dubine N (generate_graph_state)
# 2. min i max funkcija
# 3. min-max funkcija
# 4. alpha-beta pruning
# 5. ako je mnogo sporo optimizacija
# 6. refactor

# min max function params: board/board size, depth, isMax, score, deltaScore


class GameState:
    def __init__(self, board_size, peg_indexes, current_player):

        self.board_size = board_size
        self.peg_indexes = peg_indexes

        # Koj igrac igra sledeci
        self.current_player = current_player

        # Graf se koristi za pronalazenje trouglica. To radi tako sto nadje ciklus izmedju 3 cvora
        self.graph = {}
        self.init_graph()

        # pamti putanju gumica 3211
        self.paths = set()

        # Koliko poena je potrebno za pobedu igraca
        self.points_to_win = 6 * board_size + 3

        # Indeksi izmedju kojih je formiran trouglic, pamti se za oba igraca
        self.player_triangles = {
            'player1': set(),
            'player2': set()
        }

        # Broj poena svakog igraca
        self.player_points = {
            'player1': 0,
            'player2': 0
        }

        # Pamti zadnje odigran potez
        self.last_move = tuple()

    def init_graph(self):
        for i in range(2 * self.board_size - 1):
            for j in range(2 * self.board_size - 1 - abs(self.board_size - 1 - i)):
                self.graph[(i, j)] = set()

    def update_state(self, peg_path):
        GameState.__add_path(self, peg_path)
        GameState.__find_triangles(self)
        GameState.__update_score(self)
        GameState.__change_player(self)
        self.last_move = (peg_path[0], peg_path[3])

    # Menja game state ali sa kopijem instance i vraca izmenjenu verziju
    # Mora ovo da se optimizuje jer deepcopy je jako skupa operacija pogotovo ako se provlaci kroz veliku petlju
    # (n - 1) * 3 max
    def get_new_state(self, peg_path):
        g_state_copy = copy.deepcopy(self)

        GameState.__add_path(g_state_copy, peg_path)
        GameState.__find_triangles(g_state_copy)
        GameState.__update_score(g_state_copy)
        # GameState.__change_player(g_state_copy)
        g_state_copy.last_move = (peg_path[0], peg_path[3])

        return g_state_copy

    def generate_all_possible_states(self):
        all_moves = []

        # proveri da li path postoji, mozda ovde da se prebaci
        for peg_index in self.peg_indexes:
            self.__add_new_state(peg_index, get_right_peg, all_moves)
            self.__add_new_state(peg_index, get_bot_left_peg, all_moves)
            self.__add_new_state(peg_index, get_bot_right_peg, all_moves)

        return all_moves
        # self.all_possible_moves = all_moves

    def __add_new_state(self, start, direction, all_moves):
        path = self.__get_valid_peg_path(self.board_size, start, direction)
        if path and path not in self.paths:
            new_state = self.get_new_state(path)
            all_moves.append(new_state)

    @staticmethod
    def __get_valid_peg_path(board_size, start, direction):
        curr_peg = start
        path = [start]

        for i in range(3):
            curr_peg = direction(board_size, curr_peg)
            if not GameState.__check_index_range(board_size, curr_peg): return False

            path.append(curr_peg)

        return tuple(path)

    @staticmethod
    def __check_index_range(board_size, peg_index):
        i, j = peg_index
        max_i = (board_size - 1) * 2
        max_j_top = board_size + i
        max_j_bot = board_size + abs(i - (board_size - 1) * 2)
        min_j = 0

        if i > max_i: return False

        if i < board_size and (j < min_j or j >= max_j_top): return False
        if i >= board_size and (j < min_j or j >= max_j_bot): return False

        return True

    @staticmethod
    def __add_path(g_state, peg_path):
        g_state.paths.add(peg_path)
        for i, j in zip(peg_path[:-1], peg_path[1:]):
            g_state.graph[i].add(j)
            g_state.graph[j].add(i)

    @staticmethod
    def __find_triangles(g_state):
        for node in g_state.graph:
            neighbors = list(g_state.graph[node])
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in g_state.graph[neighbors[i]]:
                        # prvo proverimo da li je dati ciklus u nekom od setova
                        cycle = tuple(sorted((node, neighbors[i], neighbors[j])))
                        if tuple(cycle) not in g_state.player_triangles['player1'] and tuple(cycle) not in \
                                g_state.player_triangles['player2']:
                            g_state.player_triangles['player1'].add(cycle) if g_state.current_player == 1 else \
                            g_state.player_triangles['player2'].add(cycle)

    @staticmethod
    def __update_score(g_state):
        g_state.player_points['player1'] = len(g_state.player_triangles['player1'])
        g_state.player_points['player2'] = len(g_state.player_triangles['player2'])

    @staticmethod
    def __change_player(g_state):
        g_state.current_player = 2 if g_state.current_player == 1 else 1
