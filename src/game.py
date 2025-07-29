import os, time, pygame
from pygame import Surface
from pygame.font import Font
from src.states.title import Title
from src.ui_components.colors import player2_color_const

class Game:
    def __init__(self):
        pygame.init()
        self.GAME_W, self.GAME_H = 1280, 720
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
        self.game_canvas : Surface = Surface((self.GAME_W, self.GAME_H), pygame.SRCALPHA)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.clock = pygame.time.Clock()
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.player2_color = player2_color_const
        self.load_assets()
        self.load_states()

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False


    def update(self):
        self.state_stack[-1].update(self.dt, self.events)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))

        pygame.display.update()
        self.clock.tick(244)

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surf = self.font.render(text, True, color)
        #text_surf.setcolorkey((0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surf, text_rect)

    def load_assets(self):
        # self.font_dir
        base_dir = os.path.dirname(os.path.abspath(__file__))  # This gives the src directory

        motion_control = os.path.join(base_dir, '../resources/Fonts/MotionControl-Bold.otf')
        roboto_black = os.path.join(base_dir, '../resources/Fonts/Roboto-Black.ttf')
        roboto_light = os.path.join(base_dir, '../resources/Fonts/Roboto-Bold.ttf')
        self.gui_font = pygame.font.Font(motion_control, 27)
        self.title_font = pygame.font.Font(motion_control, 100)

        # sounds
        button_click = os.path.join(base_dir, '../resources/Sounds/button_click.mp3')
        self.button_click_sound = pygame.mixer.Sound(button_click)
        self.button_click_sound.set_volume(0.3)
        rubber_band = os.path.join(base_dir, '../resources/Sounds/rubber_band_sound.mp3')
        self.rubber_band_sound = pygame.mixer.Sound(rubber_band)
        self.rubber_band_sound.set_volume(0.3)
        error = os.path.join(base_dir, '../resources/Sounds/error.mp3')
        self.error_sound = pygame.mixer.Sound(error)
        self.error_sound.set_volume(0.3)
        win1 = os.path.join(base_dir, '../resources/Sounds/win.wav')
        win2 = os.path.join(base_dir, '../resources/Sounds/win2.wav')
        self.win_sound = pygame.mixer.Sound(win1)
        self.win_sound.set_volume(0.3)
        lose = os.path.join(base_dir, '../resources/Sounds/lose.wav')
        self.lose_sound = pygame.mixer.Sound(lose)
        self.lose_sound.set_volume(0.3)
        success = os.path.join(base_dir, '../resources/Sounds/success.mp3')
        self.success_sound = pygame.mixer.Sound(success)
        self.success_sound.set_volume(0.3)

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()