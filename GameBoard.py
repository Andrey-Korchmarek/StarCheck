from ursina import Vec3, Entity, color
from ursina.sequence import *
from collections import namedtuple
from itertools import permutations, product
from math import sqrt

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
            visible = False,
            model = 'sphere',
            collision = True,
            collider = 'sphere',
            position = pos,
            )

Piece = namedtuple('Piece', 'point form', defaults = [None])
PieceForm = int
PIECE_FORMS = [A, E, F, Y, M, V, N, I, T, H, X, W, L, Z, G, D, O, S] = range(1, 19)
PIECE_SYMBOLS = [None, "a", "e", "f", "y", "m", "v", "n", "i", "t", "h", "x", "w", "l", "z", "g", "d", "o", "s"]
PIECE_NAMES = [None, 'warrior', 'soldier', 'fighter', 'faerie', 'imp', 'thopter', 'knight', 'mine', 'sputnik',
               'roar', 'rummage', 'lofty', 'onslaught', 'mad', 'magic', 'shielding', 'mercurial', 'sage']
PIECE_TEXTURES = ["stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub",
                  "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "none"]

class Unit(Entity):
    def __init__(self, piece: Piece):
        self.form: PieceForm = self.unit_form(piece.form)
        super().__init__(
            model = 'sphere',
            texture = 'textures/' + PIECE_TEXTURES[self.form],
            collision = True,
            collider = 'sphere',
            position = Vec3(piece.point),
            scale = 1.5,
            billboard = True,
        )


    def unit_form(self, id) -> PieceForm:
        if id in PIECE_FORMS:
            return id
        else:
            id = id.__str__().lower()
        if id in PIECE_SYMBOLS:
            return PIECE_SYMBOLS[id]
        elif id.__str__().lower() in PIECE_NAMES:
            return PIECE_NAMES[id]
        else:
            return -1


class GameBoard(object):
    def __init__(self, size, pieces = []):
        """Constructor"""
        self.constants = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))
        if size <= 0:
            number_of_layers = 0
        elif int(size) == 1:
            number_of_layers = 1
        elif size < 7:
            number_of_layers = (int(size) - 1) * 4
        else:
            number_of_layers = 24
        normales6 = [Vec3(norm) for norm in product((1, -1), repeat=3)]
        normales4 = [Vec3(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]
        distance6 = self.constants['r6'] * number_of_layers
        distance4 = self.constants['r4'] * number_of_layers
        self.borders = [(norm, distance4) for norm in normales4] + [(norm, distance6) for norm in normales6]
        self.coordinates = self._generate_coordinates(number_of_layers)
        self.cells = {coord: Cell(pos= coord) for coord in self.coordinates}
        self.cells[self.constants["center"]].model = 'models/Solid'
        self.cells[self.constants["center"]].color = color.black
        self.nuclei = {coord: Nucleus(pos= coord) for coord in self.coordinates}
        self.nuclei[self.constants["center"]].collision = True
        self.units = {coord: None for coord in self.coordinates}
        self.selected: Unit = None
        if len(pieces):
            for el in pieces:
                new_unit = Unit(el)
                new_unit.on_click = Sequence(self.select(new_unit), self.legal_move(self.selected))
                self.units[Vec3(el.point)] = new_unit
        for el in self.nuclei.values():
            prev = self.selected.position
            next = el.position
            el.on_click = Sequence()

    def select(self, new: Unit) -> None:
        self.selected = new

    def legal_move(self, unit: Unit) -> None:
        pass

    def _is_point_in_borders(self, point: Vec3):
        return all([x >= 0.0 for x in [sum(normal * point) + distance for normal, distance in self.borders]])

    def _generate_coordinates(self, number_of_layers):
        result: set = set()
        previous: set
        next: set = {self.constants['center']} if number_of_layers else set()

        faces = set(product((1, -1), repeat=3)).union(*[set(permutations((i, 0, 0))) for i in (2, -2)])
        faces = [Vec3(dot) for dot in faces]
        while next:
            result.update(next)
            previous = next.copy()
            next.clear()
            next.update(*[{pre + new * 2 for new in faces} for pre in previous])
            next.difference_update(result)
            next = {x for x in next if self._is_point_in_borders(x)}
        return result

    def switch_cell_visibility(self):
        if not len(self.cells):
            return
        new = not self.cells[self.constants["center"]].visible
        for el in self.cells.values():
            el.visible = new

    def switch_core_visibility(self):
        if not len(self.nuclei):
            return
        new = not self.nuclei[self.constants["center"]].visible
        for el in self.nuclei.values():
            el.visible = new

if __name__ == '__main__':
    print("This is not app!")