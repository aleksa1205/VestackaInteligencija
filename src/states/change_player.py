from pygame import Rect
from src.states.state import State
import pygame.time
from src.ui_components.colors import player1_color, player2_color, whiteish, bg_color


class ChangePlayer(State):
    def __init__(self, game, shared_data):
        super().__init__(game)
        self.shared_data = shared_data
        self.start_time = pygame.time.get_ticks()
        self.duration = 1500

        # Stubovi
        self.stubovi = shared_data['stubovi']
        self.total_stubs = len(self.stubovi)
        self.time_per_stub = self.duration / self.total_stubs
        self.stubs_colored = 0

    def update(self, delta_time, events):
        elapsed_time = pygame.time.get_ticks() - self.start_time

        # Racuna koliko stubova boji ovog frejma
        new_stubs_colored = min(self.total_stubs, int(elapsed_time / self.time_per_stub))

        curr_player = self.shared_data['current_player']

        for i in range(self.stubs_colored, new_stubs_colored):
            self.stubovi[i].color = player1_color if not curr_player else player2_color
        self.stubs_colored = new_stubs_colored

        if elapsed_time >= self.duration:
            for stub in self.stubovi:
                stub.color = 'Black'

            self.shared_data['change_player_state'] = False
            self.exit_state()

    def render(self, surface):
        for stub in self.stubovi:
            stub.render()