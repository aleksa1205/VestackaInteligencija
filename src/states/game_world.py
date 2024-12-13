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
            'last_turn': ()
        }

        # Board
        self.board_size = board_size
        self.plays_first = plays_first
        self.board = Board(game, board_size, self.shared_data)
        self.board_size = board_size

        # Player Turn
        self.player_turn_surf, self.player_turn_rect = None, None
        self.last_turn_surf, self.last_turn_rect = None, None
        self.player1_points_surf, self.player1_points_rect = None, None
        self.player2_points_surf, self.player2_points_rect = None, None
        self.update_top_text()
        self.pause = False

        print('Game started...')
        print(self.board_size, self.plays_first)

    def update(self, delta_time, events):
        self.board.update(events)
        self.update_top_text()

        # print(self.board.player1_points)
        # print(self.board.player2_points)
        if self.board.player1_points > self.board.points_to_win or self.board.player2_points > self.board.points_to_win:
            from src.states.end_game import EndGame
            new_state = EndGame(self.game, "Player1 wins!" if self.board.player1_points > self.board.player2_points else "Player2 wins!", player1_color if self.board.player1_points > self.board.player2_points else player2_color)
            new_state.enter_state()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if len(self.board.selected_stubovi) == 1:
                        self.board.selected_stubovi[0].reset_clicked()
                        self.board.selected_stubovi.clear()
                    else:
                        from src.states.pause_menu import PauseMenu
                        new_state = PauseMenu(self.game)
                        new_state.enter_state()


    def render(self, surface):
        self.game.game_canvas.fill(bg_color)
        # nadji tacke
        self.board.render()

        self.game.game_canvas.blit(self.player_turn_surf, self.player_turn_rect)
        self.game.game_canvas.blit(self.player1_points_surf, self.player1_points_rect)
        self.game.game_canvas.blit(self.player2_points_surf, self.player2_points_rect)

        if self.shared_data['last_turn']:
            self.game.game_canvas.blit(self.last_turn_surf, self.last_turn_rect)

        if self.shared_data['change_player_state']:
            change_player_state = ChangePlayer(self.game, self.shared_data)
            change_player_state.enter_state()

    def update_top_text(self):
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

        self.player1_points_surf = self.game.title_font.render(str(self.board.player1_points), True, player1_color)
        self.player1_points_rect = self.player1_points_surf.get_rect(midleft = (15, self.game.GAME_H >> 1))

        self.player2_points_surf = self.game.title_font.render(str(self.board.player2_points), True, player2_color)
        self.player2_points_rect = self.player2_points_surf.get_rect(midright = (self.game.GAME_W - 15, self.game.GAME_H >> 1))