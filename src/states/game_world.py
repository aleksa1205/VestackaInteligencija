from src.states.change_player import ChangePlayer
from src.states.game_config import GameConfig, GameMode
from src.states.state import State
from src.board_logic.board import Board
import pygame.display
from src.ui_components.colors import bg_color, player1_color, player2_color_const, ai_color_const


class GameWorld(State):
    def __init__(self, game, game_config: GameConfig):
        super().__init__(game)
        pygame.display.set_caption('Triggle')

        if game_config.mode == GameMode.P_VS_AI:
            self.game.player2_color = ai_color_const


        ai_plays_first = game_config.current_player == 2 and game_config.mode == GameMode.P_VS_AI
        # Game data
        self.shared_data = {
            'turn_played': False,
            'ai_move': None,
            'ai_move_ready': False,
            'game_state': None,
            'ai_plays_first': ai_plays_first
        }

        # Board
        self.game_config = game_config
        self.board = Board(game, game_config, self.shared_data)

        # Player Turn
        self.player_turn_surf, self.player_turn_rect = None, None
        self.last_turn_surf, self.last_turn_rect = None, None
        self.player1_points_surf, self.player1_points_rect = None, None
        self.player2_points_surf, self.player2_points_rect = None, None
        self.update_top_text()
        self.pause = False

        print('Game started...')
        print('Board Size: ' + self.game_config.board_size.__str__())
        print('Current Player: ' + self.game_config.current_player.__str__())
        print('Game Mode: ' + self.game_config.mode.name)

    def update(self, delta_time, events):
        self.board.update(events)
        self.update_top_text()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if len(self.board.selected_pegs) == 1:
                        self.board.selected_pegs[0].reset_clicked()
                        self.board.selected_pegs.clear()
                    else:
                        from src.states.pause_menu import PauseMenu
                        new_state = PauseMenu(self.game)
                        new_state.enter_state()

    def render(self, surface):
        surface.fill(bg_color)
        self.board.render(surface)

        surface.blit(self.player_turn_surf, self.player_turn_rect)
        surface.blit(self.player1_points_surf, self.player1_points_rect)
        surface.blit(self.player2_points_surf, self.player2_points_rect)

        if self.board.game_state.last_move:
            surface.blit(self.last_turn_surf, self.last_turn_rect)

        if self.shared_data['ai_move_ready']:
            print('bro make move')
            move = self.shared_data['ai_move']
            self.board.make_move(move[0], move[1], surface)

            if self.shared_data['ai_plays_first']:
                self.shared_data['ai_plays_first'] = False
            self.shared_data['ai_move'] = None
            self.shared_data['ai_move_ready'] = False
            self.shared_data['game_state'] = None

            self.check_for_end_game()

        # ako je AI mode i ako AI igra
        if self.game_config.mode == GameMode.P_VS_AI and self.board.game_state.current_player == 2:
            change_player_state = ChangePlayer(self.game, self.board.pegs, self.board.game_state.current_player,
                                               self.shared_data, self.board.game_state)
            change_player_state.enter_state()


        if self.shared_data['turn_played']:
            change_player_state = ChangePlayer(self.game, self.board.pegs, self.board.game_state.current_player,
                                               self.shared_data)
            change_player_state.enter_state()

            self.check_for_end_game()

    def update_top_text(self):
        curr_player = self.board.game_state.current_player

        if self.shared_data['turn_played']:
            last_turn = self.board.game_state.last_move
            if curr_player == 2:
                text = f'Player 1 played {last_turn[0]} -> {last_turn[1]}'
                color = player1_color
                turn_text = ''
            else:
                text = f'Player 2 played {last_turn[0]} -> {last_turn[1]}'
                color = self.game.player2_color
                turn_text = ''
        else:
            last_turn = self.board.game_state.last_move
            turn_text = ''
            if curr_player == 1:
                text = 'Player 1 Turn'
                color = player1_color
                if last_turn:
                    turn_text = f'Player 2 played {last_turn[0]} -> {last_turn[1]} last turn'
            else:
                text = 'Player 2 Turn'
                color = self.game.player2_color
                if last_turn:
                    turn_text = f'Player 1 played {last_turn[0]} -> {last_turn[1]} last turn'

        self.player_turn_surf = self.game.gui_font.render(text, True, color)
        self.player_turn_rect = self.player_turn_surf.get_rect(midtop=(self.game.GAME_W >> 1, 30))

        self.last_turn_surf = self.game.gui_font.render(turn_text, True, (0, 0, 0))
        self.last_turn_rect = self.last_turn_surf.get_rect(midtop=(self.game.GAME_W >> 1, 60))

        self.player1_points_surf = self.game.title_font.render(str(self.board.game_state.player_points['player1']),
                                                               True, player1_color)
        self.player1_points_rect = self.player1_points_surf.get_rect(midleft=(15, self.game.GAME_H >> 1))

        self.player2_points_surf = self.game.title_font.render(str(self.board.game_state.player_points['player2']),
                                                               True, self.game.player2_color)
        self.player2_points_rect = self.player2_points_surf.get_rect(
            midright=(self.game.GAME_W - 15, self.game.GAME_H >> 1))

    def check_for_end_game(self):
        player1_pts = self.board.game_state.player_points['player1']
        player2_pts = self.board.game_state.player_points['player2']
        pts_to_win = self.board.game_state.points_to_win
        if player1_pts >= pts_to_win or player2_pts >= pts_to_win:
            from src.states.end_game import EndGame
            new_state = EndGame(self.game, "Player1 wins!" if player1_pts > player2_pts else "Player2 wins!",
                                player1_color if player1_pts > player2_pts else self.game.player2_color)
            new_state.enter_state()
