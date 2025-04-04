import time
import pygame
from Utilities import text
import math

class cool_set:
    WINDOW_SIZE = 500
    ZERO_P = (WINDOW_SIZE/2, WINDOW_SIZE/2)
    GRAPH_SIZE = 2

    def __init__(self):

        pygame.init()
        self.surface = pygame.display.set_mode((cool_set.WINDOW_SIZE, cool_set.WINDOW_SIZE))
        self.clock = pygame.Clock()
        self.fps = 60
        self.lines = cool_set.get_intercept_lines()
        self.selected_point = None
        self.is_running = True
        self.text = text.Text("(0,0)", cool_set.ZERO_P, "black")
        self.points = []
        self.keep_points = []
        self.away_points = []
        self.run()

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        mp = pygame.mouse.get_pos()
        if mp is not None:
            tmp = cool_set.window_to_graph(*mp)
            self.text.center = mp
            self.text.text = f"{tmp[0]:.2f}, {tmp[1]:.2f}i"
            self.selected_point = tmp
            self.iterate(50)
            self.text.update_text()

    def iterate(self, num_iter):
        num = self.selected_point[0] + (self.selected_point[1] * 1j)
        startnum = num
        self.points = []
        for _ in range(num_iter):
            self.points.append(num)
            try:

                num = num ** 2 + startnum

                if abs(num) > 2:
                    self.points.append(num)
                    return
            except Exception as e:
                print(e)
                return

    def draw_points(self):
        if len(self.points) < 2:
            return
        new = []
        for point in self.points:
            x, y = cool_set.graph_to_window(point.real, point.imag)
            new.append((x, y))
            pygame.draw.circle(
                surface=self.surface,
                color="black",
                center=(x, y),
                radius=2
            )
        pygame.draw.lines(
            surface=self.surface,
            color="blue",
            closed=False,
            points=new
        )

    def get_keep_points(self):
        if len(self.points) < 2:
            return
        if abs(self.points[-1]) > 2:
            self.keep_points.append(self.points[0])
        else:
            self.away_points.append(self.points[0])

    def draw_keep_points(self):
        for point in self.keep_points:
            x, y = cool_set.graph_to_window(point.real, point.imag)
            pygame.draw.circle(
                surface=self.surface,
                color="red",
                center=(x, y),
                radius=2
            )
        for point in self.away_points:
            x, y = cool_set.graph_to_window(point.real, point.imag)
            pygame.draw.circle(
                surface=self.surface,
                color="purple",
                center=(x, y),
                radius=2
            )

    def run(self):
        while self.is_running:
            self.surface.fill("white")
            self.draw_lines("black")
            self.handle_inputs()
            self.text.draw(self.surface)
            self.draw_points()
            self.get_keep_points()
            self.draw_keep_points()

            self.clock.tick(self.fps)
            pygame.display.flip()

    def draw_lines(self, color):
        for p1, p2 in self.lines:
            pygame.draw.line(
                surface=self.surface,
                color=color,
                start_pos=p1,
                end_pos=p2
            )

    @staticmethod
    def window_to_graph(x, y):
        gs = cool_set.GRAPH_SIZE
        ws = cool_set.WINDOW_SIZE/2
        ratio = gs/ws
        x -= ws
        y -= ws
        y *= -ratio
        x *= ratio
        return x, y

    @staticmethod
    def graph_to_window(x, y):
        gs = cool_set.GRAPH_SIZE
        ws = cool_set.WINDOW_SIZE/2
        ratio = ws/gs
        y *= -ratio
        x *= ratio
        x += ws
        y += ws
        return x, y

    @staticmethod
    def get_intercept_lines() -> list:
        lines = []
        gs = cool_set.GRAPH_SIZE
        for x in range(-int(gs)+1, int(gs)):
            lines.append(((cool_set.graph_to_window(x, -gs)), (cool_set.graph_to_window(x, gs))))
        for y in range(-int(gs)+1, int(gs)):
            lines.append(((cool_set.graph_to_window(-gs, y)), (cool_set.graph_to_window(gs, y))))
        return lines


if __name__ == "__main__":
    new = cool_set()
    new.run()
