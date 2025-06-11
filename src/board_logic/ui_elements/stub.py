import pygame
from pygame.rect import RectType

from src.ui_components.colors import neutral_color_500, neutral_color_900, neutral_color_800, neutral_color_700, \
    neutral_color_400, neutral_color_100, neutral_color_200


class Stub:
    def __init__(self, game, index, radius, board_size, distance, height, x_start, y_start):
        self.index = index
        self.board_size = board_size
        self.distance = distance
        self.height = height
        self.x_start = x_start
        self.y_start = y_start

        self.game = game
        self.pos = self.coordinates_to_pixel(index)
        self.default_color = neutral_color_800
        self.color = self.default_color
        self.hover_color = neutral_color_400
        self.active_color = neutral_color_900
        self.radius = radius
        self.rect : RectType = pygame.Rect(self.pos, (radius * 2, radius * 2))
        self.rect.center = self.pos
        self.clicked = False

    def update(self):
        pass

    def render(self):
        pygame.draw.circle(self.game.game_canvas, neutral_color_200, self.pos, self.radius)
        pygame.draw.circle(self.game.game_canvas, self.color, self.pos, self.radius - 1)

    def check_click(self, hover_color):
        if self.clicked: self.color = self.active_color

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.clicked:
                self.color = hover_color
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True
        elif not self.clicked:
            self.color = self.default_color
        return False

    def reset_clicked(self):
        self.clicked = False

    def coordinates_to_pixel(self, index : tuple):
        x = index[0]
        y = index[1]

        result = (
            self.x_start + abs(self.board_size - 1 - x) * self.distance / 2 + y * self.distance,
            self.y_start + x * self.height
        )

        return result