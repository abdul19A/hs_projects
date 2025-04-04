from Chess.vars import *
from PIL import Image
import pygame

def get_images_list(file_path):
    image = Image.open(file_path)

    # Calculate the height of each part
    part_width = 5
    part_height = 25
    delta_width = 300
    delta_height = 370
    parts = []
    for i in range(6):
        for j in range(2):
            box = (part_width + i * delta_width, part_height + j * delta_height,
                   part_width + (i + 1) * delta_width, part_height + (j + 1) * delta_height)
            part = image.crop(box)
            parts.append(part)
    return parts


get_images_list("chessPieces.png")


class Piece:
    list = []
    file_path = "chessPieces.png"
    images_list = get_images_list("chessPieces.png")
    images_dict = {
        "b_rook": images_list[0],
        "w_rook": images_list[1],
        "b_bishop": images_list[2],
        "w_bishop": images_list[3],
        "b_queen": images_list[4],
        "w_queen": images_list[5],
        "b_king": images_list[6],
        "w_king": images_list[7],
        "b_knight": images_list[8],
        "w_knight": images_list[9],
        "b_pawn": images_list[10],
        "w_pawn": images_list[11],
    }
    point_values = {
        "pawn": 1,
        "knight": 3,
        "bishop": 3,
        "rook": 5,
        "queen": 9,
        "king": float("inf")
    }

    def __init__(self, board, index_position: int, size: int, color: str, piece_type: str):
        """"Enter color as letter"""
        self.graphic_position: tuple = ()

        self.size: tuple = (size, round(size * 4 / 3))
        self.board = board

        self.board.piece_set_pos(self, index_position)
        self.available_moves = []
        self.times_moved = 0

        self.color = color.lower()
        self.type = piece_type.lower()
        self.point_value = Piece.point_values[self.type]
        self.image = Piece.images_dict[color + "_" + self.type]
        self.image = self.image.resize(self.size)

        self.pygame_image = pygame.image.fromstring(self.image.tobytes(), self.size, "RGBA")
        Piece.list.append(self)
        self.turns_since_last_move = 0

    def die(self):
        Piece.list.remove(self)
        if self in self.board.all_pieces:
            self.board.all_pieces[self.board.all_pieces.index(self)] = None

    def draw(self, window):
        window.blit(self.pygame_image, self.graphic_position)

    def is_facing_none(self, index):
        return 0 <= index < 64 and self.board.all_pieces[index] is None

    def is_opposite_piece(self, index):
        if 0 <= index < 64 and self.board.all_pieces[index] is not None:
            return self.board.all_pieces[index].color != self.color
        return None

    def get_moves_preventing_check(self, start_index, end_index_list):
        if self.color == self.board.turn:
            result_list = []
            for end_index in end_index_list:
                temp_piece = self.board.all_pieces[end_index]
                # alter list
                self.board.all_pieces[end_index] = self.board.all_pieces[start_index]
                self.board.all_pieces[start_index] = None

                target_king = self.board.get_targeted_king()

                # return to previous
                self.board.all_pieces[start_index] = self.board.all_pieces[end_index]
                self.board.all_pieces[end_index] = temp_piece
                if target_king is None:
                    result_list.append(end_index)
                elif target_king.color == self.color:
                    pass
                else:
                    result_list.append(end_index)
            return result_list
        else:
            return end_index_list

    @staticmethod
    def draw_all(window):
        for piece in Piece.list:
            piece.draw(window)

class Rook(Piece):
    def __init__(self, board, index_position, color, size=piece_size):
        super().__init__(board, index_position, size, color, "rook")

    def get_available_moves(self, piece_index) -> list:
        available_indices = []
        x_pos = piece_index % 8
        y_pos = piece_index // 8
        all_moves = (
            (0, -1),  # north
            (1, 0),  # east
            (0, 1),  # south
            (-1, 0),  # west
        )

        for move in all_moves:
            for i in range(1, 8):  # max value
                cur_x_pos = x_pos + move[0] * i
                cur_y_pos = y_pos + move[1] * i
                if 0 <= cur_x_pos < 8 and 0 <= cur_y_pos < 8:
                    index = cur_x_pos + cur_y_pos * 8
                    if self.is_facing_none(index):
                        available_indices.append(index)
                    elif self.is_opposite_piece(index):
                        available_indices.append(index)
                        break
                    else:
                        break
        available_moves = self.get_moves_preventing_check(piece_index, available_indices)
        self.available_moves = available_moves
        return available_moves


