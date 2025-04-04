import pygame
import math
from PIL import Image

pi2 = math.pi / 2

class Car:
    width = 5
    height = 10
    width_half = width / 2
    height_half = height / 2
    angle = math.atan2(height, width)
    radius = 10
    max_speed = 7
    accel = 0.1
    drift_factor = 0  # Controls how much the car slides
    decel = 0.99
    drift_length = 1000
    length_per = 255/drift_length
    image = Image.open("car.png")
    print(len(image.tobytes()))
    image = image.resize((width*4, height*4))
    print(len(image.tobytes()))
    pygame_image = pygame.image.fromstring(image.tobytes(), (width*4, height*4), "RGBA")
    pygame_image_rect = pygame_image.get_frect()

    def __init__(self, spawn=(100, 100), color="red"):
        self.x, self.y = spawn
        self.dx, self.dy = 0, 0
        self.color = color
        self.angle = 0  # Facing direction
        self.speed = 0
        self.angular_speed = 0
        self.points = ()
        self.wheel_marks = [[], [], [], []]
        self.color_list = [(int(i*Car.length_per), int(i*Car.length_per), int(i*Car.length_per)) for i in range(Car.drift_length)]

    def get_point(self, angle, rad):
        return self.x + rad * math.cos(angle + self.angle), self.y + rad * math.sin(angle + self.angle)

    def set_points(self):
        self.points = (self.get_point(pi2/2, Car.radius),
                       self.get_point(-pi2/2, Car.radius),
                       self.get_point(pi2/4, -Car.radius*2),
                       self.get_point(-pi2/4, -Car.radius*2))

    def make_line(self):
        for i, point in enumerate(self.points[2:]):
            self.wheel_marks[i].append(point)
            if len(self.wheel_marks[i]) > Car.drift_length:
                self.wheel_marks[i].pop(0)

    def draw_line(self, surface):
        for marks in self.wheel_marks:
            for i in range(len(marks)-1):
                cur = marks[i]
                near = marks[i+1]
                pygame.draw.aaline(
                    surface=surface,
                    color=self.color_list[i],
                    start_pos=cur,
                    end_pos=near
                )

    def draw(self, surface : pygame.surface.Surface):
        self.set_points()
        self.make_line()
        self.draw_line(surface)
        pygame.draw.polygon(
            surface=surface,
            color=self.color,
            points=self.points,
        )

    @staticmethod
    def draw_road(surface):
        pygame.draw.rect(
            surface=surface,
            color="black",
            rect=pygame.Rect((0, 300),(1400, 200))
        )

    def return_car(self, w, h):
        if not (-10 < self.x < w + 10):
            self.x = w - self.x
            self.wheel_marks = [[], [], [], []]
        elif not (-10 < self.y < h + 10):
            self.y = h - self.y
            self.wheel_marks = [[], [], [], []]

    def change_drift_factor(self):
        if 300 < self.y < 500:
            Car.drift_factor = 0.8
        else:
            Car.drift_factor = 0.99

    def move(self, main):
        self.return_car(main.surface.width, main.surface.height)
        # Apply drifting effect
        target_dx = math.cos(self.angle) * self.speed
        target_dy = math.sin(self.angle) * self.speed

        self.dx = self.dx * Car.drift_factor + target_dx * (1 - Car.drift_factor)
        self.dy = self.dy * Car.drift_factor + target_dy * (1 - Car.drift_factor)

        self.x += self.dx * main.dt
        self.y += self.dy * main.dt
        self.angle += self.angular_speed * main.dt


    def handle_inputs(self, main):
        if "w" in main.keys_down and self.speed < Car.max_speed:
            self.speed += Car.accel
        elif "s" in main.keys_down and self.speed > 0:
            self.speed -= Car.accel * 2
        else:
            self.speed *= Car.decel  # Natural deceleration

        if "a" in main.keys_down:
            self.angular_speed = -0.02 * (self.speed / Car.max_speed)
        elif "d" in main.keys_down:
            self.angular_speed = 0.02 * (self.speed / Car.max_speed)
        else:
            self.angular_speed = 0

        self.move(main)

class Game:
    def __init__(self):
        self.surface = pygame.display.set_mode((1400, 800))
        self.clock = pygame.Clock()
        self.bg_color = (30, 30, 30)
        self.running = True
        self.keys_down = []
        self.dt = 0
        pygame.mouse.set_visible(False)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        self.keys_down = [pygame.key.name(i) for i in range(len(keys)) if keys[i]]

    def run(self):
        car = Car()
        while self.running:
            self.surface.fill(self.bg_color)
            self.input()
            Car.draw_road(self.surface)
            car.change_drift_factor()
            car.handle_inputs(self)
            car.draw(self.surface)
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 10  # Adjusted for smoother motion


if __name__ == "__main__":
    Game().run()
