import pygame

from src.Trigle import pocetno_stanje, razvuci_gumicu


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

        graf = pocetno_stanje(n)
        razvuci_gumicu((100, 40), (70, 100), graf, 20)
        razvuci_gumicu((120, 40), (90, 100), graf, 20)
        razvuci_gumicu((100, 40), (130, 100), graf, 20)
        razvuci_gumicu((90, 60), (150, 60), graf, 20)
        razvuci_gumicu((100, 40), (160, 40), graf, 20)

        pygame.display.update()
        clock.tick(60)