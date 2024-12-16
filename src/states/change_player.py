from pygame import Rect
from src.states.state import State
import pygame.time
from src.ui_components.colors import player1_color, player2_color, whiteish, bg_color


class ChangePlayer(State):
    def __init__(self, game, pegs, current_player, shared_data):
        super().__init__(game)
        self.start_time = pygame.time.get_ticks()
        self.duration = 1500

        self.shared_data = shared_data
        self.current_player = current_player

        # Pegs
        self.pegs = pegs
        self.total_pegs = len(self.pegs)
        self.time_per_peg = self.duration / self.total_pegs
        self.stubs_colored = 0

        self.game.success_sound.play()

    def update(self, delta_time, events):
        elapsed_time = pygame.time.get_ticks() - self.start_time

        # Racuna koliko stubova boji ovog frejma
        new_stubs_colored = min(self.total_pegs, int(elapsed_time / self.time_per_peg))


        for i in range(self.stubs_colored, new_stubs_colored):
            self.pegs[i].color = player1_color if not self.current_player == 1 else player2_color
        self.stubs_colored = new_stubs_colored

        if elapsed_time >= self.duration:
            for stub in self.pegs:
                stub.color = 'Black'

            self.shared_data['turn_played'] = False
            self.exit_state()

    def render(self, surface):
        for peg in self.pegs:
            peg.render()