from math import sin, cos
import pygame.draw

from src.board_logic.board_utility import coordinates_to_pixel
from src.ui_components.colors import neutral_color_800


class BoardBackground:
    def __init__(self, board, offset = 25):
        self.offset = offset
        self.board = board
        self.board_bg_color = neutral_color_800

    def render(self, surface):
        angle = 3.14159 / 3
        z1 = self.offset * cos(angle)
        z2 = self.offset * sin(angle)

        point1 = coordinates_to_pixel(self.board, (0, 0))
        point1 = [point1[0] - z1, point1[1] - z2]
        point2 = coordinates_to_pixel(self.board, (0, self.board.board_size - 1))
        point2 = [point2[0] + z1, point2[1] - z2]
        point3 = coordinates_to_pixel(self.board, (self.board.board_size - 1, (self.board.board_size - 1) * 2))
        point3 = [point3[0] + self.offset, point3[1]]
        point4 = coordinates_to_pixel(self.board, ((self.board.board_size - 1) * 2, self.board.board_size - 1))
        point4 = [point4[0] + z1, point4[1] + z2]
        point5 = coordinates_to_pixel(self.board, ((self.board.board_size - 1) * 2, 0))
        point5 = [point5[0] - z1, point5[1] + z2]
        point6 = coordinates_to_pixel(self.board, (self.board.board_size - 1, 0))
        point6 = [point6[0] - self.offset, point6[1]]

        pygame.draw.polygon(surface, self.board_bg_color,
                            (point1, point2, point3, point4, point5, point6))