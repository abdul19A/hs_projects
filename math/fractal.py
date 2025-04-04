from math import sin, cos, pi, dist
import pygame

class fract:
    n = 20
    all = []

    def __init__(self, pos, rad, angle):
        self.angle = angle
        self.pos = pos
        self.rad = rad
        self.p1 = pos
        self.p2 = (pos[0] + rad * cos(angle), pos[1] + rad * sin(angle))
        fract.all.append(self)

    @staticmethod
    def draw_all(win):
        for each in fract.all:
            width = int(dist(each.p1, each.p2)/10 + 1)
            pygame.draw.line(
                surface=win,
                color="yellow",
                start_pos=each.p1,
                end_pos=each.p2,
                width=width
            )

    @staticmethod
    def something_cool():
        fract.all = []
        num = 0
        prev_iteration_all = [fract(pos=(400, 500), rad=50, angle=-pi/2)]
        # now i will do this 90 - 180/ (2 + n)
        for i in range(fract.n):
            new_one = []
            for j, each_fract in enumerate(prev_iteration_all):
                new_one.append(
                    fract(each_fract.p2, each_fract.rad * 0.9 + 0.1, each_fract.angle - pi/10)
                )
                new_one.append(
                    fract(each_fract.p2, each_fract.rad * 0.9 + 0.1, each_fract.angle + pi/10)
                )
                num += 2
            prev_iteration_all = new_one.copy()

        """fract(pos=(400, 400),
              rad= 50,
              angle=-pi/2)
        for i in range(fract.n):
            fractal = fract.all[i]
            fract(fractal.p3, 50, fractal.final_angle - pi/8)"""
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

fract.n = 0
fract.something_cool()
run = True
while run:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            fract.n += 1
            fract.something_cool()
    fract.draw_all(screen)
    pygame.display.flip()
    clock.tick(60)
