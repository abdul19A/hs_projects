from Chess.vars import *
from Chess.pieces import *
import pygame

class screen:
    # initialize window
    window = pygame.display.set_mode((screen_x, screen_y))
    # create the name of the window (caption)
    pygame.display.set_caption(screen_caption)
    # initialize clock
    clock = pygame.time.Clock()
    open = True

    chess_squares_rects = []
    chess_squares_colors = []
    chess_pieces_images = []
    chess_pieces_locations = []
    

    @staticmethod
    def create_background():
        # wipes away last frame
        screen.window.fill(screen_color)

    @staticmethod
    def draw_board():
        ...
    @staticmethod
    def draw_pieces():
        ...
    @staticmethod
    def draw_promotion():
        ...
    @staticmethod
    def draw_text():
        ...
    @staticmethod
    def draw_all():
        ...
    @staticmethod
    def update_frames():
        # updates the screen
        pygame.display.flip()
        # waits between each frame to acheive (fps) fps
        screen.clock.tick(fps)


class events:
    # window atribute
    window_open: bool = True

    # all mouse attributes
    mouse_x: float = None
    mouse_y: float = None
    mouse_is_down: bool = False
    mouse_is_held: bool = False

    # all key atributtes
    key_last_pressed: str = None
    key_held: str = None
    key_pressed: str = None
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    @staticmethod
    def update():
        # updates mouse position
        events.mouse_x, events.mouse_y = pygame.mouse.get_pos()
        # resets mouse to False until it is set to true later on
        events.mouse_is_down = False
        # resets which key was pressed
        events.key_pressed = None
        # loops through each pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.window_open = False
                screen.open = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                events.mouse_is_down = True
                events.mouse_is_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                events.mouse_is_held = False
            if event.type == pygame.KEYDOWN:
                key_down = pygame.key.name(event.key)
                events.key_last_pressed = key_down
                events.key_held = key_down
            elif event.type == pygame.KEYUP:
                events.key_held = None
                events.key_pressed = pygame.key.name(event.key)

    @staticmethod
    def get_selected_index(board):
        for rect in board.rects:
            if events.mouse_is_down and rect.collidepoint(events.mouse_x, events.mouse_y):
                return board.rects.index(rect)
        return None

    @staticmethod
    def top_text_display(board):

        if board.checkmated == "w":
            text_surface = events.font.render(f"Black wins", True, "white")
        elif board.checkmated == "b":
            text_surface = events.font.render(f"White wins", True, "white")
        elif board.checkmated == "stalemate":
            text_surface = events.font.render(f"Stalemate", True, "white")
        elif board.turn == "w":
            text_surface = events.font.render(f"White to move", True, "white")
        elif board.turn == "b":
            text_surface = events.font.render(f"Black to move", True, "white")

        text_rect = text_surface.get_rect(center=(screen_x/2, 100))
        screen.window.blit(text_surface, text_rect)

    @staticmethod
    def points_display(board):
        black_points = board.points['b']
        white_points = board.points['w']

        if white_points > black_points:
            corner = [board.bottom_left[0] + 10, board.bottom_left[1] + 15]
            advantage = white_points - black_points
            text_surface = events.font.render(f"+{advantage}", True, "white")
            text_rect = text_surface.get_rect(center=corner)
            screen.window.blit(text_surface, text_rect)

        elif black_points > white_points:
            corner = [board.top_left[0] + 10, board.top_left[1] - 15] # padding is 10
            advantage = black_points - white_points
            text_surface = events.font.render(f"+{advantage}", True, "white")
            text_rect = text_surface.get_rect(center=corner)
            screen.window.blit(text_surface, text_rect)



def test():
    while events.window_open:
        screen.create_background()
        events.update()

        if events.mouse_is_down:
            print(events.mouse_x, events.mouse_y)

        pygame.display.flip()
        screen.update_frames()


if __name__ == "__main__":
    test()



