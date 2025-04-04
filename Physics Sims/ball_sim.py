import pygame
import math
import random
import time

win_x = 600
win_y = 600

class Circle:
    list = []

    def __init__(self, center_point, radius, color, width, screen):
        self.center_point = center_point
        self.radius = radius
        self.color = color
        self.width = width
        self.screen = screen
        Circle.list.append(self)

    def draw(self):
        pygame.draw.circle(
            surface=self.screen,
            color=self.color,
            center=self.center_point,
            radius=self.radius,
            width=self.width
        )

    @staticmethod
    def draw_all():
        for circle in Circle.list[::-1]:
            circle.draw()


class Bounce_Circle(Circle):
    def __init__(self, screen):
        super().__init__([win_x / 2, win_y / 2], win_y / 2 - win_y / 10, "white", 1, screen)
        self.type = "Bounce_Circle"

    def check_hit(self, ball, dt):
        ball_next_distance = math.dist(ball.get_next_position(dt), self.center_point)

        if ball_next_distance > self.radius - ball.radius:
            # checks if after it moves it will collide
            ball.apply_energy_loss()

            inv_angle = ball.get_angle(self.center_point) + math.pi
            ball.add_speed(ball.get_speed(), inv_angle)

            new_pos_angle = get_angle(self.center_point, ball.center_point)

            new_radius = self.radius - ball.radius

            new_x_pos = self.center_point[0] + new_radius * math.cos(new_pos_angle)
            new_y_pos = self.center_point[1] + new_radius * math.sin(new_pos_angle)
            ball.center_point = [new_x_pos, new_y_pos]

    def get_available_spawn(self, ball_radius):
        while True:
            rand_x = random.randrange(ball_radius + 1, self.radius * 2 - ball_radius) + self.center_point[
                0] - self.radius
            rand_y = random.randrange(ball_radius + 1, self.radius * 2 - ball_radius) + self.center_point[
                1] - self.radius
            rand_cord = [rand_x, rand_y]

            if math.dist([rand_x, rand_y], self.center_point) < self.radius - ball_radius:
                is_inside_ball2 = False
                for ball2 in Ball.list:
                    if ball2.radius + ball_radius > math.dist(ball2.center_point, rand_cord):
                        is_inside_ball2 = True

                        break
                if not is_inside_ball2:
                    return rand_cord


