import pygame
import math
import time
import numpy as np
import pyautogui
from Utilities import text

def take_screen_shot():
    time.sleep(0.1)
    screenshot = pyautogui.screenshot()
    time_of_screenshot = time.time_ns()
    try:
        screenshot.save(f"screenshot{time_of_screenshot}.png")
    except Exception as e:
        print("could not save for the following reason:\n", e)
    print(f"screenshot saved at screenshot{time_of_screenshot}.png")

def get_midpoint(num1, num2):
    if isinstance(num1, tuple):
        return (num1[0] + num2[0]) / 2, (num1[1] + num2[1]) / 2
    else:
        return abs(num1 + num2) / 2

def check_valid(min_val, max_val):
    if min_val > max_val:
        raise ValueError(f"{min_val} should be less than {max_val}")

class Mandelbrot:
    iterations = 100

    @staticmethod
    def function(pt):
        x, y = pt
        start_num = x + 1j * y
        cur_num = start_num
        for i in range(Mandelbrot.iterations):
            if abs(cur_num) >= 2:
                return i
            else:
                cur_num = cur_num ** 2 + start_num
        return Mandelbrot.iterations

    @staticmethod
    def coloring(value):
        """Custom function to map escape values to RGB colors."""
        t = value / Mandelbrot.iterations  # Normalize to [0, 1]

        # Custom color mapping: Smooth gradient transitions
        r = int(8.5 * (1 - t) ** 3 * t * 255)  # Blue fades uniquely
        b = int(9 * (1 - t) * t ** 3 * 255)  # Red channel variation
        g = int(15 * (1 - t) ** 2 * t ** 2 * 255)  # Green transitions smoothly

        return r, g, b

class Julia:
    classic_c = -0.7 + 0.27015j
    snowflake_c = 0.285 + 0.01j
    spiral_c = -0.8 + 0.156j
    iterations = Mandelbrot.iterations

    @staticmethod
    def function(pt):
        x, y = pt
        num = x + y * 1j
        for i in range(Julia.iterations):
            if abs(num) >= 2:
                return i
            else:
                num = num ** 2 + Julia.spiral_c
        return Julia.iterations

    @staticmethod
    def coloring(num):
        if num == Julia.iterations:
            return 255, 255, 255
        return num % 5 * 63, num % 3 * 127, num % 2 * 255

class distances:
    p1 = (-7, 0)
    p2 = (7, 0)
    max = 10

    @staticmethod
    def function(pt):
        try:
            y = math.e ** (math.pi * 1j * pt[0])
        except OverflowError:
            y = -100
        return abs(y - pt[1])

    @staticmethod
    def coloring(num):
        # goal: the closer the brighter
        num2 = abs(int(255 / (num + 1)))
        return num2, 0, 0

    @staticmethod
    def draw_points(screen):
        pygame.draw.circle(
            surface=screen,
            color="red",
            center=distances.p1,
            radius=20
        )
        pygame.draw.circle(
            surface=screen,
            color="red",
            center=distances.p2,
            radius=20
        )

