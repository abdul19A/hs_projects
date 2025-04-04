import pygame
import math
import random
from Utilities import check_box, slider

window_x, window_y = 1200, 720


class Text:
    def __init__(self, text, x, y):
        self.text = text
        self.font = pygame.font.Font(None, 15)
        self.text_surface = self.font.render(text, True, "white")
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (x, y)

    def set_text(self, text):
        self.text_surface = self.font.render(text, True, "white")

    def draw(self, surface, cur_pos):
        self.text_rect.center = cur_pos[0] + 10, cur_pos[1] + 10
        surface.blit(self.text_surface, self.text_rect)


class Planet:
    can_do_trails = False
    can_attract = True
    can_do_elastic_collisions = False
    can_do_any_collision = True
    allow_mouse_drag = False
    all = []
    drag_coef = 0.0
    trail_length = 200
    grav_constant = 5
    simulation_speed = 100

    def __init__(self, size=None, color=None, x=None, y=None, dx=None, dy=None,
                 is_random=False, mass=None, can_attract=True, can_be_attracted=True,
                 is_solar_system=False, solar_system_num=0, ax=0, ay=0):
        rand = random.randrange
        if is_random:
            # set random values if is random is set to true
            self.size = rand(2, 5)
            self.color = pygame.color.Color(rand(256), rand(256), rand(256))
            self.x = rand(window_x) if not x else x
            self.y = rand(window_y) if not y else y
            self.dx = rand(-11, 10) if not dx else dx
            self.dy = rand(-11, 10) if not dy else dy

        elif is_solar_system:
            reference_point = (window_x / 2, window_y / 2)
            self.x = reference_point[0] + solar_system_num * rand(10, 20) + 50
            self.y = reference_point[1] - solar_system_num * rand(10, 20) - 50
            self.dx = 5 - solar_system_num ** .333
            self.dy = 5 - solar_system_num ** .333
            self.color = pygame.color.Color(rand(256), rand(256), rand(256))
            self.size = 3
            can_attract = False
        else:
            self.size = size
            self.color = color
            self.x, self.y = x, y
            self.dx, self.dy = dx, dy
        self.mass = self.size / 10 if not mass else mass
        self.trail_list = []
        self.can_attract = can_attract
        self.can_be_attracted = can_be_attracted
        self.mass_text = Text(f"{self.mass:.2f}", self.x, self.y)
        self.speed_text = Text(f"{self.get_speed():.2f}p/f", self.x, self.y + 10)
        self.ax = ax
        self.ay = ay
        Planet.all.append(self)

    def get_speed(self):
        return (self.dx ** 2 + self.dy ** 2) ** .5

    def move(self, dt):

        self.dx += -(Planet.drag_coef / self.mass) * self.dx * dt
        self.dy += -(Planet.drag_coef / self.mass) * self.dy * dt

        self.x += self.dx * dt * Planet.simulation_speed
        self.y += self.dy * dt * Planet.simulation_speed

    def draw(self, screen):
        pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=[self.x, self.y],
            radius=self.size
        )

    def get_angle(self, planet):
        dx = planet.x - self.x
        dy = planet.y - self.y
        return math.atan2(dy, dx)

    def get_pos(self) -> tuple:
        return self.x, self.y

    def create_trail(self):
        if Planet.can_do_trails:
            self.trail_list.append([self.x, self.y])
            if len(self.trail_list) > Planet.trail_length:
                self.trail_list.pop(0)

    @staticmethod
    def mouse_drag(mdx, mdy):
        for planet in Planet.all:
            planet.x -= mdx
            planet.y -= mdy
            for trail in planet.trail_list:
                trail[0] -= mdx
                trail[1] -= mdy

    @staticmethod
    def draw_trail(screen):
        for planet in Planet.all:
            if len(planet.trail_list) >= 2:
                pygame.draw.lines(
                    surface=screen,
                    color=planet.color,
                    closed=False,
                    points=planet.trail_list,
                    width=2
                )

    @staticmethod
    def draw_attraction_string(screen):
        for planet1 in Planet.all:
            for planet2 in Planet.all:
                if planet1 is not planet2 and planet1.can_attract:
                    pygame.draw.line(
                        surface=screen,
                        color="grey",
                        start_pos=planet1.get_pos(),
                        end_pos=planet2.get_pos(),
                        width=1
                    )

    @staticmethod
    def update_all(screen, dt):
        Planet.do_planet_interactions(dt)
        for planet in Planet.all:
            planet.create_trail()
            planet.move(dt)
            planet.draw(screen)

    @staticmethod
    def elastic_collision(planet1, planet2, distance):
        """Handle an elastic collision between two planets."""
        if planet1.size + planet2.size >= distance:  # Check if planets are colliding
            # Calculate the angle of collision
            angle = planet1.get_angle(planet2)

            # Velocity components along the angle of collision
            v1 = [planet1.dx, planet1.dy]
            v2 = [planet2.dx, planet2.dy]

            # Using the angle to project velocities onto the collision axis
            v1_parallel = (v1[0] * math.cos(angle) + v1[1] * math.sin(angle))
            v1_perpendicular = (-v1[0] * math.sin(angle) + v1[1] * math.cos(angle))
            v2_parallel = (v2[0] * math.cos(angle) + v2[1] * math.sin(angle))
            v2_perpendicular = (-v2[0] * math.sin(angle) + v2[1] * math.cos(angle))

            # Apply the elastic collision formula for parallel components (motion along the line of collision)
            v1_parallel_new = ((planet1.mass - planet2.mass) * v1_parallel + 2 * planet2.mass * v2_parallel) / (
                    planet1.mass + planet2.mass)
            v2_parallel_new = ((planet2.mass - planet1.mass) * v2_parallel + 2 * planet1.mass * v1_parallel) / (
                    planet1.mass + planet2.mass)

            # The perpendicular components (motion perpendicular to the line of collision) remain unchanged
            v1_new = (
                v1_parallel_new * math.cos(angle) - v1_perpendicular * math.sin(angle),
                v1_parallel_new * math.sin(angle) + v1_perpendicular * math.cos(angle)
            )

            v2_new = (
                v2_parallel_new * math.cos(angle) - v2_perpendicular * math.sin(angle),
                v2_parallel_new * math.sin(angle) + v2_perpendicular * math.cos(angle)
            )
            #  print(v1, v1_new)
            # Update the velocities
            planet1.dx, planet1.dy = v1_new
            planet2.dx, planet2.dy = v2_new
            #  print("elastic")

    @staticmethod
    def inelastic_collision(planet1, planet2, distance):
        """Handle an inelastic collision between two planets."""
        if planet1.size + planet2.size >= distance:  # Check if planets are colliding
            # Calculate the angle of collision
            new_size = (planet1.size ** 3 + planet2.size ** 3) ** (1 / 3)
            new_mass = planet1.mass + planet2.mass

            new_dx = (planet1.dx * planet1.mass + planet2.dx * planet2.mass) / new_mass
            new_dy = (planet1.dy * planet1.mass + planet2.dy * planet2.mass) / new_mass

            new_can_be_attracted = not (planet1.can_be_attracted and planet2.can_be_attracted)
            new_can_attract = planet1.can_attract or planet2.can_attract

            next_location = (planet1.x, planet1.y) if planet1.mass > planet2.mass else (planet2.x, planet2.y)
            Planet.all.remove(planet1)
            Planet.all.remove(planet2)
            rand = random.randrange
            Planet(size=new_size, mass=new_mass,
                   color=pygame.color.Color(rand(256), rand(256), rand(256)),
                   x=next_location[0], y=next_location[1], dx=new_dx, dy=new_dy,
                   can_be_attracted=new_can_be_attracted, can_attract=new_can_attract)

    @staticmethod
    def do_planet_interactions(dt):
        # get forces
        if Planet.can_attract:
            for planet1 in Planet.all:
                planet1.ax = 0
                planet1.ay = 0
                for planet2 in Planet.all:
                    if planet1 is not planet2:
                        planet_distance = math.dist(planet1.get_pos(), planet2.get_pos())
                        planet1.get_forces(planet2, planet_distance)

        # move
        for planet in Planet.all:
            planet.update_velocity_after_force(dt)
        # check for collisions
        if not Planet.can_do_any_collision:
            return

        for planet1 in Planet.all:
            for planet2 in Planet.all:
                if planet1 is not planet2 and planet1 in Planet.all and planet2 in Planet.all:
                    planet_distance = math.dist(planet1.get_pos(), planet2.get_pos())
                    if Planet.can_do_elastic_collisions:
                        Planet.elastic_collision(planet1, planet2, planet_distance)
                    else:
                        Planet.inelastic_collision(planet1, planet2, planet_distance)

    def bounce(self):
        if self.x + self.size > window_x:
            self.dx = -abs(self.dx)
            self.x = window_x - self.size
        elif self.x < self.size:
            self.dx = abs(self.dx)
            self.x = self.size
        if self.y + self.size > window_y:
            self.dy = -abs(self.dy)
            self.y = window_y - self.size
        elif self.y < self.size:
            self.dy = abs(self.dy)
            self.y = self.size

    @staticmethod
    def apply_wall(win_x, win_y):
        for planet in Planet.all:
            if planet.x > win_x - planet.size:
                planet.x = win_x - planet.size
                planet.dx = -abs(planet.dx)
            elif planet.x < planet.size:
                planet.x = planet.size
                planet.dx = abs(planet.dx)
            if planet.y > win_y - planet.size:
                planet.y = win_y - planet.size
                planet.dy = -abs(planet.dy)
            elif planet.y < planet.size:
                planet.y = planet.size
                planet.dy = abs(planet.dy)

    @staticmethod
    def remove_all_trails():
        for planet in Planet.all:
            planet.trail_list = []

    @staticmethod
    def show_mass(screen):
        for planet in Planet.all:
            planet.mass_text.draw(screen, planet.get_pos())

    @staticmethod
    def show_speed(screen):
        for planet in Planet.all:
            planet.speed_text.set_text(f"{planet.get_speed():.2f}p/f")
            x, y = planet.get_pos()
            planet.speed_text.draw(screen, (x, y + 10))

    @staticmethod
    def circle():
        num = 20
        d_theta = math.pi * 2 / num
        radius = window_y / 3
        for i in range(num):
            theta = d_theta * i
            x, y = radius * math.cos(theta) + window_x / 2, radius * math.sin(theta) + window_y / 2
            Planet(is_random=True, x=x, y=y, dx=0, dy=0)

    @staticmethod
    def show_dir(surface):
        line_size = 2
        for planet in Planet.all:
            line_end_pos = (planet.x + planet.dx * line_size, planet.y + planet.dy * line_size)
            angle = math.atan2(planet.dy, planet.dx)
            arrow_p1 = (line_end_pos[0] + line_size * math.cos(angle + math.pi / 2),
                        line_end_pos[1] + line_size * math.sin(angle + math.pi / 2))
            arrow_p2 = (line_end_pos[0] + line_size * math.cos(angle - math.pi / 2),
                        line_end_pos[1] + line_size * math.sin(angle - math.pi / 2))
            arrow_p3 = (
                line_end_pos[0] + line_size * 2 * math.cos(angle), line_end_pos[1] + line_size * 2 * math.sin(angle))
            pygame.draw.line(
                surface=surface,
                color="white",
                start_pos=planet.get_pos(),
                end_pos=line_end_pos
            )
            pygame.draw.polygon(
                surface=surface,
                color="white",
                points=(arrow_p1, arrow_p2, arrow_p3)
            )

    @staticmethod
    def show_acs(surface):
        line_size = 2
        multiplier = 8
        for planet in Planet.all:
            line_end_pos = (planet.x + planet.ax * line_size * multiplier, planet.y + planet.ay * line_size * multiplier)
            angle = math.atan2(planet.ay, planet.ax)
            arrow_p1 = (line_end_pos[0] + line_size * math.cos(angle + math.pi / 2),
                        line_end_pos[1] + line_size * math.sin(angle + math.pi / 2))
            arrow_p2 = (line_end_pos[0] + line_size * math.cos(angle - math.pi / 2),
                        line_end_pos[1] + line_size * math.sin(angle - math.pi / 2))
            arrow_p3 = (
                line_end_pos[0] + line_size * 2 * math.cos(angle), line_end_pos[1] + line_size * 2 * math.sin(angle))
            pygame.draw.line(
                surface=surface,
                color="blue",
                start_pos=planet.get_pos(),
                end_pos=line_end_pos
            )
            pygame.draw.polygon(
                surface=surface,
                color="blue",
                points=(arrow_p1, arrow_p2, arrow_p3)
            )

    def get_forces(self, planet2, distance):
        if distance <= self.size + planet2.size or \
                not self.can_be_attracted or\
                not planet2.can_attract:
            return
        force = Planet.grav_constant * self.mass * planet2.mass / distance ** 2
        planet1_acceleration = force / self.mass
        planet1_angle = self.get_angle(planet2)

        ax1 = planet1_acceleration * math.cos(planet1_angle)
        ay1 = planet1_acceleration * math.sin(planet1_angle)
        self.ax += ax1
        self.ay += ay1

    def update_velocity_after_force(self, dt):
        self.dx += self.ax * dt * Planet.simulation_speed
        self.dy += self.ay * dt * Planet.simulation_speed


