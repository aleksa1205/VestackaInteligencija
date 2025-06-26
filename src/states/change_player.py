from threading import Thread

from src.board_logic.game_state import GameState
from src.states.ai_thinking_state import AIThinkingState
from src.states.state import State
import pygame.time
from src.ui_components.colors import player1_color, player2_color, whiteish, bg_color
from src.board_logic.min_max import minmax
from math import inf


class ChangePlayer(State):
    def __init__(self, game, pegs, current_player, shared_data, game_state=None):
        super().__init__(game)
        self.ai_plays_first = shared_data['ai_plays_first']
        self.start_time = pygame.time.get_ticks()
        self.duration = 1500
        self.game_state = game_state

        self.shared_data = shared_data
        self.current_player = current_player

        # Pegs
        self.pegs = pegs
        self.total_pegs = len(self.pegs)
        self.time_per_peg = self.duration / self.total_pegs
        self.stubs_colored = 0

        if not self.ai_plays_first:
            self.game.success_sound.play()

        # run minmax
        if game_state is not None:
            Thread(target=run_min_max, args=(self, game_state)).start()
            # run_min_max(self, game_state)

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

            if self.game_state is not None:
                new_state = AIThinkingState(self.game, self.shared_data)
                new_state.enter_state()
                return

            self.exit_state()

    def render(self, surface):
        if self.ai_plays_first: return
        for peg in self.pegs:
            peg.render()


def run_min_max(self, game_state: GameState):
    print("Min-max started...")
    best_score, best_path = minmax(game_state, 3, -inf, inf, True)
    print("Min-max finished!")
    print(best_path)

    self.shared_data['ai_move_ready'] = True
    self.shared_data['ai_move'] = best_path[0]
    self.game_state = None
