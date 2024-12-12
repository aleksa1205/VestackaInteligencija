from pygame import Rect
from src.states.state import State
import pygame.time

from src.ui_components.colors import player1_color, player2_color, whiteish


class ChangePlayer(State):
    def __init__(self, game, shared_data):
        super().__init__(game)
        self.shared_data = shared_data
        self.start_time = pygame.time.get_ticks()
        self.duration = 2000

        self.stubovi = shared_data['stubovi']

        # text to display
        self.last_turn = shared_data['last_turn']
        if not shared_data['current_player']:
            text = f'Player 1 played bla bla'
            color = player1_color
        else:
            text = f'Player 2 played bla bla'
            color = player2_color

        self.text_surf = self.game.gui_font.render(text, True, color)
        self.text_rect : Rect = self.text_surf.get_rect(midtop = (self.game.GAME_W >> 1, 30))
        self.white_surf = pygame.surface.Surface((self.text_rect.w, self.text_rect.h))

    def update(self, delta_time):
        curr_player = self.shared_data['current_player']
        for stub in self.stubovi:
            stub.color = player1_color if not curr_player else player2_color

        curr_time = pygame.time.get_ticks()
        if curr_time - self.start_time >= self.duration:
            for stub in self.stubovi:
                stub.color = 'Black'

            self.shared_data['change_player_state'] = False
            self.exit_state()

    def render(self, surface):
        self.white_surf.fill(whiteish)
        surface.blit(self.white_surf, self.text_rect)
        surface.blit(self.text_surf, self.text_rect)

        for stub in self.stubovi:
            stub.render()