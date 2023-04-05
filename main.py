import colorsys

from ursina import *
from Unit import Piece
from GameBoard import GameBoard

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = Ursina()
    border = Entity(model="models/Solid", visible=False, scale=1, alpha=0.8)
    plus = Entity(model="models/Solid", color=color.red, position=Vec3(1, 1, 1) * border.scale * 4 / 3, scale=border.scale, alpha=0.5)
    a = [Piece(point, 18, 1) for point in [(-8, 0, 0), (-8, 0, 4), (-8, 4, 0), (-8, 0, -4), (-8, -4, 0)]]
    b = [Piece(point, 18, 2) for point in [(8, 0, 0), (8, 0, 4), (8, 4, 0), (8, 0, -4), (8, -4, 0)]]
    board = GameBoard(1)
    for el in board.nuclei.values():
        if all([x >= 0.0 for x in [sum(norm * el.position) + l for norm, l in board.borders["plus"]]]):
            el.color=color.gold
    window.fullscreen = True
    def input(key):
        if key == 'space':
            board.switch_cell_visibility()
        if key == 'x':
            board.switch_core_visibility()
        if key == 'z':
            border.visible = not border.visible
        if key == 'm':
            border.scale_x += 0.5
            border.scale_y += 0.5
            border.scale_z += 0.5
            print(border.scale)
            plus.scale = border.scale
            plus.position = border.scale * 4 / 3
        if key == 'n':
            border.scale_x -= 0.5
            border.scale_y -= 0.5
            border.scale_z -= 0.5
            plus.scale = border.scale
            plus.position = border.scale * 4 / 3

    EditorCamera()
    app.run()
