import pygame
import numpy as np
from Utilities.text import Text
class pt:

    max_iterations = 50

    win_size = 700
    gr_size = 2
    win_mid_x = win_size/2
    win_mid_y = win_size/2

    gr_to_win = gr_size/win_size
    win_to_gr = win_size/gr_size
    all = []
    pixel_array = np.zeros((win_size, win_size, 3), dtype=np.uint8)
    pixel_surface = None
    color_ratio = 255/max_iterations
    new_screen_rect = None
    new_text1 = Text("0", (10, 10), color="black")
    new_text2 = Text("0", (win_size - 10, 10), color="black")
    x_start = 0
    y_start = 0
    total_size = win_size
    @staticmethod
    def window_to_graph(x, y):
        x -= pt.win_mid_x
        y -= pt.win_mid_y
        y *= -pt.gr_to_win
        x *= pt.gr_to_win
        return x, y

    @staticmethod
    def graph_to_window(x, y):
        y *= -pt.win_to_gr
        x *= pt.win_to_gr
        x += pt.win_mid_x
        y += pt.win_mid_y
        return x, y

    @staticmethod
    def translate_x_y_to_new_screen(x, y):
        if pt.new_screen_rect is None:
            return x, y
        # x, y is 0 - size,

        x *= pt.new_screen_rect.height/pt.win_size
        y *= pt.new_screen_rect.height/pt.win_size

        x += pt.new_screen_rect.x
        y += pt.new_screen_rect.y
        return x, y

    @classmethod
    def update(cls, rect):
        if rect is None:
            return
        if cls.new_screen_rect:
            p1 = pt.translate_x_y_to_new_screen(*rect.bottomright)
            p2 = pt.translate_x_y_to_new_screen(*rect.topleft)
            size = p2[1] - p1[1]
            if size < 0:
                size = abs(size)
                p1 = p2
            rect = pygame.Rect(p1, (size, size))

        cls.new_screen_rect = rect
        cls.loop_through()

    @staticmethod
    def get_num_iterations_from_win_point(x, y):
        x, y = pt.window_to_graph(x, y)
        start_num = x + y * 1j
        cur_num = start_num
        for i in range(pt.max_iterations):
            if abs(cur_num) >= 2:
                return i
            else:
                cur_num **= 2
                cur_num += start_num
        return pt.max_iterations

    @staticmethod
    def get_num_iterations_from_win_point(x, y):
        # Convert (x, y) to the graph coordinate system using your pt.window_to_graph
        x, y = pt.window_to_graph(x, y)

        # Create a complex grid of start numbers
        start_num = x + y * 1j
        cur_num = np.copy(start_num)  # This will hold the current complex number

        # Initialize an array to store the iteration count for each point (useful for a grid of points)
        num_iterations = np.zeros_like(start_num, dtype=int)

        for i in range(pt.max_iterations):
            # Perform the check if the absolute value is >= 2
            mask = np.abs(cur_num) < 2

            # If abs(cur_num) >= 2, set the corresponding iteration count
            num_iterations[~mask] = i  # Set iteration count for points where abs(cur_num) >= 2

            # Break early if all points have escaped
            if np.all(~mask):
                break

            # Perform the iteration: cur_num = cur_num^2 + start_num
            cur_num[mask] = cur_num[mask]**2 + start_num[mask]

        # Return the iteration count for points
        return num_iterations

    @staticmethod
    def get_color(i):
        return round(i * pt.color_ratio)

    @classmethod
    def loop_through(cls):
        for x in range(pt.win_size):
            for y in range(pt.win_size):
                xt, yt = pt.translate_x_y_to_new_screen(x, y)
                i = pt.get_num_iterations_from_win_point(xt, yt)
                col_num = pt.get_color(i)
                color = (255 * (i % 2), 127 * (i % 3), 85 * (i % 4))
                cls.pixel_array[x, y] = color
            print(f"{(x*100/pt.win_size):.2f}%")
        cls.pixel_surface = pygame.surfarray.make_surface(cls.pixel_array)

    @staticmethod
    def draw(surface):
        surface.blit(pt.pixel_surface, (0, 0))
        if pt.new_screen_rect:
            pt.new_text1.text = f"{pt.new_screen_rect.left}"
            pt.new_text2.text = f"{pt.new_screen_rect.right}"
            pt.new_text1.update_text()
            pt.new_text2.update_text()
            pt.new_text1.draw(surface)
            pt.new_text2.draw(surface)


def make_rect(p1, p2, surface, t1, t2):
    if (p1 is None or p2 is None or abs(p1[1] - p2[1]) < 2 or
            max(p1[0], p1[1], p2[0], p2[1]) > pt.win_size or
            min(p1[0], p1[1], p2[0], p2[1]) < 0):
        return

    min_x = min(p1[0], p2[0])
    if p1[1] > p2[1]:
        max_y = p1[1]
        min_y = p2[1]
    else:
        max_y = p2[1]
        min_y = p1[1]

    new_p1 = min_x, min_y

    new_size = max_y - min_y
    new_rect = pygame.Rect(new_p1, (new_size, new_size))

    t1.text = str(new_rect.left)
    t2.text = str(new_rect.right)

    t1.center = new_rect.topleft
    t2.center = new_rect.topright

    t1.update_text()
    t2.update_text()

    t1.draw(surface)
    t2.draw(surface)
    pygame.draw.rect(surface=surface,
                     color="white",
                     rect=new_rect,
                     width=2)
    return new_rect

def main():
    screen = pygame.display.set_mode((pt.win_size, pt.win_size))
    pygame.display.set_caption("Mandelbrot")
    running = True
    pt.loop_through()
    dragging = False
    start_pos = None
    rect = None
    text1 = Text("", (0,0), color="black")
    text2 = Text("", (0,0), color="black")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                pt.update(rect)
                rect = None

        screen.fill((0, 0, 0))

        # Color a single pixel at position (200, 150) to red
        rect = make_rect(start_pos, pygame.mouse.get_pos(), screen, text1, text2)
        pt.draw(screen)

        if dragging:
            rect = make_rect(start_pos, pygame.mouse.get_pos(), screen, text1, text2)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
