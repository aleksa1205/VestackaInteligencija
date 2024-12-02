import pygame
from src import globals as g

def coordinates_to_pixel(i, n):
    m = abs(n - 1 - i[0])
    return g.x_start + abs(n - 1 - i[0]) * g.d / 2 + i[1] * g.d, g.y_start + i[0] * g.h

def create_empty_board(n):
    matrix = []
    for i in range(2 * n - 1):
        # row = []
        for j in range(2 * n - 1 - abs(n - 1 - i)):
            # provera za polja tabele
            # row.append(i * 10 + j)
            # print(row)
            pygame.draw.circle(g.screen, (0, 0, 0), coordinates_to_pixel((i, j), n), 3)

def create_graph():
    for i in range(2 * g.n - 1):
        for j in range(2 * g.n - 1 - abs(g.n - 1 - i)):
            # print(i)
            # print(j)
            g.graph[(i, j)] = set()

def draw_line(start, end, n):
    # pygame.draw.line(globals.screen, globals.player1_color if globals.currentPlayer else globals.player2_color, coordinates_to_pixel(start, n),coordinates_to_pixel(end, n), 3)
    pygame.draw.line(g.screen, (0, 0, 0), coordinates_to_pixel(start, n), coordinates_to_pixel(end, n), 3)

def draw_triangles():
    for i in g.player1_set if g.currentPlayer else g.player2_set:
        points_px = [coordinates_to_pixel(i[0], g.n), coordinates_to_pixel(i[1], g.n), coordinates_to_pixel(i[2], g.n)]
        pygame.draw.polygon(g.screen, g.player1_color if g.currentPlayer else g.player2_color, points_px)
        if g.currentPlayer:
            g.player1_points += 1
        else:
            g.player2_points += 1