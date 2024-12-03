import pygame
from .checker import *
from .draw import draw_line, draw_triangles
from src import globals as g

screen = pygame.display.get_surface()

def desno(coordinates):
    return coordinates[0], coordinates[1] + 1

def dole_desno(coordinates):
    x = coordinates[0]
    y = coordinates[1]
    return x + 1, y if x >= g.n - 1 else y + 1

def dole_levo(coordinates):
    x = coordinates[0]
    y = coordinates[1]
    return x + 1, y - 1 if x >= g.n - 1 else y

def make_move(start : tuple, end : tuple):
    if check_length(start, end) is False:
        print("Put nije duzine 3!")
        return

    node_desno = start
    desni = [node_desno]
    node_d_levo = start
    d_levi = [node_d_levo]
    node_d_desno = start
    d_desni = [node_d_desno]

    for i in range(3):
        node_desno = desno(node_desno)
        desni.append(node_desno)
        node_d_levo = dole_levo(node_d_levo)
        d_levi.append(node_d_levo)
        node_d_desno = dole_desno(node_d_desno)
        d_desni.append(node_d_desno)

    if node_desno == end:
        path = tuple(desni)
        if path in g.paths:
            print("Isti put je vec formiran!")
        g.paths.add(path)
        for i, j in zip(desni[:-1],desni[1:]):
            g.graph[i].add(j)
            g.graph[j].add(i)
    elif node_d_levo == end:
        path = tuple(d_levi)
        if path in g.paths:
            print("Isti put je vec formiran!")
        g.paths.add(path)
        for i, j in zip(d_levi[:-1], d_levi[1:]):
            g.graph[i].add(j)
            g.graph[j].add(i)
    elif node_d_desno == end:
        path = tuple(d_desni)
        if path in g.paths:
            print("Isti put je vec formiran!")
        g.paths.add(path)
        for i, j in zip(d_desni[:-1], d_desni[1:]):
            g.graph[i].add(j)
            g.graph[j].add(i)
    else:
        return False
    draw_line(start, end)
    find_triangle()
    draw_triangles()
    return True

def make_move_tournament(start : tuple, move):
    node = start
    path = [start]

    for i in range(3):
        if move == 'D':
            node = desno(node)
        elif move == 'DL':
            node = dole_levo(node)
        elif move == 'DD':
            node = dole_desno(node)
        else:
            #greska
            return None
        path.append(node)

    if in_boundaries(node) is False:
        print("Ispali ste iz opsega!")
        return
    #crtanje
    if tuple(path) in g.paths:
        print("Isti put je vec formiran")
        return
    for i, j in zip(path[:-1], path[1:]):
        g.graph[i].add(j)
        g.graph[j].add(i)

    draw_line(start, node)
    find_triangle()
    draw_triangles()

def find_triangle():
    for node in g.graph:
        neighbors = list(g.graph[node])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] in g.graph[neighbors[i]]:
                    #prvo proverimo da li je dati ciklus u nekom od setova
                    cycle = tuple(sorted((node, neighbors[i], neighbors[j])))
                    # print(globals.player1_set)
                    # print(globals.player2_set)
                    # print(cycle)
                    if tuple(cycle) not in g.player1_set and tuple(cycle) not in g.player2_set:
                        g.player1_set.add(cycle) if g.currentPlayer else g.player2_set.add(cycle)