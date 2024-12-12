from src.states.change_player import ChangePlayer
from src.states.state import State
from src.functionality.board import Board
import pygame.display
from src.ui_components.colors import bg_color, player1_color, player2_color


class GameWorld(State):
    def __init__(self, game, board_size, plays_first):
        super().__init__(game)
        pygame.display.set_caption('Triggle')

        # Game data
        self.shared_data = {
            'current_player': True,
            'change_player_state': False,
            'stubovi': [],
            'last_turn': None
        }

        # Board
        self.board_size = board_size
        self.plays_first = plays_first
        self.board = Board(game, board_size, (100, 100), self.shared_data)
        self.board_size = board_size

        # Player Turn
        self.player_turn_surf, self.player_turn_rect = None, None
        self.update_player_turn_text()

        print('Game started...')
        print(self.board_size, self.plays_first)

    def update(self, delta_time):
        self.update_player_turn_text()
        self.board.update()

        if self.shared_data['change_player_state']:
            change_player_state = ChangePlayer(self.game, self.shared_data)
            change_player_state.enter_state()

    def render(self, surface):
        self.game.game_canvas.fill(bg_color)

        self.game.game_canvas.blit(self.player_turn_surf, self.player_turn_rect)

        self.board.render()

    def update_player_turn_text(self):
        if self.shared_data['current_player']:
            text = 'Player 1 Turn'
            color = player1_color
        else:
            text = 'Player 2 Turn'
            color = player2_color

        self.player_turn_surf = self.game.gui_font.render(text, True, color)
        self.player_turn_rect = self.player_turn_surf.get_rect(midtop = (self.game.GAME_W >> 1, 30))