class fields:
    def __init__(self, graph_obj, line_size=20, dx=40, dy=40):
        self.rad = line_size / 2
        self.dx = dx
        self.dy = dy
        self.color_list = []
        self.lines = []
        self.arrows = []
        self.graph = graph_obj
        self.arrow_size = line_size / 4
        self.max_rad = self.rad * 4
        self.min_rad = 1
        self.rad_dropoff = 60

    def function1(self, x, y):
        return (y - self.graph.mouse_pos[1]) / (x - self.graph.mouse_pos[0])

    def function2(self, x, y):
        try:
            return (y - self.graph.mouse_pos[1]), (x - self.graph.mouse_pos[0])
        except ZeroDivisionError:
            return 0, 0

    @staticmethod
    def get_color_from_angle(angle):
        ratio = abs(2 * angle / math.pi)
        return [int(255 * ratio), 0, 0]

    @staticmethod
    def get_color_from_dist(dist):
        color = 255 / (dist/6 + 1)
        return [color, 0, 255-color]

    def get_rad(self, dist):
        return self.rad_dropoff * (self.max_rad - self.min_rad)/(self.rad_dropoff + dist**2) + self.min_rad

    def get_arrow(self, graph_point, window_point):
        gx, gy = graph_point
        wx, wy = window_point

        dist = math.dist(self.graph.mouse_pos, (gx, gy))
        dy, dx = self.function2(gx, gy)
        angle = -math.atan2(dy, dx)
        rad = self.get_rad(dist)
        dx, dy = rad * math.cos(angle), rad * math.sin(angle)

        line_end_x = wx + dx
        line_end_y = wy + dy
        self.color_list.append(self.get_color_from_dist(dist))
        self.lines.append(((wx, wy), (line_end_x, line_end_y)))
        self.arrows.append(
            ((line_end_x + self.arrow_size * math.cos(angle + math.pi / 2),
              line_end_y + self.arrow_size * math.sin(angle + math.pi / 2)),  # p1
             (line_end_x + self.arrow_size * math.cos(angle - math.pi / 2),
              line_end_y + self.arrow_size * math.sin(angle - math.pi / 2)),  # p2
             (line_end_x + self.arrow_size * 2 * math.cos(angle),
              line_end_y + self.arrow_size * 2 * math.sin(angle))  # p3
             )
        )

    def get_line(self, graph_point, window_point):
        gx, gy = graph_point
        wx, wy = window_point
        dist = 0
        try:  # the equation
            dist = math.dist((gx, gy), self.graph.mouse_pos)
            y_prime = self.function1(gx, gy)
            angle = math.atan(-y_prime)
        except ZeroDivisionError:
            angle = math.pi / 2
        self.color_list.append(fields.get_color_from_dist(dist))

        p1 = (wx + math.cos(angle) * self.rad, wy + math.sin(angle) * self.rad)
        angle += math.pi
        p2 = (wx + math.cos(angle) * self.rad, wy + math.sin(angle) * self.rad)

        self.lines.append((p1, p2))

    def create_lines(self, graph_obj):
        self.color_list = []
        self.lines = []
        self.arrows = []
        for x in range(0, graph_obj.window_x, self.dx):
            for y in range(0, graph_obj.window_y, self.dy):
                self.get_arrow(graph_obj.translate_window_to_graph(x, y), (x, y))  # get_line()

    def draw_arrow(self, surface):
        for line, color, arrow in zip(self.lines, self.color_list, self.arrows):
            pygame.draw.aaline(
                surface=surface,
                color=color,
                start_pos=line[0],
                end_pos=line[1],
            )
            pygame.draw.polygon(
                surface=surface,
                color=color,
                points=arrow,
            )

    def draw_lines(self, surface):
        for line, color in zip(self.lines, self.color_list):
            pygame.draw.aaline(
                surface=surface,
                color=color,
                start_pos=line[0],
                end_pos=line[1],
            )

class parametric:
    def __init__(self, graph_obj, t_start=-10, t_end=10, dt=0.01):
        self.graph = graph_obj
        self.t_start = t_start
        self.t_end = t_end
        self.dt = dt
        self.points = []
        self.color = "red"
        self.generate_points()

    def function1(self, t):
        try:
            y = t*math.sin(t)**4
            x = t**(0.5)*math.cos(t)**5
        except Exception as e:
            print(f"{e} at {t}")
            return None
        if x.imag != 0 or y.imag != 0:
            return None
        return self.graph.translate_graph_to_window(x, y)

    def polar_function(self, t):
        r = math.sin(t)
        try:
            y = r * math.sin(t)
            x = r * math.cos(t)
        except Exception as e:
            print(f"{e} at {t}")
            return None
        if x.imag != 0 or y.imag != 0:
            return None
        return self.graph.translate_graph_to_window(x, y)

    def generate_points(self):
        self.points = []
        cur_t = self.t_start
        while cur_t <= self.t_end:
            self.points.append(self.polar_function(cur_t))
            cur_t += self.dt

    def draw_points(self):
        for i, point1 in enumerate(self.points[:-1]):
            point2 = self.points[i+1]
            if not(point1 is None or point2 is None):
                pygame.draw.aaline(
                    surface=self.graph.screen,
                    color=self.color,
                    start_pos=point1,
                    end_pos=point2
                )

