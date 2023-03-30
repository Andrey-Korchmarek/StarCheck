
from ursina import *
from Unit import Piece
from GameBoard import GameBoard

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = Ursina()
    a = Piece((2, 2, 2), 1, 1)
    b = Piece((-2, -2, -2), 1, 2)
    board = GameBoard(3, [a, b])
    window.fullscreen = True
    def input(key):
        if key == 'space':
            board.switch_cell_visibility()

    EditorCamera()
    app.run()
