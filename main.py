from ursina.raycast import raycast
from ursina import *
from Сalculations import *

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    board = GameBoard()
    app = Ursina()
    window.fullscreen = True
    ooo = Entity(model='sphere', color=color.cyan, scale=0.2)
    dots = tuple(set().union(board.vertexes, board.edges, board.faces))
    points = Entity(model=Mesh(vertices=dots, mode='point', thickness=.05), color=color.light_gray)
    coords = board.generate_cell_pool(5) - {board.center}
    cells = [Entity(model='sphere', color=color.light_gray, scale=board.r6, collision=True, collider='sphere', position=pos) for pos in coords]
    hit_info = [raycast(board.center, dir) for dir in dots]
    for hit in hit_info:
        if hit.entity:
            hit.entity.color = color.red
    EditorCamera()
    app.run()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
