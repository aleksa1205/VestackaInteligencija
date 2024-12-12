from src.states.change_player import ChangePlayer
from src.states.state import State
from src.functionality.board import Board
from pygame import Rect
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
            'last_turn': ()
        }

        # Board
        self.board_size = board_size
        self.plays_first = plays_first
        self.board = Board(game, board_size, self.shared_data)
        self.board_size = board_size

        # Player Turn
        self.player_turn_surf, self.player_turn_rect = None, None
        self.update_player_turn_text()
        self.board = Board(game, board_size)
        self.pause = False

        print('Game started...')
        print(self.board_size, self.plays_first)

    def update(self, delta_time, events):
        self.update_player_turn_text()
        self.board.update()
        self.update_text()

    def render(self, surface):
        self.game.game_canvas.fill(bg_color)

        self.board.render()

        self.game.game_canvas.blit(self.player_turn_surf, self.player_turn_rect)

        if self.shared_data['last_turn']:
            self.game.game_canvas.blit(self.last_turn_surf, self.last_turn_rect)

        if self.shared_data['change_player_state']:
            change_player_state = ChangePlayer(self.game, self.shared_data)
            change_player_state.enter_state()
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from src.states.pause_menu import PauseMenu
                    new_state = PauseMenu(self.game)
                    new_state.enter_state()

    def update_text(self):
        if self.shared_data['change_player_state']:
            last_turn = self.shared_data['last_turn']
            if not self.shared_data['current_player']:
                text = f'Player 1 played {last_turn[0]} -> {last_turn[1]}'
                color = player1_color
                turn_text = ''
            else:
                text = f'Player 2 played {last_turn[0]} -> {last_turn[1]}'
                color = player2_color
                turn_text = ''
        else:
            last_turn = self.shared_data['last_turn']
            turn_text = ''
            if self.shared_data['current_player']:
                text = 'Player 1 Turn'
                color = player1_color
                if last_turn:
                    turn_text = f'Player 2 played {last_turn[0]} -> {last_turn[1]} last turn'
            else:
                text = 'Player 2 Turn'
                color = player2_color
                if last_turn:
                    turn_text = f'Player 1 played {last_turn[0]} -> {last_turn[1]} last turn'

        self.player_turn_surf = self.game.gui_font.render(text, True, color)
        self.player_turn_rect = self.player_turn_surf.get_rect(midtop = (self.game.GAME_W >> 1, 30))

        self.last_turn_surf = self.game.gui_font.render(turn_text, True, (0, 0, 0))
        self.last_turn_rect = self.last_turn_surf.get_rect(midtop = (self.game.GAME_W >> 1, 60))