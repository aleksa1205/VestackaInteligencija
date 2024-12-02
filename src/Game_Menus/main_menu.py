import pygame
from ..UI_Components import Button
from sys import exit

from ..UI_Components.fonts import title_font


def main_menu():
    # pygame values
    pygame.display.set_caption('Main Menu')
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    screen_width, _ = screen.get_size()

    text_surf = title_font.render('Triggle', True, 'Black')
    text_rect = text_surf.get_rect(midtop = (screen_width / 2, 30))

    play_button = Button('Play', (screen_width / 2, 300), rect_point='center')
    quit_button = Button('Quit', (screen_width / 2, 400), rect_point='center')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill('#DCDDD8')
        screen.blit(text_surf, text_rect)

        play_button.draw()
        quit_button.draw()

        if play_button.check_click():
            from .options_menu import options_menu
            options_menu()

        if quit_button.check_click():
            pygame.quit()
            exit()

        pygame.display.update()
        clock.tick(60)
