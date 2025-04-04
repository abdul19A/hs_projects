from Chess.vars import *
from Chess.events import events, screen
from Chess.gameBoard import Board
from Chess.pieces import Piece

def main():
    board = Board(center_pos=screen_mid)
    board.create_promotion_tester()

    while screen.open:
        screen.create_background()
        events.update()

        board.draw(screen.window)
        Piece.draw_all(screen.window)

        board.update(screen.window)
        screen.update_frames()


if __name__ == "__main__":
    main()
