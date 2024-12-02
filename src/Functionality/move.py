from src.Functionality.checker import *
from .draw import draw_line
from src import globals as g


def desno(i, j):
    return i, j + 1

def dole_desno(i, j, n):
    return i + 1, j if i >= n-1 else j + 1

def dole_levo(i, j, n):
    return i + 1, j - 1 if i >= n - 1 else j

def make_move(start : tuple, end : tuple,  n):
    if check_length(start, end) is False:
        print("Put nije duzine 4!")
        return

    node_desno = start
    desni = [node_desno]
    node_d_levo = start
    d_levi = [node_d_levo]
    node_d_desno = start
    d_desni = [node_d_desno]

    for i in range(3):
        node_desno = desno(node_desno[0], node_desno[1])
        desni.append(node_desno)
        node_d_levo = dole_levo(node_d_levo[0], node_d_levo[1], n)
        d_levi.append(node_d_levo)
        node_d_desno = dole_desno(node_d_desno[0], node_d_desno[1], n)
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
        return
    draw_line(start, end, n)

def make_move_tournament(start : tuple, move, n):
    node = start
    path = [start]

    for i in range(3):
        if move == 'D':
            node = desno(node[0], node[1])
        elif move == 'DL':
            node = dole_levo(node[0], node[1], n)
        elif move == 'DD':
            node = dole_desno(node[0], node[1], n)
        else:
            #greska
            return None
        path.add(node)
    if in_boundaries(node[0], node[1], n) is False:
        print("Ispali ste iz opsega!")
        return
    #crtanje
    if tuple(path) in g.paths:
        print("Isti put je vec formiran")
        return
    for i, j in zip(path[:-1], path[1:]):
        g.graph[i].add(j)
        g.graph[j].add(i)

    draw_line(start, node, n)

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