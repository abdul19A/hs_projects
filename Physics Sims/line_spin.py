import math
import pygame

class Irrational:
    PI = 3.141592653589793
    GR = 1.618033988749894
    EN = 2.718281828459045
    R2 = 1.414213562373095

x = 0
y = 1
def do_color_condition(c):
    if c < 256:
        return c
    elif c < 512:
        return 255
    return 0
def get_color(i):
    r = int(255 * math.sin(math.radians(i)))
    g = int(255 * math.cos(math.radians(i)))
    b = int(255 * -math.sin(math.radians(i)))
    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0
    return pygame.color.Color(r, g, b, 255)

class Line:
    def __init__(self, center_point: list, spin_speed: float, radius: int = 150, color: str = "white", drag_color="yellow"):

        self.angle = -math.pi/2
        self.angle_velocity = -math.radians(spin_speed/3)

        self.p1 = center_point
        self.p2 = [center_point[x] + radius * math.cos(self.angle), center_point[y] + radius * math.sin(self.angle)]

        self.color = color
        self.radius = radius

        self.drag_points = [self.p2]
        self.drag_color = drag_color

    def move(self, new_p1=None):
        if new_p1:
            self.p1 = new_p1

        new_p2_x = self.p1[x] + self.radius * math.cos(self.angle)
        new_p2_y = self.p1[y] + self.radius * math.sin(self.angle)

        self.p2 = [new_p2_x, new_p2_y]

        self.drag_points.append(self.p2)

        self.angle += self.angle_velocity

    def draw(self, window):
        pygame.draw.line(
            surface=window,
            color=self.color,
            start_pos=self.p1,
            end_pos=self.p2,
            width=1
        )

    def draw_drag_points(self, window):
        for index, point1 in enumerate(self.drag_points[:-1]):
            point2 = self.drag_points[index + 1]
            rgb_color = get_color(index)
            pygame.draw.line(surface=window,
                             color=rgb_color,
                             start_pos=point1,
                             end_pos=point2,
                             width=1)


if __name__ == "__main__":
    SCREEN_WIDTH = 1440
    SCREEN_HEIGHT = 720
    SCREEN_FILL = "black"
    CENTER_POINT = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    screen_is_open = True

    clock = pygame.time.Clock()

    line_1 = Line(center_point=CENTER_POINT, spin_speed=1)
    line_2 = Line(center_point=line_1.p2, spin_speed=Irrational.GR)
    while screen_is_open:
        screen.fill(SCREEN_FILL)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_is_open = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    line_1.radius += 5
                elif event.key == pygame.K_DOWN:
                    line_1.radius -= 5
                elif event.key == pygame.K_LEFT:
                    line_2.radius -= 5
                elif event.key == pygame.K_RIGHT:
                    line_2.radius += 5
                elif event.key == pygame.K_r:
                    line_2.drag_points = []
                elif event.key == pygame.K_e:
                    line_1.radius = 150
                    line_2.radius = 150


        line_1.move()
        line_2.move(new_p1=line_1.p2)

        line_2.draw_drag_points(screen)
        line_1.draw(screen)
        line_2.draw(screen)

        clock.tick()
        pygame.display.flip()
