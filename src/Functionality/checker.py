from src import globals as g

def in_boundaries(i, j, size):
    #nevalidan potez
    if i < 0 or j < 0:
        return False
    #ispao dole
    if i >= 2 * size - 1:
        return False
    #ispao desno
    if j >= 2 * size - 1 - abs(size - 1 - i):
        return False
    return True

def check_length(stub1 : tuple, stub2 : tuple):
    x = abs(stub2[0] - stub1[0])
    y = abs(stub2[1] - stub1[1])
    return True if x==3 or y==3 else False

def end_game():
    if g.player1_points > g.max_number_of_triangles / 2:
        print("Pobedio je prvi igrac")
        return True
    elif g.player2_points > g.max_number_of_triangles / 2:
        print("Pobedio je drugi igrac")
        return True
    else:
        return False