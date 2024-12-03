import pygame
from src import globals as g

screen = pygame.display.get_surface()

def coordinates_to_pixel(coordinates):
    x = coordinates[0]
    y = coordinates[1]
    m = abs(g.n - 1 - x)
    return g.x_start + abs(g.n - 1 - x) * g.d / 2 + y * g.d, g.y_start + x * g.h

def create_empty_board():
    # matrix = []
    for i in range(2 * g.n - 1):
        # row = []
        for j in range(2 * g.n - 1 - abs(g.n - 1 - i)):
            # provera za polja tabele
            # row.append(i * 10 + j)
            # print(row)
            pygame.draw.circle(screen, (0, 0, 0), coordinates_to_pixel((i, j)), 3)

def create_graph():
    for i in range(2 * g.n - 1):
        for j in range(2 * g.n - 1 - abs(g.n - 1 - i)):
            # print(i)
            # print(j)
            g.graph[(i, j)] = set()

def draw_line(start, end):
    # pygame.draw.line(globals.screen, globals.player1_color if globals.currentPlayer else globals.player2_color, coordinates_to_pixel(start, n),coordinates_to_pixel(end, n), 3)
    pygame.draw.line(screen, (0, 0, 0), coordinates_to_pixel(start), coordinates_to_pixel(end), 3)

def draw_triangles():
    # resetujemo na nula jer se trouglici u svakom potezu crtaju opet
    # moze da se promeni da imamo po jos jedan set koji ce da sadrzi nacrtane trouglove
    g.player1_points = 0 if g.currentPlayer else g.player2_points = 0
    for i in g.player1_set if g.currentPlayer else g.player2_set:
        points_px = [coordinates_to_pixel(i[0]), coordinates_to_pixel(i[1]), coordinates_to_pixel(i[2])]
        pygame.draw.polygon(screen, g.player1_color if g.currentPlayer else g.player2_color, points_px)
        if g.currentPlayer:
            g.player1_points += 1
        else:
            g.player2_points += 1