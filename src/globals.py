from math import sqrt

n = 4
max_number_of_triangles = 3 * n * (n - 1) + 1
x_start = 100
y_start = 100
d = 30
h = d * sqrt(3) / 2
currentPlayer = True
graph = dict()
paths = set()

#player1 / plavi
player1_color = (173, 216, 230)
#su njegovi trouglovi
player1_set = set()
player1_points = 0

#player2 / ai
player2_color = (100, 28, 30)
player2_set = set()
player2_points = 0

def change_player():
    global currentPlayer
    currentPlayer = not currentPlayer