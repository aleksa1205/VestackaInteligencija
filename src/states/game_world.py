from src.states.state import State
from src.Functionality.board import Board
import pygame.display
import src.globals as g
from src.UI_Components.colors import bg_color


class GameWorld(State):
    def __init__(self, game, board_size, plays_first):
        super().__init__(game)
        self.board_size = board_size
        self.plays_first = plays_first
        self.board = Board(game, board_size)
        self.pause = False

        g.n = board_size

        pygame.display.set_caption('Triggle')
        print('Game started...')
        print(self.board_size, self.plays_first)

    def update(self, delta_time, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from src.states.pause_menu import PauseMenu
                    new_state = PauseMenu(self.game)
                    new_state.enter_state()

    def render(self, surface):
        self.game.game_canvas.fill(bg_color)
        self.board.render()