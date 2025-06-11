from src.states.game_config import GameConfig, GameMode
from src.ui_components.colors import whiteish, bg_color
from src.states.game_world import GameWorld
from src.states.state import State
import pygame

from src.ui_components import Button
from src.ui_components.radio_group import RadioGroup

class Options(State):
    def __init__(self, game):
        super().__init__(game)
        pygame.display.set_caption('Options')

        # which surface will be active
        self.ai_surf_active = True
        self.pvp_surf_active = False

        # who will play first
        self.game_config = GameConfig()

        self.text_surf = self.game.title_font.render('Options', True, 'Black')
        self.text_rect = self.text_surf.get_rect(midtop=(self.game.GAME_W >> 1, 30))

        options_surface_size = (300, 200)
        surf_color = (210, 210, 210)

        self.ai_surf = pygame.Surface(options_surface_size)
        self.ai_surf.fill(surf_color)
        ai_rect_pos = ((self.game.GAME_W >> 1) - 300, 200)
        self.ai_rect = self.ai_surf.get_rect(midtop=ai_rect_pos)
        self.ai_button = Button(self.game, 'Play against AI', ai_rect_pos, rect_point='midbottom')

        self.player_first_ai_button = Button(self.game, 'Player first', ((self.game.GAME_W >> 1) - 300, 250), rect_point='midbottom')
        self.ai_first_button = Button(self.game, 'AI first', ((self.game.GAME_W >> 1) - 300, 300), rect_point='midbottom')

        self.pvp_surf = pygame.Surface(options_surface_size)
        self.pvp_surf.fill(surf_color)
        pvp_rect_pos = ((self.game.GAME_W >> 1) + 300, 200)
        self.pvp_surf_rect = self.pvp_surf.get_rect(midtop=pvp_rect_pos)
        self.pvp_button = Button(self.game, 'Play against another player', pvp_rect_pos, 300, 40, rect_point='midbottom')

        self.player_first_pvp_button = Button(self.game, 'Player 1 first', ((self.game.GAME_W >> 1) + 300, 250), rect_point='midbottom')
        self.enemy_first_button = Button(self.game, 'Player 2 first', ((self.game.GAME_W >> 1) + 300, 300), rect_point='midbottom')

        self.radio_group = RadioGroup([self.ai_button, self.pvp_button])
        self.game_config_group = RadioGroup(
            [self.player_first_ai_button, self.ai_first_button, self.player_first_pvp_button, self.enemy_first_button])
        self.radio_group.set_active(self.ai_button)
        self.game_config_group.set_active(self.player_first_ai_button)

        # grid size option
        self.grid_buttons = []
        for i in range(5):
            self.grid_buttons.append(Button(self.game, f'{i + 4}', (520 + (i * 50), 500), width=40, height=40, value=i + 4))

        self.grid_buttons_group = RadioGroup(self.grid_buttons)
        self.grid_buttons_group.set_active(self.grid_buttons[0])

        # Final buttons
        self.back_btn = Button(self.game, 'Back', ((self.game.GAME_W >> 1) - 200, 600), rect_point='midtop')
        self.play_btn = Button(self.game, 'Play', ((self.game.GAME_W >> 1) + 200, 600), rect_point='midtop')

    def update(self, delta_time, events):
        if self.ai_button.check_click():
            self.ai_surf_active = True
            self.pvp_surf_active = False
            self.radio_group.set_active(self.ai_button)
        if self.pvp_button.check_click():
            self.pvp_surf_active = True
            self.ai_surf_active = False
            self.radio_group.set_active(self.pvp_button)

        if self.player_first_pvp_button.check_click():
            self.game_config_group.set_active(self.player_first_pvp_button)
            self.game_config.mode = GameMode.PVP
            self.game_config.current_player = 1
        if self.player_first_ai_button.check_click():
            self.game_config_group.set_active(self.player_first_ai_button)
            self.game_config.mode = GameMode.P_VS_AI
            self.game_config.current_player = 1
        if self.ai_first_button.check_click():
            self.game_config_group.set_active(self.ai_first_button)
            self.game_config.mode = GameMode.P_VS_AI
            self.game_config.current_player = 2
        if self.enemy_first_button.check_click():
            self.game_config_group.set_active(self.enemy_first_button)
            self.game_config.mode = GameMode.PVP
            self.game_config.current_player = 2

        if self.back_btn.check_click():
            self.exit_state()
        if self.play_btn.check_click():
            active_button = self.grid_buttons_group.get_active()
            self.game_config.board_size = active_button.value
            new_state = GameWorld(self.game, self.game_config)
            new_state.enter_state()

    def render(self, surface):
        self.game.game_canvas.fill(bg_color)
        self.game.game_canvas.blit(self.text_surf, self.text_rect)
        self.ai_button.render()
        self.pvp_button.render()

        if self.ai_surf_active:
            self.game.game_canvas.blit(self.ai_surf, self.ai_rect)
            self.player_first_ai_button.render()
            self.ai_first_button.render()
        if self.pvp_surf_active:
            self.game.game_canvas.blit(self.pvp_surf, self.pvp_surf_rect)
            self.player_first_pvp_button.render()
            self.enemy_first_button.render()

        # grid buttons
        for btn in self.grid_buttons:
            btn.render()
            if btn.check_click():
                self.grid_buttons_group.set_active(btn)

        # Back and play buttons
        self.back_btn.render()
        self.play_btn.render()