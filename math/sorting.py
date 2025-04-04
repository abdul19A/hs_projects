import pygame
import random
import time
import sys
sys.setrecursionlimit(100000)

FPS = 60

PADDING = 50
NUM_RECTS = 1000

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

def check_dimension_validity():
    if SCREEN_WIDTH < NUM_RECTS or SCREEN_HEIGHT <= PADDING*2 + NUM_RECTS:
        raise ValueError(f"INVALID DIMENSIONS: {SCREEN_WIDTH}, {SCREEN_HEIGHT}")

class Rect:
    all_rects = []
    start_height, max_height = PADDING, SCREEN_HEIGHT - PADDING
    width = SCREEN_WIDTH/NUM_RECTS
    delta_height = abs((SCREEN_HEIGHT - PADDING) / NUM_RECTS)
    iterations = 0
    timer = time.perf_counter()

    @staticmethod
    def get_color(height):
        return int(height/NUM_RECTS * 255), 255, 255

    def __init__(self, pos_index, height_index):
        self.x = Rect.width * pos_index
        self.pixel_height = (height_index * Rect.delta_height) + PADDING + 1
        self.y = SCREEN_HEIGHT - self.pixel_height
        self.pos = pos_index
        self.height = height_index
        self.rect_shape = pygame.FRect(self.x, self.y, Rect.width, self.pixel_height)
        self.color = Rect.get_color(self.height)
        self.OG_COLOR = self.color

    def swap(self, rect2):
        Rect.all_rects[self.pos] = rect2
        Rect.all_rects[rect2.pos] = self
        self.pos, rect2.pos = rect2.pos, self.pos
        self.x = Rect.width * self.pos
        rect2.x = Rect.width * rect2.pos
        self.rect_shape = pygame.FRect(self.x, self.y, Rect.width, self.pixel_height)
        rect2.rect_shape = pygame.FRect(rect2.x, rect2.y, Rect.width, rect2.pixel_height)

    def shift(self, rect2):
        if self.pos < rect2.pos:
            for i in range(self.pos, rect2.pos):
                self.swap(Rect.all_rects[i + 1])
        elif self.pos > rect2.pos:
            for i in range(self.pos, rect2.pos, -1):
                self.swap(Rect.all_rects[i - 1])

    def is_greater_than(self, rect2):
        if self.height > rect2.height:
            return True
        return False

    def is_less_than(self, rect2):
        return not self.is_greater_than(rect2)

    @classmethod
    def is_sorted(cls, muted=True):
        for i, rect in enumerate(Rect.all_rects[:-1]):
            if rect.is_greater_than(Rect.all_rects[i+1]):
                if not muted:
                    print("failed at ", i)
                return False
        return True

    @classmethod
    def insert_sort(cls, surface, looper):
        for i in range(1, NUM_RECTS - 1):
            rect = Rect.all_rects[i]
            next_rect = Rect.all_rects[i+1]

            rect.color = "red"
            next_rect.color = "blue"

            cls.update(surface)
            looper.update()

            if rect.is_greater_than(next_rect):
                done = False
                for j in range(i+1):
                    this_rect = Rect.all_rects[j]
                    this_rect.color = "purple"

                    cls.update(surface)
                    looper.update()

                    if this_rect.is_greater_than(next_rect):
                        next_rect.shift(this_rect)
                        done = True
                    this_rect.color = this_rect.OG_COLOR

                    cls.update(surface)
                    looper.update()
                    if done:
                        break
            rect.color = rect.OG_COLOR
            next_rect.color = next_rect.OG_COLOR

            cls.update(surface)
            looper.update()

    @classmethod
    def quick_sort(cls, surface, looper, pivot_point=NUM_RECTS//2, start=0, end=NUM_RECTS):
        cls.iterations += 1
        pivot = Rect.all_rects[pivot_point]
        for rect2 in Rect.all_rects[start: end + 1]:
            if rect2 is not pivot:
                pivot.color = "red"
                rect2.color = "purple"

                cls.update(surface)
                looper.update()

                pivot_is_greater = pivot.is_greater_than(rect2)
                if (not pivot_is_greater and rect2.pos < pivot.pos) or (pivot_is_greater and rect2.pos > pivot.pos):
                    rect2.shift(pivot)
                    cls.iterations += 1

                pivot.color = pivot.OG_COLOR
                rect2.color = rect2.OG_COLOR

                cls.update(surface)
                looper.update()

        if end - start <= 2:
            return
        pivot_point = pivot.pos
        Rect.quick_sort(surface, looper, pivot_point=(start + pivot_point)//2, start=start, end=pivot_point)
        Rect.quick_sort(surface, looper, pivot_point=(end + pivot_point)//2, start=pivot_point, end=end)

    @classmethod
    def selection_sort(cls, surface, looper, min_i=0, max_i=NUM_RECTS-1):
        min_rect = Rect.all_rects[min_i]
        max_rect = Rect.all_rects[max_i]
        for i, rect in enumerate(Rect.all_rects[min_i: max_i+1]):
            min_rect.color = "blue"
            max_rect.color = "red"
            rect.color = "purple"

            cls.update(surface)
            looper.update()

            if rect.is_greater_than(max_rect):
                max_rect.color = max_rect.OG_COLOR
                max_rect = rect
                max_rect.color = "red"
                cls.iterations += 1
            elif min_rect.is_greater_than(rect):
                min_rect.color = min_rect.OG_COLOR
                min_rect = rect
                min_rect.color = "blue"
                cls.iterations += 1
            else:
                rect.color = rect.OG_COLOR

            cls.update(surface)
            looper.update()

        min_rect.color = min_rect.OG_COLOR
        max_rect.color = max_rect.OG_COLOR
        min_rect.swap(Rect.all_rects[min_i])
        max_rect.swap(Rect.all_rects[max_i])

        cls.update(surface)
        looper.update()
        if max_i - min_i > 2:
            cls.selection_sort(surface, looper, min_i + 1, max_i - 1)

    @classmethod
    def bubble_sort(cls, surface, looper):
        # update
        last = 1
        while not cls.is_sorted():
            for i in range(NUM_RECTS-last):
                cur_rect = Rect.all_rects[i]
                next_rect = Rect.all_rects[i+1]
                cur_rect.color = "red"
                next_rect.color = "blue"

                cls.update(surface)
                looper.update()

                if cur_rect.is_greater_than(next_rect):
                    cls.iterations += 1
                    cur_rect.swap(next_rect)

                cur_rect.color = cur_rect.OG_COLOR
                next_rect.color = next_rect.OG_COLOR

                cls.update(surface)
                looper.update()

            last += 1

    @classmethod
    def merge_sort_do_comparison(cls, surface, looper, merged_array):
        new_merged_array = []
        for a in range(0, len(merged_array)-1, 2):
            array1 = merged_array[a]
            array2 = merged_array[a+1]
            i, j = 0, 0
            new_merged_rects = []

            while i < len(array1) and j < len(array2):
                rect1 = array1[i]
                rect2 = array2[j]

                rect1.color = "red"
                rect2.color = "blue"

                cls.update(surface)
                looper.update()

                cls.iterations += 1
                if rect2.is_less_than(rect1):
                    rect2.shift(rect1)
                    new_merged_rects.append(rect2)
                    j += 1
                else:
                    new_merged_rects.append(rect1)
                    i += 1

                cls.update(surface)
                looper.update()

                rect1.color = rect1.OG_COLOR
                rect2.color = rect2.OG_COLOR
            new_merged_rects += array1[i:] + array2[j:]
            new_merged_array.append(new_merged_rects)

        if len(merged_array) % 2 == 1:
            new_merged_array.append(merged_array[-1])
        return new_merged_array

    @classmethod
    def merge_sort(cls, surface, looper):
        merged_array = []

        for i in range(0, NUM_RECTS, 2):
            rect1 = Rect.all_rects[i]
            rect2 = Rect.all_rects[i+1]

            rect1.color = "red"
            rect2.color = "blue"
            cls.update(surface)
            looper.update()

            cls.iterations += 1
            if rect1.is_greater_than(rect2):
                rect1.swap(rect2)
                merged_array.append([rect2, rect1])
            else:
                merged_array.append([rect1, rect2])

            cls.update(surface)
            looper.update()

            rect1.color = rect1.OG_COLOR
            rect2.color = rect2.OG_COLOR

        while len(merged_array) > 1:
            merged_array = cls.merge_sort_do_comparison(surface, looper, merged_array)
        cls.update(surface)
        looper.update()

    @classmethod
    def print_stats(cls):
        print(f"----  sorting complete ----\n"
              f"total iterations: {cls.iterations}\n"
              f"time elapsed: {(time.perf_counter() - cls.timer):.2f}s\n"
              f"status: {'Sorting Successful' if Rect.is_sorted() else 'Sorting Failed'}\n"
              f"----------------------------")

    def draw(self, screen):
        pygame.draw.rect(
            surface=screen,
            color=self.color,
            rect=self.rect_shape,
        )

    @classmethod
    def set_up(cls):
        cls.all_rects = []
        cls.iterations = 0
        randomized_list = list(range(NUM_RECTS))
        random.shuffle(randomized_list)
        for pos_index, height_index in enumerate(randomized_list):
            cls.all_rects.append(Rect(pos_index, height_index))

    @classmethod
    def draw_all(cls, screen):
        for rect in cls.all_rects:
            rect.draw(screen)

    @classmethod
    def update(cls, screen):
        cls.draw_all(screen)
        #  time.sleep(0.001)

class Main:
    def __init__(self):
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.Clock()
        self.running = True
        self.BG_COLOR = "black"
        self.FPS = None

    def user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        #  self.clock.tick(self.FPS)
        pygame.display.flip()
        self.surface.fill(self.BG_COLOR)
        self.user_input()

    def run(self):
        names = ( "Quick Sort", "Insertion Sort", "Selection Sort", "Merge Sort","Bubble Sort")
        for i, sorter in enumerate((Rect.quick_sort, Rect.insert_sort, Rect.selection_sort, Rect.merge_sort, Rect.bubble_sort)):
            print(names[i])
            Rect.set_up()
            print("Drawing...")
            Rect.draw_all(self.surface)
            self.update()
            print("Sorting in 3...")
            time.sleep(1)
            print("Sorting in 2...")
            time.sleep(1)
            print("Sorting in 1...")
            time.sleep(1)
            Rect.timer = time.perf_counter()
            sorter(self.surface, main)
            print(names[i])
            Rect.print_stats()
            time.sleep(3)
        print("done")
        while self.running:
            Rect.draw_all(self.surface)
            self.update()


if __name__ == "__main__":
    print("Starting...")
    main = Main()
    print("Running...")
    main.run()
