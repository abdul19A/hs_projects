from Chess.pieces import *
from Chess.events import events, screen
from Chess.bot import bot

class Board:
    # location index
    # 0  1  2  3  4  5  6  7
    # 8  9  10 11 12 13 14 15
    # 16 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30 31
    # 32 33 34 35 36 37 38 39
    # 40 41 42 43 44 45 46 47
    # 48 49 50 51 52 53 54 55
    # 56 57 58 59 60 61 62 63
    column1 = tuple(range(0, 8))
    column2 = tuple(range(8, 16))
    column3 = tuple(range(16, 24))
    column4 = tuple(range(24, 32))
    column5 = tuple(range(32, 40))
    column6 = tuple(range(40, 48))
    column7 = tuple(range(48, 56))
    column8 = tuple(range(56, 64))

    red_glow_size = grid_size + 10
    red_glow_image = Image.open("red_glow.png")
    red_glow_image = red_glow_image.resize((red_glow_size, red_glow_size))
    check_circle = pygame.image.frombytes(red_glow_image.tobytes(), (red_glow_size, red_glow_size), "RGBA")

    def __init__(self, center_pos):
        self.center_pos = center_pos
        self.locations = []
        self.all_pieces = [None for _ in range(64)]
        self.rects = []
        self.rect_colors = []
        self.turn = "w"
        # find top left point, which is 4 grid sizes from the center
        self.top_left: list = [center_pos[0] - grid_size * 4, center_pos[1] - grid_size * 4]
        self.bottom_left: list = [center_pos[0] - grid_size * 4, center_pos[1] + grid_size * 4]
        self.create_board()

        self.original_rect_colors: list = self.rect_colors.copy()
        self.selected_index: int = -1
        self.previously_selected_index: int = -1
        self.moved_from_area = -1
        self.moved_to_area = -1
        self.checkmated: str = ""
        self.points: dict = {
            "w": 0,
            'b': 0
        }
        self.forward_color: str = "w"  # the color of the piece that go up in their moves

    def create_piece_layer(self, color, column):
        Rook(self, column[0], color, size=piece_size)
        Knight(self, column[1], color, size=piece_size)
        Bishop(self, column[2], color, size=piece_size)
        Queen(self, column[3], color, size=piece_size)
        King(self, column[4], color, size=piece_size)
        Bishop(self, column[5], color, size=piece_size)
        Knight(self, column[6], color, size=piece_size)
        Rook(self, column[7], color, size=piece_size)

    def create_pawn_layer(self, color, column):
        for i in range(8):
            Pawn(self, column[i], color, size=piece_size)

    def create_original_preset(self):
        # creates the original preset
        down_color = self.forward_color
        if down_color == "w":
            up_color = "b"
        else:
            up_color = "w"

        self.create_piece_layer(up_color, self.column1)
        self.create_pawn_layer(up_color, self.column2)

        # Queen(self, 26, "b")
        # Queen(self, 29, "b")

        self.create_pawn_layer(down_color, self.column7)
        self.create_piece_layer(down_color, self.column8)

    def create_promotion_tester(self):
        King(self, self.column3[4], "b", size=piece_size)
        King(self, self.column5[4], "w", size=piece_size)
        Bishop(self, self.column1[1], "b", size=piece_size)
        self.create_pawn_layer("b", self.column7)
        self.create_pawn_layer("w", self.column2)
        Queen(self, self.column8[7], "w", size=piece_size)

    def create_checkmate_tester(self):
        self.create_original_preset()
        Queen(self, self.column4[2], "b", size=piece_size)
        Queen(self, self.column4[5], "b", size=piece_size)

    def flip_board(self):
        self.all_pieces = self.all_pieces[::-1]
        if self.forward_color == "b":
            self.forward_color = "w"
        else:
            self.forward_color = "b"

    def reset_selected(self):
        self.selected_index = -1
        self.previously_selected_index = -1
        self.rect_colors = self.original_rect_colors.copy()

    def create_board(self):
        color = light_color
        for y in range(8):
            # multiplies by the size and adjusts to board location
            y = y * grid_size + self.top_left[1]
            # switch after each iter of x
            if color == light_color:
                color = dark_color
            else:
                color = light_color
            for x in range(8):
                # switch after each iter of x
                if color == light_color:
                    color = dark_color
                else:
                    color = light_color
                # multiplies by the size and adjusts to board location
                x = x * grid_size + self.top_left[0]
                # gets the mid x and mid y
                piece_x = x + x_offset
                piece_y = y + y_offset
                # adds to corresponding list
                self.rects.append(pygame.Rect(x, y, grid_size, grid_size))
                self.locations.append((piece_x, piece_y))
                self.rect_colors.append(color)

    def piece_set_pos(self, piece, pos_index):
        self.all_pieces[pos_index] = piece
        piece.graphic_position = self.locations[pos_index]

    def highlight_selected_rect(self):
        # sets the color of the selected index to the highlight color
        current_color = self.rect_colors[self.selected_index]
        if current_color == light_color:
            self.rect_colors[self.selected_index] = light_highlight_color
        elif current_color == dark_color:
            self.rect_colors[self.selected_index] = dark_highlight_color

        # resets color of the previous rect
        if self.previously_selected_index >= 0:
            self.rect_colors[self.previously_selected_index] = self.original_rect_colors[self.previously_selected_index]
            self.reset_selected()

    def highlight_moved_rect(self):
        if self.moved_to_area == -1 or self.moved_from_area == -1:
            return
        # reset
        for i, color in enumerate(self.rect_colors):
            if color == light_moved_color:
                self.rect_colors[i] = light_color
            elif color == dark_moved_color:
                self.rect_colors[i] = dark_color
        # do it
        col1 = self.rect_colors[self.moved_to_area]
        col2 = self.rect_colors[self.moved_from_area]
        if col1 == light_color:
            self.rect_colors[self.moved_to_area] = light_moved_color
        elif col1 == dark_color:
            self.rect_colors[self.moved_to_area] = dark_moved_color

        if col2 == light_color:
            self.rect_colors[self.moved_from_area] = light_moved_color
        elif col2 == dark_color:
            self.rect_colors[self.moved_from_area] = dark_moved_color

    def update_selected_positions(self):
        if bot_enabled and bot.color == self.turn:
            bot.play_move(self)
            #  print("played ", self.previously_selected_index, " to ", self.selected_index)
        else:
            new_index = events.get_selected_index(self)

            if new_index == self.selected_index:
                self.reset_selected()
                # resets board colors

            elif new_index is not None:
                self.previously_selected_index = self.selected_index
                self.selected_index = events.get_selected_index(self)

    def update_graphic_positions(self):
        # after the self.all_pieces list is changed, graphic positions are reset to move pieces to an available position
        for piece_index, piece in enumerate(self.all_pieces):
            if piece is not None:  # checks if the square has a piece
                piece.graphic_position = self.locations[piece_index]

    def update_piece_index(self):
        if self.previously_selected_index >= 0 and self.selected_index >= 0:
            moving_piece = self.all_pieces[self.previously_selected_index]
            dying_piece = self.all_pieces[self.selected_index]
            # checks if there is a moving piece, and its the colors turn and has an available move respectively
            if moving_piece is None or moving_piece.color != self.turn:
                return
            # gets
            moving_piece.get_available_moves(self.previously_selected_index)
            if len(moving_piece.available_moves) < 1:
                return

            if self.selected_index not in moving_piece.available_moves:
                return
            moving_piece.times_moved += 1
            # get the types
            isPawn = isinstance(moving_piece, Pawn)
            isKing = isinstance(moving_piece, King)
            # promotion
            if isPawn and self.selected_index in moving_piece.promotion_column:
                temp_pawn = moving_piece
                moving_piece = self.get_promotion_piece(self.previously_selected_index, self.selected_index)
                if moving_piece is None:
                    return None
                else:
                    self.points[self.turn] += moving_piece.point_value - Piece.point_values["pawn"]
                    temp_pawn.die()
                    if dying_piece is not None:
                        self.points[self.turn] += dying_piece.point_value
                        dying_piece.die()
                    self.all_pieces[self.selected_index] = moving_piece

            # en passant
            elif isPawn and self.selected_index == moving_piece.en_passant_index:
                dying_piece = self.all_pieces[moving_piece.en_passant_dying_piece_index]
                self.all_pieces[self.selected_index] = moving_piece
                self.all_pieces[self.previously_selected_index] = None
                dying_piece.die()
                self.points[self.turn] += dying_piece.point_value
            # castling
            elif isKing and self.selected_index in moving_piece.castle_indices:
                self.all_pieces[self.selected_index] = moving_piece
                self.all_pieces[self.previously_selected_index] = None
                castle_index = moving_piece.castle_indices.index(
                    self.selected_index)  # this is so stupid oml using an index to find an index
                self.all_pieces[moving_piece.rook_next_indices[castle_index]] = self.all_pieces[
                    moving_piece.castle_rook_indices[castle_index]]
                self.all_pieces[moving_piece.castle_rook_indices[castle_index]] = None
            # empty spot
            elif dying_piece is None:
                self.all_pieces[self.selected_index] = self.all_pieces[self.previously_selected_index]
                self.all_pieces[self.previously_selected_index] = None
            # checks if the selected piece is opposite color

            # taking piece
            elif moving_piece.color != dying_piece.color:
                self.all_pieces[self.selected_index] = self.all_pieces[self.previously_selected_index]
                self.all_pieces[self.previously_selected_index] = None
                self.points[self.turn] += dying_piece.point_value
                dying_piece.die()
            else:
                raise ValueError("Illegal Move")
            for piece in self.all_pieces:
                if piece is moving_piece:
                    moving_piece.turns_since_last_move = 0
                elif piece is not None:
                    piece.turns_since_last_move += 1

            # color switch
            self.turn = "b" if self.turn == "w" else "w"
            if can_flip_board:
                self.flip_board()
        self.moved_from_area = self.previously_selected_index
        self.moved_to_area = self.selected_index
        self.update_graphic_positions()

    def check_available_moves(self, turn=None):
        turn = self.turn if turn is None else turn
        for piece_index, piece in enumerate(self.all_pieces):
            if piece is not None and turn == piece.color:
                piece.get_available_moves(piece_index)
                if piece.available_moves:  # checks if there is available moves
                    return True
        return False

    def update_winner_status(self):
        if self.check_available_moves():
            return
        self.checkmated = "stalemate"
        for king in King.all_kings:
            if king.color == self.turn and king.is_checked:
                self.checkmated = self.turn

    def get_targeted_king(self):
        color = self.turn
        for piece_index, piece in enumerate(self.all_pieces):
            if piece is not None and piece.color != color:
                targeted_indices = piece.get_available_moves(piece_index)
                for targeted_index in targeted_indices:
                    targeted_piece = self.all_pieces[targeted_index]
                    if targeted_piece is not None and targeted_piece.type == "king" and targeted_piece.color == color:
                        return targeted_piece
        return None

    def get_promotion_piece(self, pawn_index, next_index):
        pawn = self.all_pieces[pawn_index]
        if bot_enabled and self.turn == bot.color:
            return bot.get_promoted_piece(
                board=self,
                pawn=pawn,
                next_index=next_index
            )

        promo_pieces = ["queen", "knight", "rook", "bishop"]
        if next_index < 8:
            promo_range = tuple(range(next_index, 32, 8))
        else:
            promo_range = tuple(range(next_index, 32, -8))

        events.mouse_is_down = False
        while screen.open:
            for piece_num, rect_index in enumerate(promo_range):
                pygame.draw.rect(surface=screen.window,
                                 color=promote_square_color,
                                 rect=self.rects[rect_index])
                image = Piece.images_dict[pawn.color + "_" + promo_pieces[piece_num]]
                image = image.resize(pawn.size)
                pygame_image = pygame.image.frombytes(image.tobytes(), pawn.size, "RGBA")
                screen.window.blit(pygame_image, self.locations[rect_index])
            chosen_index = events.get_selected_index(self)
            if chosen_index in promo_range:
                type_index = promo_range.index(chosen_index)
                if type_index == 0:  # queen
                    return Queen(self, next_index, pawn.color, pawn.size[0])
                elif type_index == 1:  # knight
                    return Knight(self, next_index, pawn.color, pawn.size[0])
                elif type_index == 2:  # Rook
                    return Rook(self, next_index, pawn.color, pawn.size[0])
                elif type_index == 3:  # Bishop
                    return Bishop(self, next_index, pawn.color, pawn.size[0])

            elif chosen_index is not None:
                self.selected_index = -1
                return None

            screen.update_frames()
            events.update()

    def update_checks(self):
        King.reset_checks()
        king = self.get_targeted_king()
        if king is not None:
            king.is_checked = True

    def show_available_moves(self, win):
        if bot_enabled and self.turn == bot.color:
            return
        if self.selected_index >= 0:
            piece = self.all_pieces[self.selected_index]
            if piece is not None:
                available_moves_indices = piece.get_available_moves(self.selected_index)
                for location in available_moves_indices:
                    center_point = self.locations[location]
                    center_point = [center_point[0] + grid_size // 2 - x_offset,
                                    center_point[1] + grid_size // 2 - y_offset]
                    took_piece = self.all_pieces[location]
                    en_passant = (piece is not None and piece.type == "pawn" and location == piece.en_passant_index)
                    if took_piece is not None or en_passant:
                        pygame.draw.circle(
                            surface=win,
                            color=take_circ_color,
                            center=center_point,
                            radius=take_circ_radius,
                            width=0)
                    else:
                        pygame.draw.circle(
                            surface=win,
                            color=move_circ_color,
                            center=center_point,
                            radius=move_circ_radius,
                            width=0)

    def print(self):
        print_str = ""
        i = 0
        for piece in self.all_pieces:
            i += 1
            if piece is not None:
                print_str += piece.type[0] if piece.type != "knight" else "n"
            else:
                print_str += "0"
            if i % 8 == 0:
                print_str += "\n"

        print(print_str)

    def update(self, win):
        self.update_selected_positions()
        if self.selected_index >= 0:
            self.show_available_moves(win)
            self.update_piece_index()
            self.highlight_selected_rect()
            self.highlight_moved_rect()
            self.update_checks()
            self.update_winner_status()
        events.top_text_display(self)
        events.points_display(self)

        screen.update_frames()

    def draw(self, win):
        for rect_index, chess_rect in enumerate(self.rects):
            pygame.draw.rect(surface=win,
                             color=self.rect_colors[rect_index],
                             rect=chess_rect)


if __name__ == "__main__":
    import main
    main.main()
