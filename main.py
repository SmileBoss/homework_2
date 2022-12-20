import pygame
import numpy as np

colors = ["#5a3036", "#eac93c", "#f08077", "#637dac", "#5c8910", "#724ea2", "#b6e2ad", "#bce9f1"]


def dist(pnt1, pnt2):
    return np.sqrt((pnt1[0] - pnt2[0]) ** 2 + (pnt1[1] - pnt2[1]) ** 2)


def is_closest(pnt1, pnt2, points, flags, eps):
    closest = dist(pnt2, pnt1)
    for i, pnt3 in enumerate(points):
        if flags[i] == 'g' and dist(pnt2, pnt3) < eps and dist(pnt2, pnt3) < closest:
            return False
    return True


def group_neighbors(pnt1, points, groups, flags, eps, g):
    for i, pnt2 in enumerate(points):
        if groups[i] == 0 and dist(pnt1, pnt2) < eps:
            groups[i] = g
            if flags[i] != 'y':
                group_neighbors(pnt2, points, groups, flags, eps, g)


def dbscan(points):
    minPts = 3
    eps = 60
    # fill red
    flag = ['r' for _ in range(len(points))]
    # green
    for i, pnt1 in enumerate(points):
        number_pts = 0
        for pnt2 in points:
            if pnt1 != pnt2 and dist(pnt1, pnt2) < eps:
                number_pts += 1
        if number_pts >= minPts:
            flag[i] = 'g'

    # yellow
    for i, pnt1 in enumerate(points):
        if flag[i] != 'g':
            for j, pnt2 in enumerate(points):
                if flag[j] == 'g' and pnt1 != pnt2 and dist(pnt1, pnt2) < eps:
                    flag[i] = 'y'
                    break

    # grouping
    groups = [0 for _ in range(len(points))]
    g = 0
    for i, pnt1 in enumerate(points):
        if flag[i] == 'g' and groups[i] == 0:
            g += 1
            group_neighbors(pnt1, points, groups, flag, eps, g)
    return flag, groups


def grouped(screen, points, groups):
    screen.fill('white')
    for i, pnt in enumerate(points):
        pygame.draw.circle(screen, color=colors[groups[i]], center=pnt, radius=10)
    pygame.display.update()


def colorized(screen, points, flags):
    screen.fill("white")
    for i, pnt in enumerate(points):
        clr = flags[i]
        if clr == 'r':
            clr = 'red'
        elif clr == 'y':
            clr = 'yellow'
        else:
            clr = 'green'
        pygame.draw.circle(screen, color=clr, center=pnt, radius=10)
    pygame.display.update()


def paint(screen):
    points = []

    painting = True
    flags = []
    groups = []

    while painting:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    points.append(event.pos)
                    pygame.draw.circle(screen, color='black', center=event.pos, radius=10)
                    pygame.display.update()

            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_1:
                    flags, groups = dbscan(points)
                    colorized(screen, points, flags)
                if event.key == pygame.K_2:
                    flags, groups = dbscan(points)
                    grouped(screen, points, groups)

            if event.type == pygame.QUIT:
                painting = False


def start():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    running = True

    screen.fill("white")

    pygame.display.update()
    points = paint(screen)


if __name__ == '__main__':
    start()