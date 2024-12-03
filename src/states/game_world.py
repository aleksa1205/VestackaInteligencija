from src.functionality.draw import create_empty_board
from src.states.state import State
import pygame.display
import src.globals as g

class GameWorld(State):
    def __init__(self, game, board_size, plays_first):
        super().__init__(game)
        self.board_size = board_size
        self.plays_first = plays_first
        g.n = board_size

        pygame.display.set_caption('Triggle')
        print('Game started...')
        print(self.board_size, self.plays_first)

    def update(self, delta_time):
        pass

    def render(self, surface):
        self.game.game_canvas.fill('#DCDDD8')
        create_empty_board(self.game.game_canvas)