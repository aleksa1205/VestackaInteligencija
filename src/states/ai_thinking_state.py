import pygame
import math
from src.states.state import State
from src.ui_components.colors import ai_color  # make sure this is defined


def lerp_color(color1, color2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(color1, color2))


class AIThinkingState(State):
    def __init__(self, game, shared_data):
        super().__init__(game)
        self.font = self.game.gui_font
        self.base_text = "AI is thinking"
        self.shared_data = shared_data

        self.dot_count = 0
        self.last_dot_update = pygame.time.get_ticks()
        self.dot_interval_ms = 500
        self.elapsed_since_start = 0

        self.color_start_time = pygame.time.get_ticks()
        self.bounce_speed = 2.5  # adjust speed of bounce
        self.base_color = ai_color
        self.target_color = (255, 255, 255)  # or (0, 0, 0) for black

    def update(self, delta_time, events):
        if self.shared_data['ai_move_ready']:
            self.exit_state()

        now = pygame.time.get_ticks()

        # Dots animation
        if now - self.last_dot_update >= self.dot_interval_ms:
            self.last_dot_update = now
            self.dot_count = (self.dot_count + 1) % 4

        # Time for color oscillation
        self.elapsed_since_start = (now - self.color_start_time) / 1000.0

    def render(self, surface):
        if self.prev_state:
            self.prev_state.render(surface)

        # Compute t using sine wave
        t = (math.sin(self.elapsed_since_start * self.bounce_speed) + 1) / 2
        color = lerp_color(self.base_color, self.target_color, t)

        # Create text
        text_str = self.base_text + "." * self.dot_count
        text_surface = self.font.render(text_str, True, color)
        text_rect = text_surface.get_rect(midleft=(surface.get_width() - 250, surface.get_height() // 2))

        surface.blit(text_surface, text_rect)
