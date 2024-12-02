import pygame
from sys import exit

from .game_menu import game_menu
from ..UI_Components import Button
from ..UI_Components.fonts import title_font
from ..UI_Components.radio_group import RadioGroup


def options_menu():
    clock = pygame.time.Clock()
    pygame.display.set_caption('Options')
    screen = pygame.display.get_surface()
    screen_width, _ = screen.get_size()

    # which surface will be active
    ai_surf_active = True
    pvp_surf_active = False

    # who will play first
    plays_fist = ['ai', 'player']

    text_surf = title_font.render('Options', True, 'Black')
    text_rect = text_surf.get_rect(midtop = (screen_width / 2, 30))

    options_surface_size = (300, 200)
    surf_color = (210, 210, 210)

    ai_surf = pygame.Surface(options_surface_size)
    ai_surf.fill(surf_color)
    ai_rect_pos = ((screen_width / 2) - 300, 200)
    ai_rect = ai_surf.get_rect(midtop = ai_rect_pos)
    ai_button = Button('Play against AI', ai_rect_pos, rect_point='midbottom')

    player_first_ai_button = Button('Player first', ((screen_width / 2) - 300, 250), rect_point='midbottom')
    ai_first_button = Button('AI first', ((screen_width / 2) - 300, 300), rect_point='midbottom')

    pvp_surf = pygame.Surface(options_surface_size)
    pvp_surf.fill(surf_color)
    pvp_rect_pos = ((screen_width / 2) + 300, 200)
    pvp_surf_rect = pvp_surf.get_rect(midtop = pvp_rect_pos)
    pvp_button = Button('Play against another player', pvp_rect_pos, 300, 40, rect_point='midbottom')

    player_first_pvp_button = Button('Player first', ((screen_width / 2) + 300, 250), rect_point='midbottom')
    enemy_first_button = Button('Enemy first', ((screen_width / 2) + 300, 300), rect_point='midbottom')

    radio_group = RadioGroup([ai_button, pvp_button])
    plays_first_group = RadioGroup([player_first_ai_button, ai_first_button, player_first_pvp_button, enemy_first_button])
    radio_group.set_active(ai_button)
    plays_first_group.set_active(player_first_ai_button)

    # grid size option
    grid_buttons = []
    for i in range(5):
        grid_buttons.append(Button(f'{i + 4}', (520 + (i * 50), 500), width=40, height=40, value = i + 4))

    grid_buttons_group = RadioGroup(grid_buttons)
    grid_buttons_group.set_active(grid_buttons[0])

    # Final buttons
    back_btn = Button('Back', (screen_width / 2 - 200, 600), rect_point='midtop')
    play_btn = Button('Play', (screen_width / 2 + 200, 600), rect_point='midtop')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill('#DCDDD8')
        screen.blit(text_surf, text_rect)
        ai_button.draw()
        pvp_button.draw()

        if ai_button.check_click():
            ai_surf_active = True
            pvp_surf_active = False
            radio_group.set_active(ai_button)
        if pvp_button.check_click():
            pvp_surf_active = True
            ai_surf_active = False
            radio_group.set_active(pvp_button)

        if ai_surf_active:
            screen.blit(ai_surf, ai_rect)
            player_first_ai_button.draw()
            ai_first_button.draw()
        if pvp_surf_active:
            screen.blit(pvp_surf, pvp_surf_rect)
            player_first_pvp_button.draw()
            enemy_first_button.draw()

        if player_first_pvp_button.check_click():
            plays_first_group.set_active(player_first_pvp_button)
            plays_fist = ['pvp', 'player']
        if player_first_ai_button.check_click():
            plays_first_group.set_active(player_first_ai_button)
            plays_fist = ['ai', 'player']
        if ai_first_button.check_click():
            plays_first_group.set_active(ai_first_button)
            plays_fist = ['ai', 'enemy']
        if enemy_first_button.check_click():
            plays_first_group.set_active(enemy_first_button)
            plays_fist = ['pvp', 'enemy']

        # grid buttons
        for btn in grid_buttons:
            btn.draw()
            if btn.check_click():
                grid_buttons_group.set_active(btn)

        # Back and play buttons
        back_btn.draw()
        play_btn.draw()

        if back_btn.check_click():
            from .main_menu import main_menu
            main_menu()
        if play_btn.check_click():
            buton = grid_buttons_group.get_active()
            game_menu(buton.value, plays_fist)

        pygame.display.update()
        clock.tick(60)