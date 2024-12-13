import os, time, pygame
from pygame import Surface
from pygame.font import Font
from src.states.title import Title

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
        self.funct_dir = os.path.join('functionality')
        self.game_menus_dir = os.path.join('game_menus')
        self.ui_components = os.path.join('ui_components')
        # self.font_dir
        self.gui_font : Font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 100)

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()