class Bishop(Piece):
    def __init__(self, board, index_position, color, size=piece_size):
        super().__init__(board, index_position, size, color, "bishop")

    def get_available_moves(self, piece_index) -> list:
        available_indices = []
        x_pos = piece_index % 8
        y_pos = piece_index // 8
        all_moves = (
            (-1, -1),  # north west
            (1, -1),  # north east
            (-1, 1),  # south east
            (1, 1),  # south west
        )

        for move in all_moves:
            for i in range(1, 8):  # max value
                cur_x_pos = x_pos + move[0] * i
                cur_y_pos = y_pos + move[1] * i
                if 0 <= cur_x_pos < 8 and 0 <= cur_y_pos < 8:
                    index = cur_x_pos + cur_y_pos * 8
                    if self.is_facing_none(index):
                        available_indices.append(index)
                    elif self.is_opposite_piece(index):
                        available_indices.append(index)
                        break
                    else:
                        break
        available_moves = self.get_moves_preventing_check(piece_index, available_indices)
        self.available_moves = available_moves
        return available_moves


class Queen(Piece):
    def __init__(self, board, index_position, color, size=piece_size):
        super().__init__(board, index_position, size, color, "queen")

    def get_available_moves(self, piece_index) -> list:
        available_indices = []
        x_pos = piece_index % 8
        y_pos = piece_index // 8
        all_moves = (
            (-1, -1),  # north west
            (1, -1),  # north east
            (-1, 1),  # south east
            (1, 1),  # south west
            (0, -1),  # north
            (1, 0),  # east
            (0, 1),  # south
            (-1, 0),  # west
        )

        for move in all_moves:
            for i in range(1, 8):  # max value
                cur_x_pos = x_pos + move[0] * i
                cur_y_pos = y_pos + move[1] * i
                if 0 <= cur_x_pos < 8 and 0 <= cur_y_pos < 8:
                    index = cur_x_pos + cur_y_pos * 8
                    if self.is_facing_none(index):
                        available_indices.append(index)
                    elif self.is_opposite_piece(index):
                        available_indices.append(index)
                        break
                    else:
                        break

        available_moves = self.get_moves_preventing_check(piece_index, available_indices)
        self.available_moves = available_moves
        return available_moves


class King(Piece):
    all_kings = []

    def __init__(self, board, index_position, color, size=piece_size):
        super().__init__(board, index_position, size, color, "king")
        self.castle_indices = []
        self.castle_rook_indices = []
        self.rook_next_indices = []
        self.is_checked = False
        King.all_kings.append(self)

    @staticmethod
    def reset_checks():
        for king in King.all_kings:
            king.is_checked = False

    def get_available_moves(self, piece_index) -> list:
        available_indices = []
        x_pos = piece_index % 8
        y_pos = piece_index // 8
        all_moves = [(-1, 0), (1, 0), (1, 1), (-1, 1), (0, 1), (0, -1), (-1, -1), (1, -1)]
        for move in all_moves:
            if 8 > x_pos + move[0] >= 0 and 8 > y_pos + move[1] >= 0:
                new_index = piece_index + move[0] + move[1] * 8
                if self.is_facing_none(new_index) or self.is_opposite_piece(new_index):
                    available_indices.append(new_index)

        # castling
        if self.color == self.board.forward_color:
            rook1_index = 63
            rook2_index = 56
        else:
            rook1_index = 0
            rook2_index = 7
        # reset
        self.castle_indices = []
        self.castle_rook_indices = []
        self.rook_next_indices = []
        available_moves = self.get_moves_preventing_check(piece_index, available_indices)
        for rook_index in rook1_index, rook2_index:
            if self.can_castle(piece_index, rook_index):
                if rook_index > piece_index:
                    if (piece_index + 1) in available_moves:
                        available_indices.append(piece_index + 2)
                        self.castle_indices.append(piece_index + 2)
                        self.rook_next_indices.append(piece_index + 1)
                else:
                    if (piece_index - 1) in available_moves:
                        available_indices.append(piece_index - 2)
                        self.castle_indices.append(piece_index - 2)
                        self.rook_next_indices.append(piece_index - 1)
                self.castle_rook_indices.append(rook_index)

        available_moves = self.get_moves_preventing_check(piece_index, available_indices)
        self.available_moves = available_moves
        return available_moves

    def can_castle(self, king_index, rook_index):
        piece = self.board.all_pieces[rook_index]
        if piece is not None and piece.type == "rook" and piece.color == self.color:
            if rook_index > king_index:
                i = 1
            else:
                i = -1

            for index_between in range(king_index + i, rook_index, i):
                if self.board.all_pieces[index_between] is not None:
                    return False
            return (self.times_moved == 0 and
                    piece.times_moved == 0 and
                    not self.is_checked)
        return False

    def draw(self, window):
        circle_position = [self.graphic_position[0] - 10, self.graphic_position[1]]
        if self.is_checked:
            window.blit(self.board.check_circle, circle_position)
        window.blit(self.pygame_image, self.graphic_position)


