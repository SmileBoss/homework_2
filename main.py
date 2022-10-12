import pygame
import numpy as np

colors = [
    "#000000", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
    "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
    "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
    "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
    "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C"
]


def dist(pnt1, pnt2):
    return np.sqrt((pnt1[0] - pnt2[0]) ** 2 + (pnt1[1] - pnt2[1]) ** 2)


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


def group_neighbors(pnt1, points, groups, flags, eps, g):
    for i, pnt2 in enumerate(points):
        if groups[i] == 0 and dist(pnt1, pnt2) < eps:
            groups[i] = g
            if flags[i] != 'y':
                group_neighbors(pnt2, points, groups, flags, eps, g)


def start():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    running = True

    screen.fill("white")

    pygame.display.update()
    points = paint(screen)

    flags, groups = dbscan(points)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_1:
                    default(screen, points)
                if event.key == pygame.K_2:
                    colorized(screen, points, flags)
                if event.key == pygame.K_3:
                    grouped(screen, points, groups)
            if event.type == pygame.QUIT:
                running = False


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


def default(screen, points):
    screen.fill("white")

    for pnt in points:
        pygame.draw.circle(screen, color='black', center=pnt, radius=10)

    pygame.display.update()


def paint(screen):
    points = []

    painting = True

    while painting:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    points.append(event.pos)
                    pygame.draw.circle(screen, color='black', center=event.pos, radius=10)
                    pygame.display.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return points

            if event.type == pygame.QUIT:
                painting = False


if __name__ == '__main__':
    start()