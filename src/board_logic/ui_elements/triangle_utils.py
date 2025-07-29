import pygame.draw
from math import sin, cos

from src.board_logic.board_utility import coordinates_to_pixel
from src.ui_components.colors import player1_color


class TriangleUtils:
    @staticmethod
    def draw_traingle(surface, center, color, d, peg_radius, upside_down):
        line_length = d / 5
        x = center[0]
        y = center[1]

        surface = surface
        width = peg_radius - 2

        direction = 1 if not upside_down else -1

        pygame.draw.line(surface, color, center, (x, y + direction * line_length), width)
        pi = 3.14159
        angle = pi / 6
        z1 = direction * line_length * cos(angle)
        z2 = direction * line_length * sin(angle)

        pygame.draw.line(surface, color, center, (x + z1, y - z2), width)
        pygame.draw.line(surface, color, center, (x - z1, y - z2), width)\

    @staticmethod
    def draw_triangles(surface, board, player2_color):
        for cycle in board.game_state.player_triangles['player1']:
            upside_down = False
            if cycle[0][0] == cycle[1][0]:
                x, y = coordinates_to_pixel(board, cycle[2])
                center_x = x
                center_y = y - (2 / 3 * board.h)
            else:
                x, y = coordinates_to_pixel(board, cycle[0])
                center_x = x
                center_y = y + (2 / 3 * board.h)
                upside_down = True

            TriangleUtils.draw_traingle(surface, (center_x, center_y), player1_color, board.d, board.peg_radius, upside_down)

        for cycle in board.game_state.player_triangles['player2']:
            upside_down = False
            if cycle[0][0] == cycle[1][0]:
                x, y = coordinates_to_pixel(board, cycle[2])
                center_x = x
                center_y = y - (2 / 3 * board.h)
            else:
                x, y = coordinates_to_pixel(board, cycle[0])
                center_x = x
                center_y = y + (2 / 3 * board.h)
                upside_down = True
            TriangleUtils.draw_traingle(surface, (center_x, center_y), player2_color, board.d, board.peg_radius, upside_down)