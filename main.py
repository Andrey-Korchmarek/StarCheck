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
    board = GameBoard(5)
    app = Ursina()
    window.fullscreen = True
    def input(key):
        if key == 'space':
            board.switch_cell_visibility()
        if key == 'w':
            board.switch_core_visibility()
    vec = ((2, 0.5, 0.5), (2, -0.5, 0.5), (2, -0.5, -0.5), (2, 0.5, -0.5))
    hit_info = [raycast((0, 0, 0), v) for v in vec]
    for hit in hit_info:
        if len(hit.entities):
            for e in hit.entities:
                e.visible = True
                e.color = color.red
                print(e.position)
    EditorCamera()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
