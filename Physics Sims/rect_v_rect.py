import pygame
import random
import math
import time

def rand_dx():
    return random.randrange(-10, 10)


def rand_color():
    return random.choice(["white", "gray", "blue",
                          "green", "yellow", "orange",
                          "brown", "red", "pink", "purple",
                          "magenta", "indigo"])

class Block:
    E = 1
    all_blocks = []

    def __init__(self, x=None, y=None, width=None, height=None, color=None, dx=None, dy=0, mass=1, win_x=None, win_y=None):  # color and dx are none because they are rand

        if not all((x, y, width, height)) and x != 0 and y != 0:
            width = 20  # random.randrange(10, 50)
            height = 20  # random.randrange(10, 50)
            x = random.randrange(0, win_x - width)
            y = random.randrange(0, win_y - height)
            dx = random.randrange(-100, 100)
            dy = random.randrange(-100, 100)
            mass = width * height / 50

        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

        self.dx = dx if dx is not None else rand_dx()
        self.dy = dy

        self.width = width
        self.height = height
        self.color = color if color is not None else rand_color()
        self.rect = pygame.FRect(x, y, width, height)
        self.mass = mass

        self.all_blocks.append(self)

    def get_angle(self, block_2):
        b1, b2 = self, block_2

        def average(a, b):
            return (a + b) / 2

        return math.atan2(average(b1.y1, b1.y2) - average(b2.y1, b2.y2),
                          average(b1.x1, b1.x2) - average(b2.x1, b2.x2))

    @staticmethod
    def update(dt):
        for block in Block.all_blocks:
            block.x1 += block.dx * dt
            block.y1 += block.dy * dt

            block.x2 = block.x1 + block.width
            block.y2 = block.y1 + block.height

            block.rect = pygame.FRect(block.x1, block.y1, block.width, block.height)

    @staticmethod
    def draw_all(surface):
        for block in Block.all_blocks:
            pygame.draw.rect(
                surface=surface,
                color=block.color,
                rect=block.rect,
                width=0
            )

    @staticmethod
    def check_collision(block_1, block_2):
        return (
                (block_1.x1 <= block_2.x1 <= block_1.x2
                 or block_1.x1 <= block_2.x2 <= block_1.x2) and
                (block_1.y1 <= block_2.y1 <= block_1.y2
                 or block_1.y1 <= block_2.y2 <= block_1.y2)
        )

    @staticmethod
    def block_v_block_collision(block_1, block_2):
        # system 2
        # restitution
        e = Block.E
        # Calculate the angle of collision
        angle = block_1.get_angle(block_2)

        # Velocity components along the angle of collision
        v1 = (block_1.dx, block_1.dy)
        v2 = (block_2.dx, block_2.dy)

        # Using the angle to project velocities onto the collision axis
        v1_parallel = v1[0] * math.cos(angle) + v1[1] * math.sin(angle)
        v1_perpendicular = -v1[0] * math.sin(angle) + v1[1] * math.cos(angle)
        v2_parallel = v2[0] * math.cos(angle) + v2[1] * math.sin(angle)
        v2_perpendicular = -v2[0] * math.sin(angle) + v2[1] * math.cos(angle)

        # Apply the energy-loss collision formula for parallel components
        v1_parallel_new = ((block_1.mass - e * block_2.mass) * v1_parallel + (1 + e) * block_2.mass * v2_parallel) / (
                    block_1.mass + block_2.mass)
        v2_parallel_new = ((block_2.mass - e * block_1.mass) * v2_parallel + (1 + e) * block_1.mass * v1_parallel) / (
                    block_1.mass + block_2.mass)

        # The perpendicular components remain unchanged
        v1_new = (
            v1_parallel_new * math.cos(angle) - v1_perpendicular * math.sin(angle),
            v1_parallel_new * math.sin(angle) + v1_perpendicular * math.cos(angle)
        )
        v2_new = (
            v2_parallel_new * math.cos(angle) - v2_perpendicular * math.sin(angle),
            v2_parallel_new * math.sin(angle) + v2_perpendicular * math.cos(angle)
        )

        # Update the velocities
        block_1.dx, block_1.dy = v1_new
        block_2.dx, block_2.dy = v2_new
        # system 1
        """temp_dx, temp_dy = block_1.dx, block_1.dy
        temp2_dx, temp2_dy = block_2.dx, block_2.dy

        block_1_momentum_x = block_1.dx * block_1.mass
        block_1_momentum_y = block_1.dy * block_1.mass

        block_2_momentum_x = block_2.dx * block_2.mass
        block_2_momentum_y = block_2.dy * block_2.mass

        block_1.dx += (block_2.dx * block_2.mass)/block_1.mass
        block_1.dy += (block_2.dy * block_2.mass)/block_1.mass

        block_2.dx += (temp_dx * block_1.mass)/block_2.mass
        block_2.dy += (temp_dy * block_1.mass)/block_2.mass"""

    @staticmethod
    def remove_overlap(block_1, block_2):
        space = 1
        # find where overlap is greatest then reverse it
        all_overlaps = [block_1.y2 - block_2.y1, block_2.y2 - block_1.y1, block_1.x2 - block_2.x1,
                        block_2.x2 - block_1.x1]

        min_dist = (min(all_overlaps))
        min_dist_index = all_overlaps.index(min_dist)
        if min_dist_index == 0:  # when b2 approaches b1 from bottom
            block_2.y1 = block_1.y2 + space
            block_2.y2 = block_1.y2 + block_2.height + space

        elif min_dist_index == 1:  # when b2 approaches b1 from above
            block_2.y1 = block_1.y1 - block_2.height - space
            block_2.y2 = block_1.y1 - space

        if min_dist_index == 2:  # when b2 approaches b1 from right
            block_2.x1 = block_1.x2 + space
            block_2.x2 = block_1.x2 + block_2.width + space

        elif min_dist_index == 3:  # when b2 approaches b1 from left
            block_2.x1 = block_1.x1 - block_2.width - space
            block_2.x2 = block_1.x1 - space

    @staticmethod
    def apply_collisions(win_x, win_y):
        crash_timer = time.perf_counter()
        for block_1 in Block.all_blocks:
            for block_2 in Block.all_blocks:
                if block_1 is not block_2 and Block.check_collision(block_1, block_2):
                    """if they are not the same block and colliding"""
                    """IMPORTANT: ALL FORCES ARE LINEAR"""
                    Block.block_v_block_collision(block_1, block_2)
                    Block.remove_overlap(block_1, block_2)
                    Block.do_on_collision_event(win_x, win_y)
                    if time.perf_counter() - crash_timer > 1:
                        raise RuntimeError(f"SIM CRASHED, MAX NUM: {len(Block.all_blocks)}")
    
    @staticmethod
    def do_on_collision_event(win_x, win_y):
        random_number = random.randrange(100)
        if random_number <= 75:
            Block(win_x=win_x, win_y=win_y)
        else:
            Block.all_blocks.pop(-1)


    @staticmethod
    def apply_wall_bounce(win_x, win_y):
        for block in Block.all_blocks:
            if block.x1 <= 0:
                block.dx = abs(block.dx)
                block.x1 = 0
                block.x2 = block.width
            elif block.x2 >= win_x:
                block.dx = -abs(block.dx)
                block.x1 = win_x - block.width
                block.x2 = win_x
            if block.y1 <= 0:
                block.dy = abs(block.dy)
                block.y1 = 0
                block.y2 = block.height
            elif block.y2 >= win_y:
                block.dy = -abs(block.dy)
                block.y1 = win_y - block.height
                block.y2 = win_y

    @staticmethod
    def apply_gravity(gravity, dt):
        space = 1
        for block in Block.all_blocks:
            if block.y2 - space <= 600:
                block.dy += gravity * dt


