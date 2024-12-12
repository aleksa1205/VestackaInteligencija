import pygame
from src.states.state import State
from src.states.game_world import GameWorld
from src.UI_Components import Button
from src.UI_Components.colors import pause_menu_color

class PauseMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.text_font = pygame.font.Font(None, 50)
        self.text_surf = self.game.title_font.render('Pause menu', True, 'Black')
        self.text_rect = self.text_surf.get_rect(midtop=(self.game.SCREEN_WIDTH >> 1, 30))

        self.resume_button = Button(self.game, 'Resume', (self.game.SCREEN_WIDTH >> 1, 300), rect_point='center')
        self.restart_button = Button(self.game, 'Restart', (self.game.SCREEN_WIDTH >> 1, 400), rect_point='center')
        self.title_button = Button(self.game, 'Back to title menu', (self.game.SCREEN_WIDTH >> 1, 500), rect_point='center')

    def update(self, delta_time, events):
        if self.resume_button.check_click():
            self.exit_state()
        if self.restart_button.check_click():
            pause_menu = self.exit_state()
            game_world = pause_menu.exit_state()
            new_state = GameWorld(game_world.game, game_world.board_size, game_world.plays_first)
            new_state.enter_state()
        if self.title_button.check_click():
            pause_menu = self.exit_state()
            game_world = pause_menu.exit_state()
            game_world.exit_state()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_state()

    def render(self, surface):
        self.game.game_canvas.fill(pause_menu_color)
        self.game.game_canvas.blit(self.text_surf, self.text_rect)

        self.resume_button.render()
        self.restart_button.render()
        self.title_button.render()