class Event:
    win_closed: bool = False
    mouse_clicked: bool = False
    mouse_held: bool = False
    mouse_pos: tuple = (window_x // 2, window_y // 2)
    mouse_down_pos = mouse_pos

    @staticmethod
    def update():
        Event.mouse_clicked = False
        if Event.mouse_held:
            m_x, m_y = pygame.mouse.get_pos()
            slider.Slider.update(m_x, m_y)
            if Planet.allow_mouse_drag:
                m1_x, m1_y = Event.mouse_down_pos
                Planet.mouse_drag(m1_x - m_x, m1_y-m_y)
                Event.mouse_down_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Event.win_closed = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Event.mouse_clicked = True
                Event.mouse_held = True
                Event.mouse_down_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = pygame.mouse.get_pos()
                if m_x <= 100 or m_y <= 100:
                    check_box.CheckBox.update(m_x, m_y)
                elif not Planet.allow_mouse_drag:
                    Planet(is_random=True, x=m_x, y=m_y, mass=50)
                Event.mouse_held = False


def initialize():
    Planet(size=10, color="grey", x=window_x / 2, y=window_y / 2, dx=0, dy=0, mass=5000, can_be_attracted=False)
    for z in range(20):
        Planet(is_solar_system=True, solar_system_num=z)


def main(window_width, window_height):
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    window_fill = "black"
    clock = pygame.time.Clock()

    # ------ initializations ------
    initialize()
    box1 = check_box.CheckBox(10, 10, 30, "red", "string")
    box2 = check_box.CheckBox(10, 10, 60, "red", "wall")
    box3 = check_box.CheckBox(10, 10, 90, "red", "trail")
    box4 = check_box.CheckBox(10, 10, 120, "red", "show mass")
    box5 = check_box.CheckBox(10, 10, 150, "red", "reset")
    box6 = check_box.CheckBox(10, 10, 180, "red", "elastic")
    box7 = check_box.CheckBox(10, 10, 210, "red", "collisions", checked=True)
    box8 = check_box.CheckBox(10, 10, 240, "red", "gravity", checked=True)
    box9 = check_box.CheckBox(10, 10, 270, "red", "circle")
    box10 = check_box.CheckBox(10, 10, 300, "red", "show dir")
    box11 = check_box.CheckBox(10, 10, 330, "red", "show acs")
    box12 = check_box.CheckBox(10, 10, 360, "red", "show spd")
    box13 = check_box.CheckBox(10, 10, 390, "red", "mouse drg")
    slider1 = slider.Slider(100, 30, 100, 10, "sim speed", "red", percentage_start=.0)
    slider2 = slider.Slider(250, 30, 100, 10, "drag", "red", percentage_start=.0)
    slider3 = slider.Slider(400, 30, 100, 10, "big g", "red", percentage_start=.1)

    # --- initializations end -----

    def do_check_list_functions():
        if box1.is_checked:
            Planet.draw_attraction_string(window)
        if box2.is_checked:
            Planet.apply_wall(window_width, window_height)
        if box3.is_checked:
            Planet.can_do_trails = True
            Planet.draw_trail(window)
        else:
            Planet.can_do_trails = False
            Planet.remove_all_trails()
        if box4.is_checked:
            Planet.show_mass(window)
        if box5.is_checked:
            Planet.all = []
            initialize()
            box5.is_checked = False
        if box6.is_checked:
            Planet.can_do_elastic_collisions = True
        else:
            Planet.can_do_elastic_collisions = False
        if box7.is_checked:
            Planet.can_do_any_collision = True
            box6.color = "red"
        else:
            Planet.can_do_any_collision = False
            box6.color = "gray"
        if box8.is_checked:
            Planet.can_attract = True
            box1.color = "red"
        else:
            Planet.can_attract = False
            box1.is_checked = False
            box1.color = "gray"

        if box9.is_checked:
            Planet.circle()
            box9.is_checked = False
        if box10.is_checked:
            Planet.show_dir(window)
        if box11.is_checked:
            Planet.show_acs(window)
        if box12.is_checked:
            Planet.show_speed(window)
        if box13.is_checked:
            Planet.allow_mouse_drag = True
        else:
            Planet.allow_mouse_drag = False
        Planet.simulation_speed = slider1.percentage * 100
        Planet.drag_coef = slider2.percentage ** 3
        Planet.grav_constant = slider3.percentage * 2 / .1

    while not Event.win_closed:
        window_width, window_height = window.width, window.height
        Event.update()
        dt = clock.tick(60) / 1000
        pygame.display.set_caption(f"Gravity, FPS: {clock.get_fps():.2f}")
        if dt > 1:
            dt = 0
        window.fill(window_fill)

        Planet.update_all(window, dt)
        do_check_list_functions()

        check_box.CheckBox.draw_all(window)
        slider.Slider.draw_all(window)
        pygame.display.flip()


if __name__ == "__main__":
    main(window_x, window_y)
