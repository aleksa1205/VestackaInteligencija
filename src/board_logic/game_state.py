class GameState:
    def __init__(self, board_size):

        self.board_size = board_size

        # Koj igrac igra sledeci
        self.current_player = 1

        # Graf se koristi za pronalazenje trouglica. To radi tako sto nadje ciklus izmedju 3 cvora
        self.graph = {}
        self.init_graph()

        # pamti putanju gumica
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
        self.add_path(peg_path)
        self.find_triangles()
        self.update_score()
        self.change_player()
        self.last_move = (peg_path[0], peg_path[3])

    def add_path(self, peg_path):
        self.paths.add(peg_path)
        for i, j in zip(peg_path[:-1], peg_path[1:]):
            self.graph[i].add(j)
            self.graph[j].add(i)

    def find_triangles(self):
        for node in self.graph:
            neighbors = list(self.graph[node])
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in self.graph[neighbors[i]]:
                        # prvo proverimo da li je dati ciklus u nekom od setova
                        cycle = tuple(sorted((node, neighbors[i], neighbors[j])))
                        if tuple(cycle) not in self.player_triangles['player1'] and tuple(cycle) not in self.player_triangles['player2']:
                            self.player_triangles['player1'].add(cycle) if self.current_player == 1 else self.player_triangles['player2'].add(cycle)

    def update_score(self):
        self.player_points['player1'] = len(self.player_triangles['player1'])
        self.player_points['player2'] = len(self.player_triangles['player2'])

    def change_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    # Implementirati ovo
    def get_new_state(self, peg_path):
        pass