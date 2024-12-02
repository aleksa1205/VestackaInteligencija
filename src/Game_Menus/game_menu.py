import pygame
from src.Functionality.draw import create_graph, create_empty_board, draw_triangles
from src.Functionality.move import make_move, find_triangle
from src import globals as g
from src.Trigle import pocetno_stanje, razvuci_gumicu

def game_menu(n, plays_first):
    screen = pygame.display.get_surface()
    g.n = n
    g.screen = screen
    clock = pygame.time.Clock()
    create_graph()
    pygame.display.set_caption('Triggle')

    print('Game started...')
    print(n, plays_first)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill('#DCDDD8')
        create_empty_board(n)

        make_move((0, 0), (0, 3), n)
        make_move((0, 0), (3, 0), n)
        make_move((0, 0), (3, 3), n)
        make_move((1, 0), (1, 3), n)
        # print(globals.paths)
        # print(globals.graph)
        find_triangle()
        draw_triangles()
        g.change_player()
        make_move((0, 1), (3, 1), g.n)
        find_triangle()
        # print(globals.player1_set)
        # print(globals.player2_set)
        draw_triangles()
        # print(globals.player1_points)
        # print(globals.player2_points)

        pygame.display.update()
        clock.tick(60)