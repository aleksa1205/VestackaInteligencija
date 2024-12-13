import pygame

from src.ui_components.colors import main_color_600, main_color_700, main_color_800


class Button:
    def __init__(self, game, text, pos, width = 200, height = 40, rect_point = None, value = None):
        # Core attributes
        self.game = game
        self.pressed = False
        self.active = False
        self.button_color = main_color_600
        self.hover_color = main_color_700
        self.active_color = main_color_800
        self.value = value

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        if rect_point == 'midtop':
            self.top_rect.midtop = pos
        if rect_point == 'center':
            self.top_rect.center = pos
        if rect_point == 'midbottom':
            self.top_rect.midbottom = pos
        self.top_color = self.button_color

        #text
        self.text_surf = game.gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def render(self):
        pygame.draw.rect(self.game.game_canvas, self.top_color, self.top_rect, border_radius = 12)
        self.game.game_canvas.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.active:
            self.top_color = self.active_color
        else:
            self.top_color = self.button_color

        if self.top_rect.collidepoint(mouse_pos):
            if not self.active:
                self.top_color = self.hover_color
            if pygame.mouse.get_pressed()[0] and not self.pressed:
               self.pressed = True
               return True
        elif not self.active:
            self.top_color = self.button_color

        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False

            return False

    def set_active(self, active):
        self.active = active