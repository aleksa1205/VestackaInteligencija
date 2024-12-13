from typing import Tuple, List
import pygame
from math import sqrt
from src.ui_components.colors import rubber_band_color, player1_color, player2_color, neutral_color_900, \
    neutral_color_800, neutral_color_700, neutral_color_500, neutral_color_100, blue_color_300, blue_color_400
from src.ui_components.stub import Stub
from src.states.transparent import Transparent
from math import sin, cos

class Board:
    def __init__(self, game, board_size, shared_data):
        self.game = game
        self.board_size = board_size
        self.d = 50 if self.board_size < 8 else 43
        self.h = self.d * sqrt(3) / 2
        self.stub_radius = 6
        self.rubber_band_color = rubber_band_color
        self.rubber_band_width = 3
        self.shared_data = shared_data
        self.board_bg_color = neutral_color_800
        # self.hex_width = ((self.board_size - 1) * 2) * self.d
        # self.hex_height = ((self.board_size - 1) * 2) * self.h
        self.x_start = (self.game.SCREEN_WIDTH - (((self.board_size - 1) * 2) * self.d)) / 2
        self.y_start = (self.game.SCREEN_HEIGHT - (((self.board_size - 1) * 2) * self.h)) / 2
        self.y_start = self.y_start if self.board_size < 8 else self.y_start + 50
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
            if stub.check_click():
                self.selected_stubovi.append(stub)

        # Izabrana su 2 stuba, znaci odigraj potez
        if len(self.selected_stubovi) == 2:
            self.make_move(self.selected_stubovi[0].index, self.selected_stubovi[1].index)
            self.selected_stubovi[0].reset_clicked()
            self.selected_stubovi[1].reset_clicked()
            self.selected_stubovi.clear()

    def render(self):
        self.draw_board_bg(25)
        for stub in self.stubovi: stub.render()
        self.draw_rubber_bands()

        # crtanje povlacenje gumice
        if len(self.selected_stubovi) == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_rubber_band(self.selected_stubovi[0].pos, mouse_pos)

        self.draw_triangles()

    # Pomocne funkcije
    def initialize_stubovi_and_graph(self):
        for i in range(2 * self.board_size - 1):
            for j in range(2 * self.board_size - 1 - abs(self.board_size - 1 - i)):
                # print(i,j,self.coordinates_to_pixel((i,j)))
                self.stubovi.append(Stub(self.game, (i, j), self.stub_radius, self.board_size, self.d, self.h, self.x_start, self.y_start))
                self.graph[(i, j)] = set()
        self.shared_data['stubovi'] = self.stubovi

    def coordinates_to_pixel(self, coordinates : Tuple):
        x = coordinates[0]
        y = coordinates[1]
        return self.x_start + abs(self.board_size - 1 - x) * self.d / 2 + y * self.d, self.y_start + x * self.h

    def draw_rubber_band(self, start_pos, end_pos, draw_circles = True):
        """Draw a hollow, bordered line between two points."""
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = sqrt(dx ** 2 + dy ** 2)

        if length == 0: return

        nx = -dy / length
        ny = dx / length

        offset = self.stub_radius
        p1 = (start_pos[0] + nx * offset, start_pos[1] + ny * offset)
        p2 = (start_pos[0] - nx * offset, start_pos[1] - ny * offset)
        p3 = (end_pos[0] - nx * offset, end_pos[1] - ny * offset)
        p4 = (end_pos[0] + nx * offset, end_pos[1] + ny * offset)

        pygame.draw.polygon(self.game.game_canvas, self.rubber_band_color, [p1, p2, p3, p4], width=1)

        if draw_circles:
            pygame.draw.circle(self.game.game_canvas, self.rubber_band_color, start_pos, self.stub_radius)
            pygame.draw.circle(self.game.game_canvas, self.rubber_band_color, end_pos, self.stub_radius)

    def draw_board_bg(self, offset):
        angle = 3.14159 / 3
        z1 = offset * cos(angle)
        z2 = offset * sin(angle)

        point1 = self.coordinates_to_pixel((0, 0))
        point1 = [point1[0] - z1, point1[1] - z2]
        point2 = self.coordinates_to_pixel((0, self.board_size - 1))
        point2 = [point2[0] + z1, point2[1] - z2]
        point3 = self.coordinates_to_pixel((self.board_size - 1, (self.board_size - 1) * 2))
        point3 = [point3[0] + offset, point3[1]]
        point4 = self.coordinates_to_pixel(((self.board_size - 1) * 2, self.board_size - 1))
        point4 = [point4[0] + z1, point4[1] + z2]
        point5 = self.coordinates_to_pixel(((self.board_size - 1) * 2, 0))
        point5 = [point5[0] - z1, point5[1] + z2]
        point6 = self.coordinates_to_pixel((self.board_size - 1, 0))
        point6 = [point6[0] - offset, point6[1]]

        pygame.draw.polygon(self.game.game_canvas, self.board_bg_color, (point1, point2, point3, point4, point5, point6))

    def draw_rubber_bands(self):
        for path in self.paths:
            self.draw_rubber_band(self.coordinates_to_pixel(path[0]), self.coordinates_to_pixel(path[3]), True)

    def desno(self, coordinates):
        return coordinates[0], coordinates[1] + 1

    def dole_desno(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        return x + 1, y if x >= self.board_size - 1 else y + 1

    def dole_levo(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        return x + 1, y - 1 if x >= self.board_size - 1 else y

    def make_move(self, start: tuple, end: tuple):
        if self.check_length(start, end) is False:
            new_state = Transparent(self.game, "Put nije duzine 3!", self.shared_data)
            new_state.enter_state()
            return

        node_desno = start
        desni = [node_desno]
        node_d_levo = start
        d_levi = [node_d_levo]
        node_d_desno = start
        d_desni = [node_d_desno]

        for i in range(3):
            node_desno = self.desno(node_desno)
            desni.append(node_desno)
            node_d_levo = self.dole_levo(node_d_levo)
            d_levi.append(node_d_levo)
            node_d_desno = self.dole_desno(node_d_desno)
            d_desni.append(node_d_desno)

        # transparent da se popravi ne radi lepo za ovu gresku
        if node_desno == end:
            path = tuple(desni)
            if path in self.paths:
                new_state = Transparent(self.game, "Isti put je vec formiran!", self.shared_data)
                new_state.enter_state()
                return
            self.paths.add(path)
            for i, j in zip(desni[:-1], desni[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        elif node_d_levo == end:
            path = tuple(d_levi)
            if path in self.paths:
                new_state = Transparent(self.game, "Isti put je vec formiran!", self.shared_data)
                new_state.enter_state()
                return
            self.paths.add(path)
            for i, j in zip(d_levi[:-1], d_levi[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        elif node_d_desno == end:
            path = tuple(d_desni)
            if path in self.paths:
                new_state = Transparent(self.game, "Isti put je vec formiran!", self.shared_data)
                new_state.enter_state()
                return
            self.paths.add(path)
            for i, j in zip(d_desni[:-1], d_desni[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        else:
            new_state = Transparent(self.game, "Potez mora da bude u formatu: Desno, Dole Desno ili Dole Levo!", self.shared_data)
            new_state.enter_state()
            return False

        self.shared_data['last_turn'] = (start, end)
        self.find_triangle()
        self.change_player()

        return True

    def check_length(self, stub1: tuple, stub2: tuple):
        x = abs(stub2[0] - stub1[0])
        y = abs(stub2[1] - stub1[1])
        return True if x == 3 or y == 3 else False

    def draw_traingle(self, center, color, upside_down):
        line_length = self.d / 5
        x = center[0]
        y = center[1]

        surface = self.game.game_canvas
        width = self.stub_radius - 2

        direction = 1 if not upside_down else -1

        pygame.draw.line(surface, color, center, (x, y + direction * line_length), width)
        pi = 3.14159
        angle = pi / 6
        z1 = direction * line_length * cos(angle)
        z2 = direction * line_length * sin(angle)

        pygame.draw.line(surface, color, center, (x + z1, y - z2), width)
        pygame.draw.line(surface, color, center, (x - z1, y - z2), width)

    def draw_triangles(self):
        # resetujemo na nula jer se trouglici u svakom potezu crtaju opet
        # moze da se promeni da imamo po jos jedan set koji ce da sadrzi nacrtane trouglove

        # if self.shared_data['current_player']:
        #     self.player1_points = 0
        # else:
        #     self.player2_points = 0
        self.player1_points = len(self.player1_set)
        self.player2_points = len(self.player2_set)

        for cycle in self.player1_set:
            upside_down = False
            if cycle[0][0] == cycle[1][0]:
                x, y = self.coordinates_to_pixel(cycle[2])
                center_x = x
                center_y = y - (2 / 3 * self.h)
            else:
                x, y = self.coordinates_to_pixel(cycle[0])
                center_x = x
                center_y = y + (2 / 3 * self.h)
                upside_down = True

            self.draw_traingle((center_x, center_y), player1_color, upside_down)
            # if self.shared_data['current_player']:
            #     self.player1_points += 1
            # else:
            #     self.player2_points += 1

        for cycle in self.player2_set:
            upside_down = False
            if cycle[0][0] == cycle[1][0]:
                x, y = self.coordinates_to_pixel(cycle[2])
                center_x = x
                center_y = y - (2 / 3 * self.h)
            else:
                x, y = self.coordinates_to_pixel(cycle[0])
                center_x = x
                center_y = y + (2 / 3 * self.h)
                upside_down = True
            self.draw_traingle((center_x, center_y), player2_color, upside_down)
            # if self.shared_data['current_player']:
            #     self.player1_points += 1
            # else:
            #     self.player2_points += 1

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