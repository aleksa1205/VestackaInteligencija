import pygame
from ..Functionality.draw import create_graph, create_empty_board, draw_triangles
from ..Functionality.move import make_move, find_triangle
from .. import globals as g

def game_menu(n, plays_first):
    g.n = n
    screen = pygame.display.get_surface()
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
        create_empty_board()

        make_move((0, 0), (0, 3))
        make_move((0, 0), (3, 0))
        make_move((0, 0), (3, 3))
        make_move((1, 0), (1, 3))
        # print(globals.paths)
        # print(globals.graph)
        g.change_player()
        make_move((0, 1), (3, 1))
        # print(globals.player1_set)
        # print(globals.player2_set)
        # print(globals.player1_points)
        # print(globals.player2_points)

        pygame.display.update()
        clock.tick(60)