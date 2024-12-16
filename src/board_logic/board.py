from typing import List
import pygame
from math import sqrt

from src.board_logic.ui_elements.board_background import BoardBackground
from src.board_logic.ui_elements.rubber_band_utils import RubberBandUtils
from src.board_logic.ui_elements.triangle_utils import TriangleUtils
from src.ui_components.colors import rubber_band_color, player1_color, player2_color
from src.board_logic.ui_elements.stub import Stub
from src.states.transparent import Transparent

class Board:
    def __init__(self, game, board_size, shared_data):
        self.game = game
        self.board_size = board_size
        self.d = 0
        self.get_d_for_board_size()
        self.h = self.d * sqrt(3) / 2
        self.stub_radius = 6
        self.shared_data = shared_data
        self.x_start = (self.game.SCREEN_WIDTH - (((self.board_size - 1) * 2) * self.d)) / 2
        self.y_start = (self.game.SCREEN_HEIGHT - (((self.board_size - 1) * 2) * self.h)) / 2
        self.y_start = self.y_start if self.board_size < 8 else self.y_start + 50
        self.board_bg = BoardBackground(self)

        # Funckionalnosti
        self.currentPlayer = True
        self.paths = set()
        self.points_to_win = 6 * self.board_size + 3

        # player1 / plavi
        self.player1_set = set()
        self.player1_points = 0

        self.message_start_time = None

        # player2 / ai
        self.player2_set = set()
        self.player2_points = 0

        self.graph = {}
        self.stubovi = []
        self.initialize_stubovi_and_graph()
        self.selected_stubovi : List[Stub] = []

    # Metode klase
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and len(self.selected_stubovi) == 1:
                    self.selected_stubovi[0].reset_clicked()
                    self.selected_stubovi.clear()

        for stub in self.stubovi:
            if stub.check_click(player1_color if self.shared_data['current_player'] else player2_color):
                self.selected_stubovi.append(stub)

        # Izabrana su 2 stuba, znaci odigraj potez
        if len(self.selected_stubovi) == 2:
            self.make_move(self.selected_stubovi[0].index, self.selected_stubovi[1].index)
            self.selected_stubovi[0].reset_clicked()
            self.selected_stubovi[1].reset_clicked()
            self.selected_stubovi.clear()

    def render(self, surface):
        self.board_bg.render(surface)
        for stub in self.stubovi: stub.render()

        RubberBandUtils.draw_rubber_bands(surface, self.paths, self, self.stub_radius, rubber_band_color)
        # crtanje povlacenje gumice
        if len(self.selected_stubovi) == 1:
            mouse_pos = pygame.mouse.get_pos()
            RubberBandUtils.draw_rubber_band(surface, self.selected_stubovi[0].pos, mouse_pos, self.stub_radius, rubber_band_color)

        TriangleUtils.draw_triangles(surface, self)

    # Pomocne funkcije
    def get_d_for_board_size(self):
        if self.board_size == 4: self.d = 60
        elif self.board_size == 5: self.d = 55
        elif self.board_size == 6: self.d = 50
        elif self.board_size == 7: self.d = 43
        elif self.board_size == 8: self.d = 40
        else: self.d = 45

    def initialize_stubovi_and_graph(self):
        for i in range(2 * self.board_size - 1):
            for j in range(2 * self.board_size - 1 - abs(self.board_size - 1 - i)):
                # print(i,j,self.coordinates_to_pixel((i,j)))
                self.stubovi.append(Stub(self.game, (i, j), self.stub_radius, self.board_size, self.d, self.h, self.x_start, self.y_start))
                self.graph[(i, j)] = set()
        self.shared_data['stubovi'] = self.stubovi

    def get_right_peg(self, coordinates):
        return coordinates[0], coordinates[1] + 1

    def get_bot_right_peg(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        return x + 1, y if x >= self.board_size - 1 else y + 1

    def get_bot_left_peg(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        return x + 1, y - 1 if x >= self.board_size - 1 else y

    def get_end_peg(self, start, direction):
        curr_peg = start
        path = [start]

        for i in range(3):
            curr_peg = direction(curr_peg)
            path.append(curr_peg)

        return path, curr_peg

    def make_move(self, start: tuple, end: tuple):
        if self.check_length(start, end) is False:
            new_state = Transparent(self.game, "Rubber band must go through 4 pegs!", self.shared_data)
            new_state.enter_state()
            return

        desni, node_desno = self.get_end_peg(start, self.get_right_peg)
        d_desni, node_d_desno = self.get_end_peg(start, self.get_bot_right_peg)
        d_levi, node_d_levo = self.get_end_peg(start, self.get_bot_left_peg)

        if node_desno == end:
            path = tuple(desni)
            if path in self.paths:
                new_state = Transparent(self.game, "There is already rubber band on those pegs!", self.shared_data)
                new_state.enter_state()
                return
            self.paths.add(path)
            for i, j in zip(desni[:-1], desni[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        elif node_d_levo == end:
            path = tuple(d_levi)
            if path in self.paths:
                new_state = Transparent(self.game, "There is already rubber band on those pegs!", self.shared_data)
                new_state.enter_state()
                return
            self.paths.add(path)
            for i, j in zip(d_levi[:-1], d_levi[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        elif node_d_desno == end:
            path = tuple(d_desni)
            if path in self.paths:
                new_state = Transparent(self.game, "There is already rubber band on those pegs!", self.shared_data)
                new_state.enter_state()
                return
            self.paths.add(path)
            for i, j in zip(d_desni[:-1], d_desni[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        else:
            new_state = Transparent(self.game, "You can only stretch in those directions: Right, Down Right and Down Left", self.shared_data)
            new_state.enter_state()
            return False

        self.shared_data['last_turn'] = (start, end)
        self.find_triangle()
        self.player1_points = len(self.player1_set)
        self.player2_points = len(self.player2_set)
        self.change_player()
        print(self.player1_points, self.player2_points)

        return True

    def is_valid_move(self):
        pass

    def check_length(self, stub1: tuple, stub2: tuple):
        x = abs(stub2[0] - stub1[0])
        y = abs(stub2[1] - stub1[1])
        return True if x == 3 or y == 3 else False

    def find_triangle(self):
        for node in self.graph:
            neighbors = list(self.graph[node])
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if neighbors[j] in self.graph[neighbors[i]]:
                        # prvo proverimo da li je dati ciklus u nekom od setova
                        cycle = tuple(sorted((node, neighbors[i], neighbors[j])))
                        # print(globals.player1_set)
                        # print(globals.player2_set)
                        # print(cycle)
                        if tuple(cycle) not in self.player1_set and tuple(cycle) not in self.player2_set:
                            self.player1_set.add(cycle) if self.shared_data['current_player'] else self.player2_set.add(cycle)

    def change_player(self):
        self.shared_data['current_player'] = not self.shared_data['current_player']
        self.shared_data['change_player_state'] = True