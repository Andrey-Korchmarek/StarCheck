
from Unit import Unit, Legalmove
from Сalculations import *
from ursina import Entity, Vec3, color, sequence


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
    def __init__(self, pos):
        super().__init__(
            ignore_input = True,
            visible = False,
            model = 'sphere',
            color = color.gray,
            collision = True,
            collider = 'sphere',
            position = pos,
            )

class GameBoard(object):
    def __init__(self, size):
        """Constructor"""
        self.center = Vec3(0, 0, 0)
        self.borders = generate_borders(size)
        self.coordinates = generate_coordinates(self.borders["limits"])
        self.cells = {coord: Cell(coord) for coord in self.coordinates}
        self.cells[self.center].model = 'models/Solid'
        self.cells[self.center].color = color.black
        self.nuclei = {coord: Nucleus(coord) for coord in self.coordinates}
        for el in self.nuclei.values():
            el.on_double_click = sequence.Func(self.walk, end = el)
            if all([x >= 0.0 for x in [sum(norm * el.position) + l for norm, l in self.borders["plus"]]]):
                el.color = color.peach
            if all([x >= 0.0 for x in [sum(norm * el.position) + l for norm, l in self.borders["minus"]]]):
                el.color = color.cyan
        self.nuclei[self.center].color = color.clear
        self.nuclei[self.center].collision = True
        self.nuclei[self.center].on_double_click = todo_nothing
        self.units = {coord: None for coord in self.coordinates}
        """
        self.add_units(pieces)
        for el in self.units.values():
            if None != el:
                el.on_click = sequence.Func(self.select, el)
                attack = sequence.Func(self.attack, capture = el)
                destroy = sequence.Func(self.destroy, target = el)
                el.on_double_click = attack if 0 == held_keys['left control'] else destroy
        """
        self.selected: Legalmove = Legalmove(None)
        self.catching_units = dict()
        self.catching_units[True] = []
        self.catching_units[False] = []

    def add_units(self, pieces):
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
                    from Unit import Piece, Unit
                    if type(element_from_iterator) == Piece:
                        self.units[element_from_iterator.point] = Unit(element_from_iterator, self)

    def what_is_there(self, point: Vec3):
        from Unit import Unit, WHITE, BLACK
        if self.center == point:
            return None
        elif any([x < 0.0 for x in [sum(norm * point) + l for norm, l in self.borders["limits"]]]):
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

    def select(self, unit):
        if None == self.selected.source and None != unit:
            self.selected = unit.legal_move_generator()
            self.switch_select_visibility(True)
        elif None == self.selected.source and None == unit:
            pass
        elif None != self.selected.source and None == unit:
            self.switch_select_visibility(False)
            self.selected.motion.clear()
            self.selected.capture.clear()
            self.selected.kill.clear()
            self.selected = Legalmove(None)
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
        elif None == start and None != end and None != self.selected.source:
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
            self.nuclei[point].ignore_input = not new
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