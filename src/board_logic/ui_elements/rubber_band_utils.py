from src.board_logic.board_utility import coordinates_to_pixel
from src.ui_components.colors import rubber_band_color
from math import sqrt
import pygame.draw

class RubberBandUtils:

    @staticmethod
    def draw_rubber_band(surface, start_pos, end_pos, peg_radius, color, draw_circles = True):
        """Draw a hollow, bordered line between two points."""
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = sqrt(dx ** 2 + dy ** 2)

        if length == 0: return

        nx = -dy / length
        ny = dx / length

        offset = peg_radius
        p1 = (start_pos[0] + nx * offset, start_pos[1] + ny * offset)
        p2 = (start_pos[0] - nx * offset, start_pos[1] - ny * offset)
        p3 = (end_pos[0] - nx * offset, end_pos[1] - ny * offset)
        p4 = (end_pos[0] + nx * offset, end_pos[1] + ny * offset)

        pygame.draw.polygon(surface, color, [p1, p2, p3, p4], width=1)

        if draw_circles:
            pygame.draw.circle(surface, color, start_pos, peg_radius)
            pygame.draw.circle(surface, color, end_pos, peg_radius)

    @staticmethod
    def draw_rubber_bands(surface, paths, board, peg_radius, color):
        for path in paths:
            RubberBandUtils.draw_rubber_band(surface, coordinates_to_pixel(board, path[0]), coordinates_to_pixel(board, path[3]), peg_radius, color, True)