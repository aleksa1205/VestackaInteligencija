import pygame

from src.ui_components.colors import transparent, bg_color, rubber_band_color
from src.states.state import State

class Transparent(State):
    def __init__(self, game, text, shared_data):
        super().__init__(game)
        self.time = pygame.time.get_ticks()
        self.duration = 1500

        self.text_surf = self.game.gui_font.render(text, True, 'Red')
        self.text_rect = self.text_surf.get_rect(midbottom=(self.game.SCREEN_WIDTH >> 1, self.game.SCREEN_HEIGHT - 30))

        self.white_surf = pygame.surface.Surface((self.text_rect.w, self.text_rect.h))
        self.white_rect = self.white_surf.get_rect(center = self.text_rect.center)

        self.game.error_sound.play()

        # Stubovi
        self.stubovi = shared_data['stubovi']
        self.total_stubs = len(self.stubovi)
        self.time_per_stub = self.duration / self.total_stubs
        self.stubs_colored = 0

    def update(self, delta_time, events):
        elapsed_time = pygame.time.get_ticks() - self.time

        # Racuna koliko stubova boji ovog frejma
        new_stubs_colored = min(self.total_stubs, int(elapsed_time / self.time_per_stub))


        for i in range(self.stubs_colored, new_stubs_colored):
            self.stubovi[i].color = rubber_band_color
        self.stubs_colored = new_stubs_colored

        if elapsed_time > self.duration:
            for stub in self.stubovi: stub.color = stub.default_color
            self.exit_state()

    def render(self, surface):
        # self.game.game_canvas.fill(transparent)
        self.white_surf.fill(bg_color)
        self.game.game_canvas.blit(self.white_surf, self.white_rect)
        self.game.game_canvas.blit(self.text_surf, self.text_rect)

        for stub in self.stubovi: stub.render()