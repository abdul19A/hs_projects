import pygame
import math
from Utilities import text

class Wire:
    LENGTH = 100
    WIDTH = 20
    COLOR = "gray"
    all = []

    def __init__(self, x, y, x2=None, y2=None):
        self.x_start, self.y_start = x, y
        self.x_end, self.y_end = (x, y+100) if not(x2 and y2) else (x2, y2)
        self.current = None
        self.resistance = None
        Wire.all.append(self)

    def draw(self, surface):
        pygame.draw.line(
            surface=surface,
            color=Wire.COLOR,
            start_pos=(self.x_start, self.y_start),
            end_pos=(self.x_end, self.y_end),
            width=Wire.WIDTH
        )
        pygame.draw.circle(
            surface=surface,
            color=Wire.COLOR,
            center=(self.x_start, self.y_start),
            radius=Wire.WIDTH//2 + 1
        )
        pygame.draw.circle(
            surface=surface,
            color=Wire.COLOR,
            center=(self.x_end, self.y_end),
            radius=Wire.WIDTH//2 + 1
        )

    def drag(self, mx, my):
        if math.dist((mx, my), (self.x_start, self.y_start)) <= Wire.WIDTH:
            self.x_start, self.y_start = mx, my
        elif math.dist((mx, my), (self.x_end, self.y_end)) <= Wire.WIDTH:
            self.x_end, self.y_end = mx, my

    def connected_to(self, wire):
        p1, p2 = (self.x_start, self.y_start), (self.x_end, self.y_end)
        p1w, p2w = (wire.x_start, wire.y_start), (wire.x_end, wire.y_end)
        for point in (p1w, p2w):
            if math.dist(p1, point) <= Wire.WIDTH:
                return p1, point

            elif math.dist(p2, point) <= Wire.WIDTH:
                return p2, point
        return None

    @staticmethod
    def draw_all(surface):
        for each in Wire.all:
            each.draw(surface)

    @staticmethod
    def drag_all(mx, my):
        for each in Wire.all:
            each.drag(mx, my)


class Battery(Wire):
    WIDTH = 40
    HEIGHT = 80
    END_WIDTH = 8
    END_HEIGHT = 4
    COLOR_POS = "black"
    COLOR_NEG = "orange"
    COLOR_END = "gray"
    all = []

    def __init__(self, x, y, voltage, internal_resistance=1):
        super().__init__(x, y-Battery.HEIGHT/2, x, y+Battery.HEIGHT/2)
        self.x, self.y = x, y
        self.voltage = voltage
        self.internal_resistance = internal_resistance
        self.current = self.voltage/self.internal_resistance
        self.text1 = text.Text("+", (x, y-Battery.HEIGHT/2 + 10))
        self.text2 = text.Text("-", (x, y+Battery.HEIGHT/2 - 10))

    def draw(self, surface):
        rect = pygame.Rect
        pygame.draw.rect(
            surface=surface,
            color=Battery.COLOR_NEG,
            rect=rect(self.x - Battery.WIDTH/2, self.y - Battery.HEIGHT/2, Battery.WIDTH, Battery.HEIGHT/2)
        )
        pygame.draw.rect(
            surface=surface,
            color=Battery.COLOR_POS,
            rect=rect(self.x - Battery.WIDTH/2, self.y, Battery.WIDTH, Battery.HEIGHT/2)
        )
        pygame.draw.rect(
            surface=surface,
            color=Battery.COLOR_END,
            rect=rect(self.x - Battery.END_WIDTH/2, self.y - Battery.HEIGHT/2 - Battery.END_HEIGHT, Battery.END_WIDTH, Battery.END_HEIGHT)
        )
        self.text1.draw(surface)
        self.text2.draw(surface)
    def drag(self, mx, my):
        return
class Main:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.Clock()
        self.bg_color = "blue"
        self.fps = 120
        self.is_running = True
        self.is_dragging = False

    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.is_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_dragging = False

    def drag(self):
        if self.is_dragging:
            mx, my = pygame.mouse.get_pos()
            Wire.drag_all(mx, my)

    def run(self):
        w1 = Wire(100, 100)
        b1 = Battery(300, 300, 10)

        while self.is_running:
            self.surface.fill(self.bg_color)
            self.inputs()
            self.drag()
            Wire.draw_all(self.surface)
            print(b1.connected_to(w1))
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == "__main__":
    new = Main(800, 600)
    new.run()
