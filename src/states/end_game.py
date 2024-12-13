from src.states.state import State
from src.ui_components.button import Button
from src.ui_components.colors import menu_color

class EndGame(State):
    def __init__(self, game, text, color):
        super().__init__(game)
        self.text_surf = self.game.title_font.render(text, True, color)
        self.text_rect = self.text_surf.get_rect(midtop=(self.game.SCREEN_WIDTH >> 1, 30))

        self.play_again = Button(self.game, 'Play again', (self.game.SCREEN_WIDTH >> 1, 300), rect_point='center')
        self.quit_button = Button(self.game, 'Quit game', (self.game.SCREEN_WIDTH >> 1, 400), rect_point='center')

    def update(self, delta_time, events):
        if self.play_again.check_click():
            end_game = self.exit_state()
            end_game.exit_state()
        if self.quit_button.check_click():
            self.game.playing = False
            self.game.running = False

    def render(self, surface):
        self.game.game_canvas.fill(menu_color)
        self.game.game_canvas.blit(self.text_surf, self.text_rect)

        self.play_again.render()
        self.quit_button.render()