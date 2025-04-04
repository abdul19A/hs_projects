import pygame

screen_x = 500
screen_y = 700
screen_mid = (screen_x//2, screen_y//2)
screen_color = "midnightBlue"
screen_caption = "Chess"

dark_color = pygame.color.Color([122, 152, 225])   # blue color
light_color = pygame.color.Color([248, 243, 239])  # white color

dark_highlight_color = pygame.color.Color([172, 159, 60])  # dark yellow color
light_highlight_color = pygame.color.Color([255, 184, 28])  # light yellow color

dark_moved_color = pygame.color.Color([122, 112, 225])  # dark yellow color
light_moved_color = pygame.color.Color([248, 203, 249])  # light yellow color

player_turn = "w"

move_circ_color = pygame.color.Color(200, 150, 150)  # gray color
move_circ_radius = 8

take_circ_color = pygame.color.Color(120, 120, 100)
take_circ_radius = 10

grid_size = 55
piece_size = grid_size - 10
promote_square_color = pygame.color.Color(52, 82, 115)

can_flip_board = False
bot_enabled = True

x_offset = 4
y_offset = -3

fps = 60
