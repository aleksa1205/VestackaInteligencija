import pygame

from src.UI_Components.colors import transparent
from src.states.state import State

class Transparent(State):
    def __init__(self, game, text):
        super().__init__(game)
        self.time = pygame.time.get_ticks()

        self.text_surf = self.game.gui_font.render(text, True, 'Red')
        self.text_rect = self.text_surf.get_rect(midbottom=(self.game.SCREEN_WIDTH >> 1, self.game.SCREEN_HEIGHT - 30))

    def update(self, delta_time, events):
        elapsed_time = pygame.time.get_ticks() - self.time
        if elapsed_time > 1500:
            self.exit_state()

    def render(self, surface):
        # self.game.game_canvas.fill(transparent)
        self.game.game_canvas.blit(self.text_surf, self.text_rect)