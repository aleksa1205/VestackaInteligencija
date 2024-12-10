from src.states.options import Options
from src.states.state import State
from src.ui_components import Button
import pygame

class Title(State):
    def __init__(self, game):
        super().__init__(game)

        pygame.display.set_caption('Main Menu')
        self.text_surf = self.game.title_font.render('Triggle', True, 'Black')
        self.text_rect = self.text_surf.get_rect(midtop=(self.game.SCREEN_WIDTH >> 1, 30))

        self.play_button = Button(self.game, 'Play', (self.game.SCREEN_WIDTH >> 1, 300), rect_point='center')
        self.quit_button = Button(self.game,'Quit', (self.game.SCREEN_WIDTH >> 1, 400), rect_point='center')

    def update(self, delta_time):
        if self.play_button.check_click():
            new_state = Options(self.game)
            new_state.enter_state()

        if self.quit_button.check_click():
            self.game.playing = False
            self.game.running = False
    def render(self, surface):
        self.game.game_canvas.fill('#DCDDD8')
        self.game.game_canvas.blit(self.text_surf, self.text_rect)

        self.play_button.render()
        self.quit_button.render()