class Simulation:
    GRAVITY = 100

    def __init__(self, win_x, win_y, graph_width=600, FPS=60, bg_color="black"):
        pygame.init()
        self.win_x = win_x
        self.win_y = win_y
        self.FPS = FPS
        self.bg_color = bg_color
        self.graph_width = graph_width
        self.surface = pygame.display.set_mode((win_x + graph_width, win_y), pygame.RESIZABLE)
        self.clock = pygame.Clock()
        self.start_time = time.perf_counter()
        self.num_blocks = [0]
        self.times = [0.0]
        self.margin = 50
        self.timer_start = time.perf_counter()
        self.timer_dur = 0.5
        self.font = pygame.font.Font(None, 20)

    def draw_graph(self):
        pygame.draw.rect(self.surface, color="white", rect=pygame.Rect(self.win_x, 0, self.graph_width, self.win_y))

        pygame.draw.line(self.surface, color="black", start_pos=(self.win_x + self.margin, self.margin),
                         end_pos=(self.win_x + self.margin, self.win_y - self.margin))
        pygame.draw.line(self.surface, color="black", start_pos=(self.win_x + self.margin, self.win_y - self.margin),
                         end_pos=(self.win_x + self.graph_width - self.margin, self.win_y - self.margin))

        space = 10
        self.draw_text(f"{max(self.num_blocks)}", (self.win_x + self.margin - space, self.margin))
        self.draw_text(f"{self.times[-1]:.2f}", (self.win_x + self.graph_width - self.margin, self.win_y - self.margin + space))
        #print(self.win_x + self.margin - space, self.win_y + self.margin)

    def do_per_timer(self):
        if time.perf_counter() - self.timer_start >= self.timer_dur:
            self.timer_start = time.perf_counter()
            return True
        return False

    def translate_points(self):
        if self.do_per_timer():
            cur_time: float = time.perf_counter() - self.start_time
            self.num_blocks.append(len(Block.all_blocks))
            self.times.append(cur_time)

    def draw_points(self):
        graph_x_start = self.win_x + self.margin
        graph_y_start = self.win_y - self.margin

        graph_height = self.win_y - 2 * self.margin
        graph_width = self.graph_width - 2 * self.margin

        min_num = min(self.num_blocks)
        min_times = self.times[0]

        total_delta_time = self.times[-1] - min_times  # last index is always the greatest
        total_delta_num_b = max(self.num_blocks) - min_num

        if total_delta_num_b == 0 or total_delta_num_b == 0:
            return
        all_points = []

        for i, num_block in enumerate(self.num_blocks):
            cur_time = self.times[i]
            x = graph_x_start + ((cur_time - min_times)/total_delta_time) * graph_width
            y = graph_y_start - ((num_block - min_num)/total_delta_num_b * graph_height)
            #print(x, y)
            center = (x, y)
            pygame.draw.circle(surface=self.surface, color="red", center=center, radius=5)
            all_points.append(center)

        if len(all_points) >= 2:
            pygame.draw.lines(surface=self.surface, color="red", closed=False, points=all_points)

    def init_blocks(self):
        for _ in range(3):
            Block(win_x=self.win_x, win_y=self.win_y)

    def draw_text(self, text, center):
        text_surface = self.font.render(text, True, "black")
        text_rect = text_surface.get_rect(center=center)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        running = True
        self.init_blocks()
        while running:
            dt = self.clock.tick(self.FPS) / 1000
            self.surface.fill(self.bg_color)
            self.draw_graph()
            self.translate_points()
            self.draw_points()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            Block.update(dt)
            Block.draw_all(self.surface)
            Block.apply_collisions(self.win_x, self.win_y)
            Block.apply_wall_bounce(self.win_x, self.win_y)
            Block.apply_gravity(Simulation.GRAVITY, dt)


            pygame.display.flip()


if __name__ == "__main__":
    sim = Simulation(800, 700, FPS=120, graph_width=500)
    sim.run()