class Ball(Circle):
    list = []
    gravity = 50
    energy_loss_coefficient = 1.01

    def __init__(self, center_point: list = None,
                 radius=None,
                 color=None,
                 screen=None,
                 big_circle=None,
                 dx=None,
                 dy=None):

        self.radius = radius if radius else random.randrange(3, 10)
        if not center_point:
            center_point = big_circle.get_available_spawn(self.radius)

        super().__init__(center_point, self.radius, color if color else get_color(), 0, screen)
        self.dx = dx if dx else random.randrange(-6, 5)
        self.dy = dy if dx else random.randrange(-6, 5)
        self.mass = self.radius ** 3
        self.type = "Ball"
        Ball.list.append(self)

    def apply_energy_loss(self):
        self.dx *= Ball.energy_loss_coefficient
        self.dy *= Ball.energy_loss_coefficient

    def get_next_position(self, dt) -> list:
        return [self.center_point[0] + self.dx * dt, self.center_point[1] + self.dy * dt]

    def get_previous_position(self, dt) -> list:
        return [self.center_point[0] - self.dx * dt, self.center_point[1] - self.dy * dt]

    def get_angle(self, big_circle_point: list) -> float:
        change_x = self.center_point[0] - big_circle_point[0]
        change_y = self.center_point[1] - big_circle_point[1]
        return math.atan2(change_y, change_x)

    def get_speed(self):
        return (self.dx ** 2 + self.dy ** 2) ** .5

    def add_speed(self, speed, angle):
        self.dx += speed * math.cos(angle)
        self.dy += speed * math.sin(angle)

    def move(self, dt):
        self.center_point[0] += self.dx * dt
        self.center_point[1] += self.dy * dt

    def get_ball_v_ball_angle(self, ball2):
        return math.atan2(self.center_point[1] - ball2.center_point[1], self.center_point[0] - ball2.center_point[0])

    def apply_gravity(self, dt,  gravitator: tuple = None, negative=False):
        # linear
        if not gravitator:
            self.dy += Ball.gravity * dt
            return
        #  mouse
        angle = math.atan2(gravitator[1] - self.center_point[1], gravitator[0] - self.center_point[0])
        gravity = -Ball.gravity * 8 if negative else Ball.gravity
        self.dx += (gravity * math.cos(angle)) * dt
        self.dy += (gravity * math.sin(angle)) * dt

    @staticmethod
    def collide(ball1, ball2):
        """Handle a collision between two balls with a specified coefficient of restitution."""

        # Calculate the angle of collision
        angle = ball1.get_ball_v_ball_angle(ball2)

        # Velocity components along the angle of collision
        v1 = (ball1.dx, ball1.dy)
        v2 = (ball2.dx, ball2.dy)

        # Using the angle to project velocities onto the collision axis
        v1_parallel = (v1[0] * math.cos(angle) + v1[1] * math.sin(angle))
        v1_perpendicular = (-v1[0] * math.sin(angle) + v1[1] * math.cos(angle))
        v2_parallel = (v2[0] * math.cos(angle) + v2[1] * math.sin(angle))
        v2_perpendicular = (-v2[0] * math.sin(angle) + v2[1] * math.cos(angle))

        # Apply the collision formula for parallel components with the coefficient of restitution
        v1_parallel_new = ((ball1.mass - Ball.energy_loss_coefficient * ball2.mass) * v1_parallel + (1 + Ball.energy_loss_coefficient) * ball2.mass * v2_parallel) / (ball1.mass + ball2.mass)
        v2_parallel_new = ((ball2.mass - Ball.energy_loss_coefficient * ball1.mass) * v2_parallel + (1 + Ball.energy_loss_coefficient) * ball1.mass * v1_parallel) / (ball1.mass + ball2.mass)

        # The perpendicular components (motion perpendicular to the line of collision) remain unchanged
        v1_new = (
            v1_parallel_new * math.cos(angle) - v1_perpendicular * math.sin(angle),
            v1_parallel_new * math.sin(angle) + v1_perpendicular * math.cos(angle)
        )

        v2_new = (
            v2_parallel_new * math.cos(angle) - v2_perpendicular * math.sin(angle),
            v2_parallel_new * math.sin(angle) + v2_perpendicular * math.cos(angle)
        )
        # Update the velocities
        ball1.dx, ball1.dy = v1_new
        ball2.dx, ball2.dy = v2_new

    @staticmethod
    def remove_overlap(ball1, ball2):
        space = 1
        dist = ball1.radius + ball2.radius + space
        angle = ball2.get_ball_v_ball_angle(ball1)
        ball2.center_point = [ball1.center_point[0] + dist * math.cos(angle),
                              ball1.center_point[1] + dist * math.sin(angle)]
        ball1.center_point = [ball2.center_point[0] + dist * math.cos(angle + math.pi),
                              ball2.center_point[1] + dist * math.sin(angle + math.pi)]

    @staticmethod
    def check_overlap():
        for ball1 in Ball.list:
            for ball2 in Ball.list:
                distance = math.dist(ball1.center_point, ball2.center_point)
                if ball1 is not ball2 and distance < ball1.radius + ball2.radius:
                    return True
        return False

    @staticmethod
    def apply_ball_v_ball_collision():
        for ball_index, ball1 in enumerate(Ball.list[:-1]):
            for ball2 in Ball.list[ball_index + 1:]:
                distance = math.dist(ball1.center_point, ball2.center_point)
                if distance <= ball1.radius + ball2.radius:
                    Ball.collide(ball1, ball2)
        overlap = True
        max_timer = 0.01
        start_time = time.perf_counter()
        while overlap:
            for i, ball1 in enumerate(Ball.list[:-1]):
                for ball2 in Ball.list[i:]:
                    distance = math.dist(ball1.center_point, ball2.center_point)
                    if distance < ball1.radius + ball2.radius:
                        Ball.remove_overlap(ball1, ball2)
                        #  print("remove overlap")
            overlap = Ball.check_overlap()
            if time.perf_counter() - start_time >= max_timer:
                print("lag")
                return

    @staticmethod
    def apply_all_movement(big_circle, dt, gravity_point):
        Ball.get_total_energy(big_circle.center_point[1] + big_circle.radius)
        Ball.apply_ball_v_ball_collision()
        for ball in Ball.list:
            ball.apply_gravity(dt)
            #ball.apply_gravity(dt, gravity_point, negative=True)#(win_x/2, win_y/2))
            ball.move(dt)
            big_circle.check_hit(ball, dt)

    @staticmethod
    def get_total_energy(min_floor):
        total_energy = 0
        for ball in Ball.list:
            # 1/2 m v ^ 2
            kinetic_energy = ((ball.dx + ball.dy) ** 2) * (ball.mass / 2)
            potential_energy = ball.mass * Ball.gravity * abs(min_floor - ball.center_point[1])  # mgh
            total_energy += kinetic_energy + potential_energy
        return total_energy

def get_color():
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)
    a = random.randrange(256)
    return pygame.color.Color(r, g, b, a)


def get_midpoint(point1, point2):
    # returns a list of averaged coordinates
    return [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]


def get_angle(start_point, end_point):
    # returns an angle given two points
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    return math.atan2(dy, dx)


def main():
    # everything is ran here
    pygame.init()

    screen = pygame.display.set_mode([win_x, win_y])
    clock = pygame.time.Clock()

    big_circle = Bounce_Circle(screen)
    NUM_BALLS = 50
    for _ in range(NUM_BALLS):
        Ball(big_circle=big_circle, screen=screen)

    is_closed = False
    while not is_closed:
        screen.fill("black")
        Circle.draw_all()
        dt = clock.tick(60) / 1000
        pygame.display.flip()
        Ball.apply_all_movement(big_circle, dt, pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_closed = True


if __name__ == "__main__":
    main()