class Knight(Piece):
    def __init__(self, board, index_position, color, size=piece_size):
        super().__init__(board, index_position, size, color, "knight")

    def get_available_moves(self, piece_index) -> list:
        available_indices = []
        x_pos = piece_index % 8
        y_pos = piece_index // 8
        all_moves = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-2, -1), (-1, -2)]
        for move in all_moves:
            if 8 > x_pos + move[0] >= 0 and 8 > y_pos + move[1] >= 0:
                new_index = piece_index + move[0] + move[1] * 8
                if self.is_facing_none(new_index) or self.is_opposite_piece(new_index):
                    available_indices.append(new_index)

        available_moves = self.get_moves_preventing_check(piece_index, available_indices)
        self.available_moves = available_moves
        return available_moves


class Pawn(Piece):
    def __init__(self, board, index_position, color, size=piece_size):
        super().__init__(board, index_position, size, color, "pawn")
        self.en_passant_index = None
        self.en_passant_dying_piece_index = None
        if can_flip_board or self.color == self.board.forward_color:
            self.promotion_column = self.board.column1
        else:
            self.promotion_column = self.board.column8

    def get_available_moves(self, piece_index) -> list:
        available_indices = []
        if piece_index in self.promotion_column:
            return []
        # forward
        if self.color == self.board.forward_color:
            forward = piece_index - 8
            forward2 = piece_index - 16
            takes_left = piece_index - 9
            takes_right = piece_index - 7
        else:
            forward = piece_index + 8
            forward2 = piece_index + 16
            takes_left = piece_index + 9
            takes_right = piece_index + 7
        # check max rank pawn:

        # single move
        if self.is_facing_none(forward):
            available_indices.append(forward)

            # double move
            if self.times_moved == 0 and self.is_facing_none(forward2):
                available_indices.append(forward2)

        # takes

        for takes in takes_left, takes_right:
            is_one_col_away = abs(takes // 8 - piece_index // 8) == 1
            if self.is_opposite_piece(
                    takes) and is_one_col_away:  # checks if there is opposite then checks if the distance of columns does not exceed 1
                available_indices.append(takes)
        # conditions for En-Passant
        # add the index of en_passant to self.en_passant_index and available_indices and self.available_moves

        if (self.color == self.board.forward_color and piece_index // 8 == 3) or (
                self.color != self.board.forward_color and piece_index // 8 == 4):
            for other_index in piece_index - 1, piece_index + 1:
                other_piece = self.board.all_pieces[other_index]
                if (other_index // 8 == piece_index // 8 and
                        self.is_opposite_piece(other_index) and
                        other_piece.turns_since_last_move == 0 and
                        other_piece.type == "pawn" and
                        other_piece.times_moved == 1):

                    if self.color == self.board.forward_color:
                        self.en_passant_index = other_index - 8
                    else:
                        self.en_passant_index = other_index + 8

                    self.en_passant_dying_piece_index = other_index
                    available_indices.append(self.en_passant_index)

        available_moves = self.get_moves_preventing_check(piece_index, available_indices)
        self.available_moves = available_moves
        return available_moves
