import pygame
from math import cos, sin, atan2
import numpy as np
import random
# constants
GRAVITY = 0

def get_axes(corners):
    """Returns the perpendicular (normal) vectors of a rectangle's edges."""
    axes = []
    for i in range(4):
        p1, p2 = corners[i], corners[(i + 1) % 4]
        edge = np.array(p2) - np.array(p1)
        normal = np.array([-edge[1], edge[0]])  # Perpendicular vector
        normal /= np.linalg.norm(normal)  # Normalize
        axes.append(normal)
    return axes

def project_corners(corners, axis):
    """Projects a rectangle's corners onto an axis and returns the min & max projection values, and the extreme points."""
    corners = np.array(corners)
    projections = np.dot(corners, axis)
    min_proj, max_proj = min(projections), max(projections)
    min_point = corners[np.argmin(projections)]
    max_point = corners[np.argmax(projections)]
    return min_proj, max_proj, min_point, max_point

def sat_collision(rect1, rect2):
    """
    Uses SAT to check collision between two sets of corners.
    Returns a tuple: (collided: bool, collision_point, collision_normal)
    """
    rect1 = np.array(rect1)
    rect2 = np.array(rect2)
    axes = get_axes(rect1) + get_axes(rect2)

    min_overlap = float('inf')
    collision_normal = None
    contact_points = []

    for axis in axes:
        min1, max1, min_p1, max_p1 = project_corners(rect1, axis)
        min2, max2, min_p2, max_p2 = project_corners(rect2, axis)

        # If there's a separating axis, there is no collision.
        if max1 < min2 or max2 < min1:
            return False, None, None

        # Find the smallest overlap.
        overlap = min(max1 - min2, max2 - min1)
        if overlap < min_overlap:
            min_overlap = overlap
            collision_normal = axis
            # Choose contact points based on the overlap direction.
            if max1 - min2 < max2 - min1:
                contact_points = [max_p1, min_p2]
            else:
                contact_points = [max_p2, min_p1]

    collision_point = np.mean(contact_points, axis=0)
    return True, collision_point, collision_normal

def resolve_collision(obj1, obj2, collision_normal, collision_point):
    """
    Applies an impulse-based collision response to obj1 and obj2 at the given collision point.
    The collision_normal should be normalized.
    """
    # Convert collision point and object centers to numpy arrays.
    cp = np.array(collision_point)
    pos1 = np.array([obj1.x, obj1.y])
    pos2 = np.array([obj2.x, obj2.y])

    # Vectors from centers to collision point.
    r1 = cp - pos1
    r2 = cp - pos2

    # For 2D, the perpendicular (rotational) contribution is given by:
    # omega cross r = (-omega * r_y, omega * r_x)
    v1 = np.array([obj1.dx, obj1.dy]) + np.array([-obj1.angular_velocity * r1[1], obj1.angular_velocity * r1[0]])
    v2 = np.array([obj2.dx, obj2.dy]) + np.array([-obj2.angular_velocity * r2[1], obj2.angular_velocity * r2[0]])
    v_rel = v1 - v2

    # Relative velocity along the collision normal.
    v_rel_normal = np.dot(v_rel, collision_normal)

    # Do not resolve if objects are separating.
    if v_rel_normal > 0:
        return

    # Coefficient of restitution (1 = perfectly elastic)
    e = 1.0

    # Inverse mass (if an object is static, treat its inverse mass as 0).
    inv_mass1 = 0 if obj1.is_static else 1 / obj1.mass
    inv_mass2 = 0 if obj2.is_static else 1 / obj2.mass

    # Moment of inertia for a rectangle: I = m*(width^2 + height^2) / 12.
    # For static objects, we treat the rotational inverse as 0.
    I1 = 0 if obj1.is_static else (obj1.mass * (obj1.width ** 2 + obj1.height ** 2) / 12)
    I2 = 0 if obj2.is_static else (obj2.mass * (obj2.width ** 2 + obj2.height ** 2) / 12)
    inv_I1 = 0 if I1 == 0 else 1 / I1
    inv_I2 = 0 if I2 == 0 else 1 / I2

    # For rotation: in 2D, r_perp dot n (with r_perp = (-r_y, r_x))
    r1_perp_dot_n = np.dot(np.array([-r1[1], r1[0]]), collision_normal)
    r2_perp_dot_n = np.dot(np.array([-r2[1], r2[0]]), collision_normal)

    # Denominator of impulse scalar.
    denom = inv_mass1 + inv_mass2 + (r1_perp_dot_n ** 2) * inv_I1 + (r2_perp_dot_n ** 2) * inv_I2
    if denom == 0:
        return

    # Impulse magnitude.
    j = -(1 + e) * v_rel_normal / denom

    impulse = j * collision_normal

    # Update linear velocities.
    if not obj1.is_static:
        obj1.dx += impulse[0] * inv_mass1
        obj1.dy += impulse[1] * inv_mass1
        # Update angular velocity (scalar in 2D is the cross product of r and impulse).
        obj1.angular_velocity += np.cross(r1, impulse) * inv_I1

    if not obj2.is_static:
        obj2.dx -= impulse[0] * inv_mass2
        obj2.dy -= impulse[1] * inv_mass2
        obj2.angular_velocity -= np.cross(r2, impulse) * inv_I2

