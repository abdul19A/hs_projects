import pygame
import random
win_x = 800
win_y = 600
mid_point = 400, 300
def get_midpoint(p1, p2):
    x = p1[0] + (p2[0] - p1[0])/2
    y = p1[1] + (p2[1] - p1[1])/2
    return x, y
class cool_triangle:
    def __init__(self, p1, p2, p3, color="yellow", num_points=100):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.num_points = num_points
        self.color = color
        self.points = self.create_points()

    def create_points(self) -> tuple:
        x1, y1 = self.p1
        x2, y2 = self.p2
        x3, y3 = self.p3
        all_points = []
        r1, r2 = random.random(), random.random()
        if r1 + r2 > 1:
            r1 = 1 - r1
            r2 = 1 - r2
        x = (1 - r1 - r2)*x1 + r1*x2 + r2*x3
        y = (1 - r1 - r2)*y1 + r1*y2 + r2*y3
        start_point = (x, y)
        for _ in range(self.num_points):
            corner = random.choice((self.p1, self.p2, self.p3))
            start_point = get_midpoint(start_point, corner)
            all_points.append(start_point)
        return tuple(all_points)

    def do_cool_operation(self, surface):
        for point in self.points:
            x, y = point
            surface.set_at((round(x), round(y)), self.color)

    def draw(self, surface):
        pygame.draw.polygon(
            surface=surface,
            color=self.color,
            points=(self.p1, self.p2, self.p3),
            width=1
        )

def main():
    screen = pygame.display.set_mode((win_x, win_y))
    clock = pygame.Clock()
    tri = cool_triangle(p1=(150, 500), p2=(650, 500), p3=(400, 100), num_points=100000)
    tri.create_points()
    run = True
    while run:
        screen.fill("black")
        for event in pygame.event.get():
            if event == pygame.QUIT:
                run = False
        tri.draw(surface=screen)
        tri.do_cool_operation(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
