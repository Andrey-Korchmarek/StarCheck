from ursina.raycast import raycast
from ursina import *
#from Сalculations import *
from GameBoard import *
from Unit import *

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Game(object):
    def __init__(self, boardsize, pieces = []):
        app = Ursina()
        board = GameBoard(boardsize)
        try:
            iterator = iter(pieces)
        except TypeError:
            print("The pieces is not iterable")
        else:
            next_element_exist = True
            while next_element_exist:
                try:
                    element_from_iterator = next(iterator)
                except StopIteration:
                    next_element_exist = False
                else:
                    if type(element_from_iterator) == Piece:
                        new_unit = Unit(element_from_iterator, board)
                        board.units[element_from_iterator.point] = new_unit
        window.fullscreen = True
        EditorCamera()
        app.run()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = Ursina()
    a = Piece((2, 2, 2), 1)
    b = Piece((-2, -2, -2), 1)
    board = GameBoard(3)
    window.fullscreen = True
    def input(key):
        if key == 'space':
            board.switch_cell_visibility()
        if key == 'w':
            board.switch_core_visibility()

    EditorCamera()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
