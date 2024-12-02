import pygame

def game_menu(n, plays_first):
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Triggle')

    print('Game started...')
    print(n, plays_first)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill('#DCDDD8')

        pygame.display.update()
        clock.tick(60)