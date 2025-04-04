import pygame
import math
import time
import numpy as np

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
                cur_num = cur_num**2 + start_num
        return Mandelbrot.iterations

    @staticmethod
    def coloring(value):
        """Custom function to map escape values to RGB colors."""
        t = value / Mandelbrot.iterations  # Normalize to [0, 1]
        r = int(8.5 * (1 - t)**3 * t * 255)  # Blue fades uniquely
        b = int(9 * (1 - t) * t**3 * 255)     # Red channel variation
        g = int(15 * (1 - t)**2 * t**2 * 255)   # Green transitions smoothly
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
                num = num**2 + Julia.spiral_c
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
        except Exception:
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
        self.screen = pygame.display.set_mode((self.window_x, self.window_y))
        self.clock = pygame.Clock()
        self.is_running = True
        self.bg_color = "black"
        self.FPS = 60

        pygame.display.set_caption("Mandelbrot")
        self.function = function
        self.coloring = coloring
        if self.function is None:
            self.function = Mandelbrot.function
        if self.coloring is None:
            self.coloring = Mandelbrot.coloring

        # Note: we keep the same shape as before.
        self.np_array = np.zeros((self.window_x, self.window_y, 3), dtype=np.uint8)
        self.pixel_surface = None

        self.holding_mouse = False
        self.holding_mouse_start_pos = None

    # Old translate (commented out)
    """def translate_window_to_graph(self, x, y):
        xg = (x - self.window_mid_x) * self.graph_win_ratio_x
        yg = (self.window_mid_y - y) * self.graph_win_ratio_y
        return xg, yg"""

    def translate_window_to_graph(self, x, y):
        xg = graph.x_start + (x / self.window_x) * graph.width
        yg = graph.y_start + (1 - y / self.window_y) * graph.height
        return xg, yg

    def loop_through(self):
        timer = time.perf_counter()
        print("loading...")
        pygame.display.set_caption("loading...")

        # Instead of two nested loops in pure Python,
        # we process one row at a time using NumPy operations.
        for y in range(self.window_y):
            # Compute the y coordinate in graph space.
            y_graph = graph.y_start + (1 - y / self.window_y) * graph.height
            # Generate an array of x pixel indices and convert to graph x-values.
            xs = graph.x_start + (np.arange(self.window_x) / self.window_x) * graph.width

            # Create the row's complex starting values.
            start = xs + 1j * y_graph
            # Copy to hold current values.
            cur = start.copy()
            # Prepare an array for the iteration count.
            iters_row = np.full(xs.shape, Mandelbrot.iterations, dtype=int)
            # Vectorized escape time calculation for the row.
            for i in range(Mandelbrot.iterations):
                mask = np.abs(cur) < 2
                if not np.any(mask):
                    break
                cur[mask] = cur[mask] ** 2 + start[mask]
                # For pixels that have just escaped, record the iteration count.
                newly_escaped = mask & (np.abs(cur) >= 2)
                iters_row[newly_escaped] = i

            # Now, compute the color for each pixel in this row.
            t = iters_row / Mandelbrot.iterations  # normalized escape count
            r_row = (8.5 * (1 - t)**3 * t * 255).astype(np.uint8)
            g_row = (15 * (1 - t)**2 * t**2 * 255).astype(np.uint8)
            b_row = (9 * (1 - t) * t**3 * 255).astype(np.uint8)
            row_colors = np.stack((r_row, g_row, b_row), axis=-1)  # shape (window_x, 3)
            # Store the row into our np_array (remember: first index is x, second is y)
            self.np_array[:, y, :] = row_colors

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

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.holding_mouse = True
                self.holding_mouse_start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.holding_mouse = False
                print("zooming..")
                self.zoom(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Press 'm' to minimize the window
                    pygame.display.iconify()

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
        distances.draw_points(self.screen)
        self.loop_through()
        while self.is_running:
            self.screen.fill(self.bg_color)
            self.draw()
            self.handle_inputs()
            self.preview_rect()
            distances.draw_points(self.screen)
            self.clock.tick(self.FPS)
            pygame.display.flip()


if __name__ == "__main__":
    print("starting")
    graph1 = graph(1400, 800, function=Mandelbrot.function, coloring=Mandelbrot.coloring)
    graph1.run()
    print("Ended")
