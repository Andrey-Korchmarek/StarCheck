
from __init__ import *
from Unit import Unit
from Сalculations import *
from ursina import Entity, Vec3, color, sequence, held_keys, Func


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
    def __init__(self, size, start_new_turn, end):
        """Constructor"""
        self.center = Vec3(0, 0, 0)
        self.borders = generate_borders(size)
        self.coordinates = generate_coordinates(self.borders["limits"])
        self.cells = {coord: Cell(coord) for coord in self.coordinates}
        self.cells[self.center].model = 'models/Solid'
        self.cells[self.center].color = color.black
        self.nuclei = {coord: Nucleus(coord) for coord in self.coordinates}
        for el in self.nuclei.values():
            if all([x >= 0.0 for x in [sum(norm * el.position) + l for norm, l in self.borders["plus"]]]):
                el.color = color.peach
            if all([x >= 0.0 for x in [sum(norm * el.position) + l for norm, l in self.borders["minus"]]]):
                el.color = color.cyan
        self.nuclei[self.center].color = color.white
        self.nuclei[self.center].collision = True
        self.nuclei[self.center].on_double_click = todo_nothing
        self.unit_map = {coord: None for coord in self.coordinates}
        self.units = {WHITE: [], BLACK: [], HOLE: []}
        bh = Unit(Piece(), self.what_is_there)
        bh.visible = False
        bh.collider = None
        self.unit_map[self.center] = bh
        self.units[HOLE].append(bh)
        self.selected: Unit = bh
        self.highlighted = set()
        self.legal_move: Legalmove = Legalmove()
        self.next_turn = start_new_turn
        self.catch = todo_nothing
        self.game_over = end

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
                        new_unit = Unit(element_from_iterator, self.what_is_there)
                        self.unit_map[new_unit.position] = new_unit
                        self.units[new_unit.side].append(new_unit)

    def what_is_there(self, point: Vec3):
        if self.center == point:
            return '-'
        elif any([x < 0.0 for x in [sum(norm * point) + l for norm, l in self.borders["limits"]]]):
            return '-'
        elif None == self.unit_map[point]:
            return '_'
        elif Unit == type(self.unit_map[point]):
            return self.unit_map[point].side
        else:
            return -1

    def clean_selection(self):
        # Функция должна делать все клетки невидимыми а фигуры не подсвеченными
        for el in self.highlighted:
            if Unit == type(el):
                el.color = color.white
                el.on_double_click = todo_nothing
            elif Nucleus == type(el):
                el.visible = False
                el.on_double_click = todo_nothing
            else:
                pass#Errror
        self.highlighted = set()
        self.selected = self.units[HOLE]
        self.legal_move = Legalmove()

    def select(self, unit: Unit):
        if self.selected == unit:
            return
        else:
            self.clean_selection()
            self.selected = unit
            self.legal_move = unit.legal_move_generator()
            result = set()
            for el in map(lambda x: self.nuclei[x], self.legal_move.motion):
                result.add(el)
                el.visible = True
                el.on_double_click = Func(self.move, el)
            for el in map(lambda x: self.unit_map[x], self.legal_move.capture & self.legal_move.kill):
                result.add(el)
                el.color = color.orange
                el.on_double_click = Func(self.attack, el) if 0 == held_keys['left control'] else Func(self.destroy, el)
            for el in map(lambda x: self.unit_map[x], self.legal_move.capture - self.legal_move.kill):
                result.add(el)
                el.color = color.yellow
                el.on_double_click = Func(self.attack, el) if 0 == held_keys['left control'] else todo_nothing
            for el in map(lambda x: self.unit_map[x], self.legal_move.kill - self.legal_move.capture):
                result.add(el)
                el.color = color.red
                el.on_double_click = todo_nothing if 0 == held_keys['left control'] else Func(self.destroy, el)
            self.highlighted = result

    def set_units_action(self, active, waiting):
        for el in self.units[active]:
            el.on_click = Func(self.select, el)
        for el in self.units[waiting]:
            el.on_click = todo_nothing

    def move(self, stop: Nucleus):
        self.unit_map[self.selected.position] = None
        self.unit_map[stop.position] = self.selected
        self.selected.position = stop.position
        self.clean_selection()
        self.next_turn()

    def attack(self, capture: Unit):
        if S == capture.form:
            self.clean_selection()
            self.game_over()
        else:
            self.catch(capture.form)
            self.unit_map[capture.position] = None
            self.unit_map[capture.position] = self.selected
            self.unit_map[self.selected.position] = None
            self.selected.set_position(capture.position)
            capture.disable()
            self.clean_selection()
            self.next_turn()


    def destroy(self, target: Unit):
        if S == target.form:
            self.clean_selection()
            self.game_over()
        else:
            self.unit_map[target.position] = None
            target.disable()
            self.clean_selection()
            self.next_turn()


    def switch_select_visibility(self, new: bool = False):
        for point in self.selected.motion:
            self.nuclei[point].visible = new
            self.nuclei[point].ignore_input = not new
        for point in self.selected.capture:
            self.unit_map[point].color = color.yellow if new else color.white
        for point in self.selected.kill:
            prevcolor = self.unit_map[point].color
            self.unit_map[point].color = (color.red if color.white == prevcolor else color.orange) if new else color.white

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