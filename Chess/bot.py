from Chess.vars import *
from Chess.pieces import *
import time
import random

def get_chess_notation(index):
    height_list = ["1", "2", "3", "4", "5", "6", "7", "8"]
    width_list =  ["a", "b", "c", "d", "e", "f", "g", "h",]
    return width_list[index%8] + height_list[(63-index)//8]

class bot:
    color = "w" if player_turn == "b" else "b"
    promotion_choice = None
    smartness = 0
    clock = None
    delay = 1

    @staticmethod
    def print_dict(board, dictionary):
        print("____________________________")
        for i in dictionary:
            piece = board.all_pieces[i]
            notated = [get_chess_notation(pos) for pos in dictionary[i]]
            print(f"{piece.type} at {get_chess_notation(i)}, ->", *notated, sep=", " )
        print("____________________________")

    @staticmethod
    def generate_piece_dict(board):
        piece_dict = {}
        promo_dict = {}
        for index, piece in enumerate(board.all_pieces):
            if piece is not None and piece.color == bot.color:
                available_moves = piece.get_available_moves(index)
                if available_moves:
                    piece_dict[index] = piece.get_available_moves(index)
                if piece.type == "pawn":
                    promotion_list = []
                    for move in piece.get_available_moves:
                        if move in piece.promotion_column:
                            promotion_list.append(move)
                    if promotion_list:
                        piece_dict[index] = promotion_list
        bot.print_dict(board, piece_dict)
        return piece_dict, promo_dict

    @staticmethod
    def play_move(board):
        if not bot.delayed():
            return

        piece_dict, promo_dict = bot.generate_piece_dict(board)

        # result
        if piece_dict:  # we check if it is empty so it does not keep "playing" during stalemate or checkmate
            chosen_to_index, chosen_from_index = bot.choose_move(board, piece_dict, promo_dict)
            board.previously_selected_index = chosen_from_index
            board.selected_index = chosen_to_index

    @staticmethod
    def get_promoted_piece(board, pawn, next_index):
        choice_index = bot.promotion_choice
        if choice_index == 0:
            return Queen(board, next_index, pawn.color, pawn.size[0])
        elif choice_index == 1:
            return Rook(board, next_index, pawn.color, pawn.size[0])
        elif choice_index == 2:
            return Bishop(board, next_index, pawn.color, pawn.size[0])
        else:
            return Knight(board, next_index, pawn.color, pawn.size[0])

    @staticmethod
    def promote(board, piece, next_move):
        if not isinstance(piece, Pawn):
            return None

    @staticmethod
    def delayed():
        if bot.delay == 0:
            return True

        if bot.clock is None:
            bot.clock = time.perf_counter()

        if time.perf_counter() - bot.clock < bot.delay:
            return False
        else:
            bot.clock = None
            return True

    @staticmethod
    def choose_move(board, every_move_dict, promo_dict):
        # return bot.choose_random(every_move_dict)
        max_point_value = 0
        chosen_move = None
        chosen_piece = None
        piece_list = board.all_pieces.copy()
        promotion_choice = None
        for piece_index in every_move_dict:
            for move_index in every_move_dict[piece_index]:
                if piece_index in promo_dict:
                    promo_dict
                # gets highest piece point value
                move_value = 0
                other_piece = piece_list[move_index]
                this_piece = piece_list[piece_index]

                move_value += bot.attack_piece(other_piece)
                move_value += bot.check_mate(board, piece_index, move_index)

                if move_value > max_point_value:
                    chosen_move = move_index
                    chosen_piece = piece_index
                    max_point_value = move_value
                    bot.promotion_choice = bot.promote()


        print(max_point_value, chosen_move, chosen_piece)
        if max_point_value != 0:
            return chosen_move, chosen_piece
        else:
            print("chose random move")
            return bot.choose_random(every_move_dict)


    @staticmethod
    def attack_piece(other_piece):
        if other_piece is None:
            return 0
        return other_piece.point_value

    @staticmethod
    def defend_piece(piece):
        if other_piece is None:
            return 0
        return other_piece

    @staticmethod
    def choose_random(every_move):
        random_piece = random.choice(list(every_move.keys()))
        random_move = random.choice(every_move[random_piece])
        return random_move, random_piece
    @staticmethod
    def promotion(board, piece, move_index):
        if isinstance(piece, Pawn) and move_index in piece.promotion_column:
            pass

    @staticmethod
    def check_mate(board, piece_index, move_index):
        # alter the all pieces list and then make it normal again
        piece = board.all_pieces[piece_index]
        if piece is None:
            return
        all_pieces_copy = board.all_pieces.copy()
        board.all_pieces[move_index] = piece
        board.all_pieces[piece_index] = None
        board.turn = "b" if board.turn == "w" else "w"

        for goto_piece_index, other_piece in enumerate(board.all_pieces):
            if other_piece is not None and other_piece.color != bot.color:
                if other_piece.get_available_moves(goto_piece_index):
                    board.all_pieces = all_pieces_copy
                    board.turn = "b" if board.turn == "w" else "w"
                    return 0

        board.all_pieces = all_pieces_copy
        board.turn = "b" if board.turn == "w" else "w"
        return 100

    @staticmethod
    def choose_promo():
        if bot.smartness == 0:
            return random.randrange(0, 4)
            # return random.randrange(4)

if __name__ == "__main__":
    import main
    main.main()
