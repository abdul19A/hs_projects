from math import *
import pygame
from Utilities.input_box import InputBox
import time
import warnings


# This is a graph that can make any function
warnings.filterwarnings("ignore", category=SyntaxWarning)
# window size
WIN_X, WIN_Y = 650, 650
# each cordinate is stored in a list
# the x value is the first index and the y is the second
X, Y = 0, 1
start = time.perf_counter()

# the graph that is based on the window
def taylor(x: float, i: int):

    sum = 0
    for i in range(i):
        sum += x ** i / factorial(i)
    return sum

class Graph:
    def __init__(self,
                 x_start: float = -10,
                 x_end: float = 10,
                 x_grid_step: float = 1,
                 y_start: float = -10,
                 y_end: float = 10,
                 y_grid_step: float = 1):
        # sets up the graph's grid, which is like a graphing calculator
        self.x_start = x_start
        self.x_end = x_end
        self.x_grid_step = x_grid_step

        self.y_start = y_start
        self.y_end = y_end
        self.y_grid_step = y_grid_step

        # gets the middle of the graph
        self.type: type = float
        self.check_graph_validity()

        self.y_mid = (self.y_start + self.y_end) / 2
        self.x_mid = (self.x_start + self.x_end) / 2

        self.graph_win_x_ratio = WIN_X / (self.x_end - self.x_start)
        self.graph_win_y_ratio = -(WIN_Y / (self.y_end - self.y_start))
        self.grid_lines = []
        self.create_grid_lines()

    def check_graph_validity(self):
        errors = ["the following error(s) have occurred: \n"]
        if isinstance(self.y_start, complex) != isinstance(self.y_end, complex):
            errors.append("INVALID IMAGINARY - FLOAT ASSIGNMENT")
        elif isinstance(self.y_start, complex):
            self.type = complex
            self.y_start = self.y_start.imag
            self.y_end = self.y_end.imag
            self.y_grid_step = self.y_grid_step.imag
        if self.x_end <= self.x_start:
            errors.append("INVALID X DIMENSIONS\n")
        if self.y_end <= self.y_start:
            errors.append("INVALID Y DIMENSIONS\n")
        if self.x_grid_step <= 0:
            errors.append("INVALID X GRID STEP\n")
        if self.y_grid_step <= 0:
            errors.append("INVALID Y GRID STEP\n")
        if len(errors) > 1:
            errors_string = "".join(errors)
            raise ValueError(errors_string)

    def translate_points(self, graph_point) -> list:
        # there is two types of points, a graph and a window point
        win_point = graph_point.copy()
        # a graph point is a point from a function, a window point is where it is on the screen
        win_point[X] *= self.graph_win_x_ratio
        win_point[Y] *= self.graph_win_y_ratio

        win_point[X] += WIN_X/2 - self.x_mid * self.graph_win_x_ratio
        win_point[Y] += WIN_Y/2 - self.y_mid * self.graph_win_y_ratio

        return win_point

    def create_grid_lines(self):
        i = 0
        while i < self.y_end:
            if i > self.y_start:
                isBold = False
                if i == 0:
                    isBold = True
                grid_point1 = self.translate_points([self.x_start, i])
                grid_point2 = self.translate_points([self.x_end, i])
                self.grid_lines.append([grid_point1, grid_point2, isBold])
            i += self.y_grid_step
        i = 0
        while i > self.y_start:
            if i < self.y_end:
                isBold = False
                if i == 0:
                    isBold = True
                grid_point1 = self.translate_points([self.x_start, i])
                grid_point2 = self.translate_points([self.x_end, i])
                self.grid_lines.append([grid_point1, grid_point2, isBold])
            i -= self.y_grid_step
        i = 0
        while i < self.x_end:
            if i > self.x_start:
                isBold = False
                if i == 0:
                    isBold = True
                grid_point1 = self.translate_points([i, self.y_start])
                grid_point2 = self.translate_points([i, self.y_end])
                self.grid_lines.append([grid_point1, grid_point2, isBold])
            i += self.x_grid_step
        i = 0
        while i > self.x_start:
            if i < self.x_end:
                isBold = False
                if i == 0:
                    isBold = True
                grid_point1 = self.translate_points([i, self.y_start])
                grid_point2 = self.translate_points([i, self.y_end])
                self.grid_lines.append([grid_point1, grid_point2, isBold])
            i -= self.x_grid_step

    def draw(self,screen):
        for line in self.grid_lines:
            if self.type == complex:
                pygame.draw.line(surface=screen,
                                 color="white" if line[2] else "gray", # makes x y axis white
                                 start_pos=[line[0][X].real, line[0][Y].real],
                                 end_pos=[line[1][X].real, line[1][Y].real],
                                 width=2 if line[2] else 1) # makes x y axis bolder
            else:
                pygame.draw.line(surface=screen,
                                 color="white" if line[2] else "gray", # makes x y axis white
                                 start_pos=line[0],
                                 end_pos=line[1],
                                 width=2 if line[2] else 1) # makes x y axis bolder


class Function:
    x_step = 0.001

    def __init__(self, y: str, graph: Graph):
        self.equation = y.lower()
        self.graph = graph

        # 2d list containing all points (not to be confused with just y values)
        self.graph_points = []
        self.window_points = []
        self.error = None
        self.evaluate_points()

    def evaluate_points(self):
        # the starting x value is the start of the graphs smallest x value
        cur_x = self.graph.x_start
        end_x = self.graph.x_end
        # "end_x + 0.1" this is done because of small errors in some numbers
        while cur_x < end_x + 0.000_000_000_1:
            # replaces the "x" with a value which is turned into a string, and stores the evaluation in cur_y
            cur_y = self.eval_function(cur_x)
            # checks if the point is real
            graph_point = [cur_x, cur_y]
            self.graph_points.append(graph_point)
            # point is translated then is stored
            if cur_y:
                self.window_points.append(self.graph.translate_points(graph_point))
            else:
                self.window_points.append(None)
            cur_x += Function.x_step

    def eval_function(self, cur_x):

        try:
            if self.graph.type == complex:
                val = eval(self.equation.replace("x", "(" + str(cur_x) + ")")).imag
            else:
                val = eval(self.equation.replace("x", "(" + str(cur_x) + ")"))
                if isinstance(val, complex):
                    return None
        except Exception as error:
            self.error = error
            return None
        return val

    def draw(self, screen):
        for point_index in range(len(self.window_points) - 1):
            point1, point2 = self.window_points[point_index], self.window_points[point_index+1]
            if None not in (point1, point2):
                pygame.draw.line(surface=screen,
                                  color="red",
                                  start_pos=point1,
                                  end_pos=point2,
                                  width=1)

    def change(self, new_equation):
        self.__init__(new_equation, self.graph)

    def print_error(self):
        if self.error:
            print("error: " + str(self.error))
        self.error = None
def main():
    win = pygame.display.set_mode([WIN_X, WIN_Y])
    clock = pygame.time.Clock()

    win_color = "black"

    new = Graph(x_start=-10,
                x_end=10,
                x_grid_step=1,
                y_start=-10,
                y_end=10,
                y_grid_step=1)
    f1 = Function(y="", graph=new)
    run = True
    new_input = InputBox(0,0,100,30,"")

    while run:
        win.fill(win_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            text = new_input.handle_event(event)
            if text != "":
                f1.change(new_input.handle_event(event))

        new_input.update()
        new.draw(screen=win)
        f1.draw(screen=win)
        f1.print_error()

        new_input.draw(win)

        clock.tick(120)
        pygame.display.flip()


if __name__ == "__main__":
    main()
