from typing import Tuple
import pygame
from math import sqrt

from src.states.transparent import Transparent


class Board:
    def __init__(self, game, board_size):
        self.game = game
        self.board_size = board_size
        self.d = 30
        self.h = self.d * sqrt(3) / 2
        # self.hex_width = ((self.board_size - 1) * 2) * self.d
        # self.hex_height = ((self.board_size - 1) * 2) * self.h
        self.x_start = (self.game.SCREEN_WIDTH - (((self.board_size - 1) * 2) * self.d)) / 2
        self.y_start = (self.game.SCREEN_HEIGHT - (((self.board_size - 1) * 2) * self.h)) / 2
        self.currentPlayer = True
        self.paths = set()
        # player1 / plavi
        self.player1_color = (102, 208, 242)
        # su njegovi trouglovi
        self.player1_set = set()
        self.player1_points = 0

        self.message_start_time = None

        # player2 / ai
        self.player2_color = (100, 28, 30)
        self.player2_set = set()
        self.player2_points = 0
        self.graph = {}
        # kreiranje grafa
        for i in range(2 * self.board_size - 1):
            for j in range(2 * self.board_size - 1 - abs(self.board_size - 1 - i)):
                # print(i)
                # print(j)
                self.graph[(i, j)] = set()

    # Metode klase
    def update(self):
        pass

    def render(self):
        for i in range(2 * self.board_size - 1):
            # row = []
            for j in range(2 * self.board_size - 1 - abs(self.board_size - 1 - i)):
                # provera za polja tabele
                # row.append(i * 10 + j)
                # print(row)
                pygame.draw.circle(self.game.game_canvas, (0, 0, 0), self.coordinates_to_pixel((i, j)), 3)

        self.make_move((0, 0), (0, 3))
        self.make_move((0, 0), (0, 4))
        self.make_move((0, 0), (3, 0))
        self.make_move((0, 0), (3, 3))
        self.make_move((1, 0), (1, 3))
        self.change_player()
        self.make_move((0, 1), (3, 1))

    # Pomocne funkcije
    def coordinates_to_pixel(self, coordinates : Tuple):
        x = coordinates[0]
        y = coordinates[1]
        return self.x_start + abs(self.board_size - 1 - x) * self.d / 2 + y * self.d, self.y_start + x * self.h

    def draw_line(self, start : Tuple, end : Tuple):
        # pygame.draw.line(globals.screen, globals.player1_color if globals.currentPlayer else globals.player2_color, coordinates_to_pixel(start, n),coordinates_to_pixel(end, n), 3)
        pygame.draw.line(self.game.game_canvas, (0, 0, 0), self.coordinates_to_pixel(start), self.coordinates_to_pixel(end), 3)

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
            new_state = Transparent(self.game, "Put nije duzine 3!")
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
                print("Isti put je vec formiran!")
            self.paths.add(path)
            for i, j in zip(desni[:-1], desni[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        elif node_d_levo == end:
            path = tuple(d_levi)
            if path in self.paths:
                print("Isti put je vec formiran!")
            self.paths.add(path)
            for i, j in zip(d_levi[:-1], d_levi[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        elif node_d_desno == end:
            path = tuple(d_desni)
            if path in self.paths:
                print("Isti put je vec formiran!")
            self.paths.add(path)
            for i, j in zip(d_desni[:-1], d_desni[1:]):
                self.graph[i].add(j)
                self.graph[j].add(i)
        else:
            return False
        self.draw_line(start, end)
        self.find_triangle()
        self.draw_triangles()
        return True

    def check_length(self, stub1: tuple, stub2: tuple):
        x = abs(stub2[0] - stub1[0])
        y = abs(stub2[1] - stub1[1])
        return True if x == 3 or y == 3 else False

    def draw_triangles(self):
        # resetujemo na nula jer se trouglici u svakom potezu crtaju opet
        # moze da se promeni da imamo po jos jedan set koji ce da sadrzi nacrtane trouglove
        if self.currentPlayer:
            self.player1_points = 0
        else:
            self.player2_points = 0
        # g.player1_points = 0 if g.currentPlayer else g.player2_points = 0
        for i in self.player1_set if self.currentPlayer else self.player2_set:
            points_px = [self.coordinates_to_pixel(i[0]), self.coordinates_to_pixel(i[1]), self.coordinates_to_pixel(i[2])]
            pygame.draw.polygon(self.game.game_canvas, self.player1_color if self.currentPlayer else self.player2_color, points_px)
            if self.currentPlayer:
                self.player1_points += 1
            else:
                self.player2_points += 1

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
                            self.player1_set.add(cycle) if self.currentPlayer else self.player2_set.add(cycle)

    def change_player(self):
        self.currentPlayer = not self.currentPlayer