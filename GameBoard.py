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
        self.board.walk(end = self)

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
        self.catching_units = dict(WHITE = [], BLACK = [])

    def what_is_there(self, point: Vec3):
        if any([x < 0.0 for x in [sum(norm * point) + d for norm, d in self.borders]]):
            return None
        elif None == self.units[point]:
            return 0
        elif Unit != type(self.units[point]):
            return -1
        else:
            if WHITE == self.units[point].side:
                return 1
            elif BLACK == self.units[point].side:
                return 2
            else:
                return -1

    def select(self, unit: Unit):
        if None == self.selected and None != unit:
            self.selected = unit.legal_move_generator()
            self.switch_select_visibility(True)
        elif None == self.selected and None == unit:
            pass
        elif None != self.selected and None == unit:
            self.switch_select_visibility(False)
            self.selected = None
        else:
            if unit.side == self.selected.source.side:
                self.switch_select_visibility(False)
                self.selected = unit.legal_move_generator()
                self.switch_select_visibility(True)
            else:
                pass

    def walk(self, start: Unit = None, end: Nucleus = None):
        if None != start and None != end:
            self.units[end.position] = start
            self.units[start.position] = None
            start.set_position(end.position)
            self.select(None)
        elif None != start and None == end:
            self.select(start)
        elif None == start and None != end and None != self.selected:
            self.walk(self.selected.source, end)
        else:
            pass

    def attack(self, attacker: Unit = None, capture: Unit = None):
        if None != attacker and None != capture and attacker.side != capture.side:
            self.catching_units[attacker.side].append(capture.form)
            self.units[capture.position] = None
            self.units[capture.position] = attacker
            self.units[attacker.position] = None
            attacker.set_position(capture.position)
            capture.disable()
            self.select(None)
        elif None == attacker and None != capture and None != self.selected:
            self.attack(attacker = self.selected.source, capture = capture)
        else:
            pass

    def destroy(self, gunner: Unit = None, target: Unit = None):
        if None != gunner and None != target and gunner.side != target.side:
            self.units[target.position] = None
            target.disable()
            self.select(None)
        elif None != gunner and None != target and None != self.selected:
            self.destroy(gunner = self.selected.source, target = target)
        else:
            pass

    def switch_select_visibility(self, new: bool = False):
        for point in self.selected.motion:
            self.nuclei[point].visible = new
        for point in self.selected.capture:
            self.units[point].color = color.yellow if new else color.white
        for point in self.selected.kill:
            prevcolor = self.units[point].color
            self.units[point].color = (color.red if color.white == prevcolor else color.orange) if new else color.white

    def switch_cell_visibility(self):
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