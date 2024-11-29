import pygame
import math

def nacrtaj_tablu(x, space, start):
    c = 1
    r = 0
    n = x
    p = start
    q = space
    i = x+1
    t = 2*x-1
    z = 0
    z1 = 0
    h=(x-2)*10
    p1 = start - h
    koordinate = []

    while n != 2*x-1:
        while r != 2*x-1:
            q = q + space
            if i == ( 2*x + 1):
                while c != t:
                    koordinate.append((p1, q))
                    pygame.draw.circle(win, BLACK, (p1, q), 2)
                    c += 1
                    p1 += space
                z1 = z1 + (space//2)
                p1 = (start-h)+z1
                c = 1
                t -= 1
                r += 1
            else:
                while c != i:
                    koordinate.append((p, q))
                    pygame.draw.circle(win, BLACK, (p, q), 2)
                    c += 1
                    p += space
                z = z + (space//2)
                p = start - z
                c = 1
                i += 1
                r += 1
        n += 1

    graf = napravi_graf(koordinate)
    return graf, koordinate

def napravi_graf(koordinate):
    graf = { }
    for k in koordinate:
        graf[k]=[]
    return graf

#t je ovde nabodena vrednost znaci
def proveri_duzinu(stub1, stub2, space, t=8):
    x1, y1 = stub1
    x2, y2 = stub2

    udaljenost = math.sqrt((x2-x1)**2+(y2-y1)**2)

    if abs(udaljenost - 3*space) <= t:
        return True
    return False

def proveri_pravac(stub1, stub2, space):
     x1, y1 = stub1
     x2, y2 = stub2

     if y1==y2 and abs(x1-x2)==3*space:
         return "D"
     if x2 == (x1-3*(space//2)) and y2 == (y1+3*space):
         return "DL"
     if x2 == (x1+3*(space//2)) and y2 == (y1+3*space):
         return "DD"
     return None

def validan_potez(stub1, stub2, space):
    if not proveri_duzinu(stub1, stub2, space):
        return False
    if not proveri_pravac(stub1, stub2, space):
        return False
    return True

print(validan_potez((100, 40), (60, 100), 20))

screen = WIDTH, HEIGHT = 600, 600

WHITE = (255, 255, 255)
BLACK = (12, 12, 12)

pygame.init()

win = pygame.display.set_mode(screen)
running = True
while running:
    win.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    nacrtaj_tablu(6, 20, 100)
    pygame.display.update()

pygame.quit()