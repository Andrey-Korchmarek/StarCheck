from Сalculations import *
from Unit import *
from ursina import Vec3, Entity, color
from ursina.sequence import *

class Cell(Entity):
    def __init__(self, pos):
        color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
        super().__init__(
            visible = False,
            model='models/Cell',
            color = color_calc[sum(pos) % 8],
            position=pos,
            )

class Nucleus(Entity):
    def __init__(self, pos, board):
        self.board = board
        super().__init__(
            visible = False,
            model = 'sphere',
            collision = True,
            collider = 'sphere',
            position = pos,
            )

    def on_double_click(self):
        #По двойному клику на пустую клетку выбранная фигура перемещается на эту клетку
        super().on_double_click()
        self.board.walk(end = self.position)

class GameBoard(object):
    def __init__(self, size):
        """Constructor"""
        self.center = Vec3(0, 0, 0)
        self.borders = generate_borders(size)
        self.coordinates = generate_coordinates(self.borders)
        self.cells = {coord: Cell(pos= coord) for coord in self.coordinates}
        self.cells[self.center].model = 'models/Solid'
        self.cells[self.center].color = color.black
        self.nuclei = {coord: Nucleus(coord, self) for coord in self.coordinates}
        self.nuclei[self.center].collision = True
        self.units = {coord: None for coord in self.coordinates}
        self.selected: Legalmove = None

    def select(self, unit):
        if None == self.selected.source:
            self.move(prev = unit)
        else:
            if unit.side == self.selected.source.side:
                self.move(prev = unit)
            else:
                self.move(new = unit)

    def move(self, prev = None, new = None):
        pass

    def walk(self, start = None, end = None):
        pass

    def attack(self, attacker = None, capture = None):
        pass

    def destroy(self, gunner = None, target = None):
        pass

    def switch_cell_visibility(self):
        if not len(self.cells):
            return
        new = not self.cells[self.center].visible
        for el in self.cells.values():
            el.visible = new

    def switch_core_visibility(self):
        if not len(self.nuclei):
            return
        new = not self.nuclei[self.center].visible
        for el in self.nuclei.values():
            el.visible = new

if __name__ == '__main__':
    print("This is not app!")