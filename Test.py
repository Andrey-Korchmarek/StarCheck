from GameBoard import *
from ursina import *
from Unit import *

if __name__ == '__main__':
    app = Ursina()
    test = Piece((2, 2, 2), 1)
    a = Unit(test)
    a.color = color.red
    window.fullscreen = True

    EditorCamera()
    app.run()