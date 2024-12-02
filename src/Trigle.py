import pygame
import math

koordinate = []
win = pygame.display.get_surface()

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
    return koordinate

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

def razvuci_gumicu(stub1, stub2, graf, space):
    #c1 i c2 su stubici izmedju koji moraju da se uzmu u obzir
    if validan_potez(stub1, stub2, space):
        if proveri_pravac(stub1, stub2, space) == "D":
            c1 = ((stub1[0]+space), stub1[1])
            c2 = ((stub1[0] + 2* space), stub1[1])
        if proveri_pravac(stub1, stub2, space) == "DL":
            c1=((stub1[0]-(space//2)), (stub1[1]+space))
            c2=((stub1[0]-space), (stub1[1]+2*space))
        if proveri_pravac(stub1, stub2, space) == "DD":
            c1=((stub1[0]+(space//2)), (stub1[1]+space))
            c2 = ((stub1[0] + space), (stub1[1] + 2 * space))
        graf[stub1].append(c1)
        graf[c1].append(stub1)
        graf[c1].append(c2)
        graf[c2].append(c1)
        graf[c2].append(stub2)
        graf[stub2].append(c2)

        pygame.draw.line(win, BLACK, stub1, c1, 2)
        pygame.draw.line(win, BLACK, c1, c2, 2)
        pygame.draw.line(win, BLACK, c2, stub2, 2)

        detektuj_trougao(stub1, c1, graf, 20)
        detektuj_trougao(c1, c2, graf, 20)
        detektuj_trougao(c2, stub2, graf, 20)

def detektuj_trougao(stub1, stub2, graf, space):
    if stub1 in graf[stub2]:
        for stub3 in graf[stub1]:
            if stub3 in graf[stub2] and stub3 != stub1:
                pygame.draw.polygon(win, RED, [stub1, stub2, stub3])
                return True
    return False

def pocetno_stanje(n):
    space = 20
    start = 100
    nacrtaj_tablu(n, space, start)
    graf = napravi_graf(koordinate)
    return graf

#ova treba da se zavrsi, uzeto je u obzir samo kad su svi formirani ali nmg vise glavobolja <3
def kraj_igre(graf):
    for i in graf:
        if len(graf[i]) == 3:
            print("Svi troulici su formirani.")
            return True


screen = WIDTH, HEIGHT = 600, 600

WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLACK = (12, 12, 12)

# pygame.init()
#
# win = pygame.display.set_mode(screen)
# running = True
# while running:
#     win.fill(WHITE)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     graf = pocetno_stanje(4)
#     razvuci_gumicu((100, 40), (70, 100), graf, 20)
#     razvuci_gumicu((120, 40), (90, 100), graf, 20)
#     razvuci_gumicu((100, 40), (130, 100), graf, 20)
#     razvuci_gumicu((90, 60), (150, 60), graf, 20)
#     razvuci_gumicu((100, 40), (160, 40), graf, 20)
#
#     pygame.display.update()
#
# pygame.quit()