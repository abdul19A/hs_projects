import pygame
import random

# vars

WIN_X: int = 800
WIN_Y: int = 600
WIN_MID: tuple = (WIN_X / 2, WIN_Y / 2)
GRID_SIZE: int = 10
GRID_WIDTH: int = WIN_X // GRID_SIZE
GRID_HEIGHT: int = WIN_Y // GRID_SIZE
BG_COLOR: pygame.Color = pygame.Color(0, 100, 200)
FPS = 60

# Do error handling
if WIN_X % GRID_SIZE != WIN_Y % GRID_SIZE != 0:
    raise ValueError("UN-GRID-ABLE WINDOW SIZE")


# classes
class Sandbox:
    @staticmethod
    def get_list():
        ret = []
        for y in range(GRID_HEIGHT):
            ret.append([])
            for x in range(GRID_WIDTH):
                ret[y].append(0)
        return ret

    @staticmethod
    def get_rect_list():
        start_pos_list = Sandbox.get_list()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                start_pos_list[y][x] = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        return start_pos_list

    @staticmethod
    def get_sand_color(particle):
        return 255, 255, int(particle * 127)

    @staticmethod
    def is_in_bounds(x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def get_particle_type(self, x, y):
        particle = self.sand_list[y][x]
        new_particle = self.new_list[y][x]
        if particle == 0 :
            return "empty"
        elif particle <= 1 or new_particle <= 1:
            return "sand"
        elif particle <= 2 or new_particle <= 2:
            return "water"

    def __init__(self, runner):
        self.sand_list: list = Sandbox.get_list()
        self.water_list: list = Sandbox.get_list()
        self.new_list = self.sand_list.copy()
        self.runner = runner
        self.rect_list = Sandbox.get_rect_list()

    def set_sand(self, grid_x, grid_y):
        if self.sand_list[grid_y][grid_x] != 0:
            return
        self.sand_list[grid_y][grid_x] = random.random()

    def do_sand_movement(self, sand_p, x, y):
        if y >= GRID_HEIGHT - 1:
            self.new_list[y][x] = sand_p
            return

        sand_below = self.sand_list[y + 1][x]

        if sand_below == 0:
            self.new_list[y][x] = 0
            self.new_list[y + 1][x] = sand_p
            return
        bot_left_is_available = Sandbox.is_in_bounds(x + 1, y + 1) and self.sand_list[y + 1][x + 1] == 0
        bot_right_is_available = Sandbox.is_in_bounds(x - 1, y + 1) and self.sand_list[y + 1][x - 1] == 0
        if bot_left_is_available and bot_right_is_available:
            if random.random() >= 0.5:
                bot_left_is_available = False
        if bot_left_is_available:
            self.new_list[y][x] = 0
            self.new_list[y + 1][x + 1] = sand_p
            return
        elif bot_right_is_available:
            self.new_list[y][x] = 0
            self.new_list[y + 1][x - 1] = sand_p
            return
        else:
            self.new_list[y][x] = sand_p

    def do_water_movement(self, water_p, x, y):
        if Sandbox.is_in_bounds(x, y + 1) and self.get_particle_type(x, y + 1) == "empty":  # below
            self.new_list[y][x] = 0
            self.new_list[y + 1][x] = water_p
            return
        elif Sandbox.is_in_bounds(x + 1, y + 1) and self.get_particle_type(x + 1, y + 1) == "empty":  # bot-right
            self.new_list[y][x] = 0
            self.new_list[y+1][x+1] = water_p
            return
        elif Sandbox.is_in_bounds(x - 1, y + 1) and self.get_particle_type(x - 1, y + 1) == "empty":  # bot-left
            self.new_list[y][x] = 0
            self.new_list[y+1][x-1] = water_p
            return
        left_available = Sandbox.is_in_bounds(x - 1, y) and self.get_particle_type(x - 1, y) == "empty"
        right_available = Sandbox.is_in_bounds(x + 1, y) and self.get_particle_type(x + 1, y) == "empty"
        if left_available and right_available:
            if random.random() >= 0.5:
                left_available = False

        if left_available:
            self.new_list[y][x] = 0
            self.new_list[y][x-1] = water_p
            return
        elif right_available:
            self.new_list[y][x] = 0
            self.new_list[y][x+1] = water_p
            return
        self.new_list[y][x] = water_p

    def do_particle_movement(self, x, y):
        particle = self.sand_list[y][x]
        if self.get_particle_type(x, y) == "sand":
            self.do_water_movement(particle, x, y)
            return
        elif self.get_particle_type(x, y) == "water":
            self.do_water_movement(particle, x, y)
            return

    def move_sand(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                self.do_particle_movement(x, y)
        self.sand_list = self.new_list.copy()
        self.new_list = Sandbox.get_list()

    def get_num_sand(self):
        num = 0
        for row in self.sand_list:
            for particle in row:
                if particle > 0:
                    num += 1
        return num

    def draw(self, surface):
        for y, row in enumerate(self.sand_list):
            for x, particle in enumerate(row):
                if particle != 0:
                    pygame.draw.rect(
                        surface=surface,
                        color=Sandbox.get_sand_color(particle),
                        rect=self.rect_list[y][x],

                    )


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_X, WIN_Y))
        self.clock = pygame.Clock()
        self.is_running = True
        self.is_dragging = False
        self.mouse_location = ()

    def get_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.is_dragging = True
                return
            if event.type == pygame.MOUSEBUTTONUP:
                self.is_dragging = False
                return

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        self.screen.fill(BG_COLOR)

    def put_sand(self, sand_obj):
        if not self.is_dragging:
            return
        mx, my = pygame.mouse.get_pos()
        gx, gy = mx // GRID_SIZE, my // GRID_SIZE
        if 0 <= gx <= GRID_WIDTH - 1 and 0 <= gy <= GRID_HEIGHT - 1 and mx > 0:
            sand_obj.set_sand(gx, gy)

    def run(self):
        sand_sim = Sandbox(self)
        while self.is_running:
            self.get_user_input()
            self.put_sand(sand_sim)
            sand_sim.move_sand()
            sand_sim.draw(self.screen)
            self.update()


if __name__ == "__main__":
    main = Main()
    main.run()
