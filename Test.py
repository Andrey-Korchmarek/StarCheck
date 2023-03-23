from GameBoard import *
from ursina import *

if __name__ == '__main__':
    app = Ursina()
    test = Piece((2, 2, 2), 0)
    a = Unit(test)
    window.fullscreen = True

    EditorCamera()
    app.run()