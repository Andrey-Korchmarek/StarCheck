from ursina.raycast import raycast
from ursina import *
#from Сalculations import *
from GameBoard import *

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    board = GameBoard(3)
    app = Ursina()
    window.fullscreen = True
    def input(key):
        if key == 'space':
            board.changing_visibility()
        if key == 'w':
            board.show_core()
    EditorCamera()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