class graph:
    x_start = -14
    x_end = 14
    width = x_end - x_start
    check_valid(x_start, x_end)

    y_start = -8
    y_end = 8
    height = y_end - y_start
    check_valid(y_start, y_end)
    LOCK_RATIO = True
    W_TO_H_RATIO = width / height

    def __init__(self, window_x, window_y, function=None, coloring=None):
        self.window_x = window_x
        self.window_y = window_y
        self.window_mid_x = window_x / 2
        self.window_mid_y = window_y / 2
        self.graph_win_ratio_x = graph.width / window_x
        self.graph_win_ratio_y = graph.height / window_y

        pygame.display.set_caption("Mandelbrot")
        if function is None:
            function = Mandelbrot.function
        if coloring is None:
            coloring = Mandelbrot.coloring

        self.function = function
        self.coloring = coloring

        self.screen = pygame.display.set_mode((self.window_x, self.window_y))
        self.clock = pygame.Clock()
        self.FPS = 60
        self.is_running = True
        self.bg_color = "black"

        self.np_array = np.zeros((self.window_x, self.window_y, 3), dtype=np.uint8)
        self.pixel_surface = None

        self.holding_mouse = False
        self.holding_mouse_start_pos = None
        self.can_zoom = True
        self.show_mouse_location = False
        self.mouse_text = text.Text("(-,-)", center=(0, 0), color="white")
        self.mouse_pos = (0, 0)

    """def translate_window_to_graph(self, x, y):
        xg = (x - self.window_mid_x) * self.graph_win_ratio_x
        yg = (self.window_mid_y - y) * self.graph_win_ratio_y
        return xg, yg"""

    def translate_window_to_graph(self, x, y):
        xg = graph.x_start + (x / self.window_x) * graph.width
        yg = graph.y_start + (1 - y / self.window_y) * graph.height
        return xg, yg

    def translate_graph_to_window(self, x, y):
        xw = self.window_x * (x - graph.x_start)/graph.width
        yw = self.window_y * (1 - (y - graph.y_start)/graph.height)
        return xw, yw

    def loop_through(self):
        timer = time.perf_counter()
        print("loading...")
        pygame.display.set_caption("loading...")
        for y in range(0, self.window_y):
            for x in range(0, self.window_x):
                pt = self.translate_window_to_graph(x, y)
                self.np_array[x, y] = self.coloring(self.function(pt))
            if y % 10 == 0:
                print(f"{y * 100 / self.window_y :.1f}% complete")
        self.pixel_surface = pygame.surfarray.make_surface(self.np_array)
        self.get_delta()
        pygame.display.set_caption("mandelbrot")
        print("loading complete")
        print(f"{(time.perf_counter() - timer):.2f} seconds elapsed")

    def preview_rect(self):
        cur_pos = pygame.mouse.get_pos()
        if self.holding_mouse_start_pos and cur_pos:
            p1, p2 = cur_pos, self.holding_mouse_start_pos
            if graph.LOCK_RATIO:
                height = abs(p1[1] - p2[1])
                width = height * graph.W_TO_H_RATIO
                if p1[1] < p2[1]:
                    pygame.draw.rect(
                        surface=self.screen,
                        color="white",
                        rect=pygame.Rect(p1, (width, height)),
                        width=2
                    )
                else:
                    pygame.draw.rect(
                        surface=self.screen,
                        color="white",
                        rect=pygame.Rect(p2, (width, height)),
                        width=2
                    )
                return
            new_p1 = (min(p1[0], p2[0]), min(p1[1], p2[1]))
            new_size = (abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
            pygame.draw.rect(
                surface=self.screen,
                color="white",
                rect=pygame.Rect(new_p1, new_size),
                width=2
            )

    def get_delta(self):
        p1 = self.translate_window_to_graph(1, 1)
        p2 = self.translate_window_to_graph(2, 2)
        print(f"delta: 10^{math.log(p2[0] - p1[0]):.2f}")

    def draw_mouse_locations(self):
        mouse_location = pygame.mouse.get_pos()
        self.mouse_pos = self.translate_window_to_graph(*mouse_location) if mouse_location else (0, 0)
        if mouse_location is not None and self.show_mouse_location:
            self.mouse_text.center = mouse_location
            graph_pos = self.translate_window_to_graph(*mouse_location)
            self.mouse_text.text = f"{graph_pos[0]:.2f}, {graph_pos[1]:.2f}"
            self.mouse_text.update_text()
            self.mouse_text.draw(self.screen)

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.can_zoom:
                self.holding_mouse = True
                self.holding_mouse_start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and self.can_zoom:
                self.holding_mouse = False
                print("zooming..")
                self.zoom(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Press 'm' to minimize the window
                    pygame.display.iconify()
                if event.key == pygame.K_s:
                    take_screen_shot()

    @classmethod
    def change_position(cls, new_x_start, new_x_end, new_y_start, new_y_end):
        cls.x_start = new_x_start
        cls.x_end = new_x_end
        cls.width = new_x_end - new_x_start

        cls.y_start = new_y_start
        cls.y_end = new_y_end
        cls.height = new_y_end - new_y_start

    def zoom(self, end_pos):
        if self.holding_mouse_start_pos is None or end_pos is None:
            return
        end_x, end_y = end_pos
        m_x, m_y = self.holding_mouse_start_pos
        if graph.LOCK_RATIO:
            height = abs(end_y - m_y)
            width = height * graph.W_TO_H_RATIO
            end_pos = (m_x + width, m_y + height)
            end_x, end_y = end_pos
        x1, y1 = self.translate_window_to_graph(end_x, end_y)
        x2, y2 = self.translate_window_to_graph(m_x, m_y)
        print(x1)
        graph.change_position(new_x_start=min(x1, x2),
                              new_x_end=max(x1, x2),
                              new_y_start=min(y1, y2),
                              new_y_end=max(y1, y2))

        self.graph_win_ratio_x = graph.width / self.window_x
        self.graph_win_ratio_y = graph.height / self.window_y

        self.np_array = np.zeros((self.window_x, self.window_y, 3), dtype=np.uint8)
        self.loop_through()
        self.holding_mouse_start_pos = None

    def draw(self):
        self.screen.blit(self.pixel_surface, (0, 0))

    def run(self):
        self.loop_through()
        while self.is_running:
            self.screen.fill(self.bg_color)

            self.draw()
            self.handle_inputs()
            self.preview_rect()
            distances.draw_points(self.screen)

            self.clock.tick(self.FPS)
            pygame.display.flip()

    def run_fields(self):
        self.can_zoom = False
        field = fields(self)
        while self.is_running:
            self.screen.fill(self.bg_color)
            self.handle_inputs()
            field.create_lines(graph_obj=self)
            self.draw_mouse_locations()
            #  print(self.mouse_pos)
            field.draw_arrow(self.screen)
            pygame.display.flip()

    def run_param(self):
        self.can_zoom = False
        param = parametric(self)
        while self.is_running:
            self.screen.fill(self.bg_color)
            self.handle_inputs()
            param.draw_points()
            pygame.display.flip()


if __name__ == "__main__":
    graph1 = graph(1400, 800, function=Mandelbrot.function, coloring=Mandelbrot.coloring)
    graph1.run_param()
