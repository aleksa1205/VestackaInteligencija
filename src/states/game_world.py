from src.functionality.draw import create_empty_board
from src.states.state import State
from src.functionality.board import Board
import pygame.display
import src.globals as g
from src.ui_components.colors import bg_color


class GameWorld(State):
    def __init__(self, game, board_size, plays_first):
        super().__init__(game)
        self.board_size = board_size
        self.plays_first = plays_first
        self.board = Board(game, board_size)
        g.n = board_size

        pygame.display.set_caption('Triggle')
        print('Game started...')
        print(self.board_size, self.plays_first)

    def update(self, delta_time):
        pass

    def render(self, surface):
        self.game.game_canvas.fill(bg_color)
        self.board.render()