# A helper function to compute the length of a vector (used to compute the circumscribed radius).
def c_squared(a, b):
    return (a ** 2 + b ** 2) ** 0.5

###############################################################################
# Classes for your simulation
###############################################################################

class rectangle:
    list = []

    def __init__(self, x, y, width, height, color="red", mass=1.0, is_static=False):
        self.x, self.y = x, y
        self.mid = [x, y]
        self.width, self.height = width, height
        self.color = color

        # Use the diagonal as the radius to rotate the corners.
        self.rad = c_squared(width, height) / 2

        # Physical properties.
        self.mass = mass
        self.is_static = is_static  # For platforms, etc.
        self.dx = 0  # Linear velocity components
        self.dy = 0
        self.angular_velocity = 0
        self.delta_angle = 0

        # Set up corner points relative to the center.
        self.points = [
            [x - width / 2, y - height / 2],
            [x + width / 2, y - height / 2],
            [x + width / 2, y + height / 2],
            [x - width / 2, y + height / 2]
        ]
        # Store the initial angles (relative to center) for rotation.
        self.angles_i = [atan2(point[1] - self.y, point[0] - self.x) for point in self.points]

        rectangle.list.append(self)

    def rotate(self, dt):
        self.delta_angle += self.angular_velocity * dt

    def despawn(self, win_x, win_y):
        if not (-50 < self.x < win_x + 50 and -50 < self.y < win_y + 50):
            rectangle.list.remove(self)

    def update(self, dt):
        self.rotate(dt)
        # Recalculate the corner positions based on the current rotation.
        self.points = [
            [self.x + (self.width / 2) * cos(angle + self.delta_angle) - (self.height / 2) * sin(angle + self.delta_angle),
             self.y + (self.width / 2) * sin(angle + self.delta_angle) + (self.height / 2) * cos(angle + self.delta_angle)]
            for angle in self.angles_i
        ]

    def draw(self, surface):
        pygame.draw.polygon(surface=surface, color=self.color, points=self.points)

    @staticmethod
    def update_all(main):
        rectangle.do_collisions()
        for rect in rectangle.list:
            rect.update(main.dt)
            rect.despawn(main.surface.get_width(), main.surface.get_height())

    @staticmethod
    def draw_all(surface):
        for rect in rectangle.list:
            rect.draw(surface)

    @staticmethod
    def do_collisions():
        # Check every unique pair for collisions.
        for i, rect1 in enumerate(rectangle.list):
            for rect2 in rectangle.list[i+1:]:
                collided, collision_point, collision_normal = sat_collision(rect1.points, rect2.points)
                if collided:
                    # For debugging: print the collision point.
                    x, y = collision_point
                    print(f"Collision at: {x:.2f}, {y:.2f}")
                    resolve_collision(rect1, rect2, collision_normal, collision_point)

# cube is a dynamic rectangle.
class cube(rectangle):
    def __init__(self, x, y, size, color="blue", mass=1.0):
        # For cubes, width and height are the same.
        super(cube, self).__init__(x, y, size, size, color, mass, is_static=False)
        self.dx = random.randrange(-50, 50)
        self.dy = random.randrange(-50, 50)
        self.angular_velocity = random.randrange(-5, 5, 1)   # Initial angular velocity

    def move(self, dt):
        # Apply gravity.
        self.dy += GRAVITY * dt
        self.x += self.dx * dt
        self.y += self.dy * dt

    def update(self, dt):
        self.rotate(dt)
        self.move(dt)
        self.points = [
            [self.x + (self.width / 2) * cos(angle + self.delta_angle) - (self.height / 2) * sin(angle + self.delta_angle),
             self.y + (self.width / 2) * sin(angle + self.delta_angle) + (self.height / 2) * cos(angle + self.delta_angle)]
            for angle in self.angles_i
        ]

###############################################################################
# Main Application
###############################################################################

class Main:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.mid = (width / 2, height / 2)
        self.clock = pygame.time.Clock()
        self.bg_color = "black"
        self.fps = 120
        self.is_running = True
        self.is_dragging = False
        self.drag_location = None

        # Create a static platform (rectangle) at the center.
        self.scale = rectangle(self.mid[0], self.mid[1], 300, 20, color="red", is_static=True)
        self.dt = 0

    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.is_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_dragging = False
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos is not None:
                    x, y = mouse_pos
                    # Spawn a new cube at the mouse position.
                    cube(x, y, 10, mass=1.0)

    def drag(self):
        if self.is_dragging:
            self.drag_location = pygame.mouse.get_pos()

    def update(self):
        self.dt = self.clock.tick(self.fps) / 1000
        pygame.display.flip()
        self.surface.fill(self.bg_color)
        self.inputs()
        self.drag()

    def run(self):
        while self.is_running:
            rectangle.update_all(self)
            rectangle.draw_all(self.surface)
            self.update()


if __name__ == "__main__":
    print("running")
    pygame.init()
    new = Main(800, 600)
    new.run()
    pygame.quit()
