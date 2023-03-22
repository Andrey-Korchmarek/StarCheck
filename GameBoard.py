from ursina import Vec3, Entity, color
from itertools import permutations, product
from math import sqrt

class Cell(Entity):
    def __init__(self, pos, **kwargs):
        super().__init__(**kwargs)
        self.model = 'models/Cell'
        self.visible = False
        self.position = pos
        color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
        self.color = color_calc[sum(pos) % 8]

class Nucleus(Entity):
    def __init__(self, pos, **kwargs):
        super().__init__(**kwargs)
        self.model = 'sphere'
        self.visible = False
        self.position = pos
        self.collision = True
        self.collider = 'sphere'

class GameBoard(object):
    def __init__(self, level):
        """Constructor"""
        self.constants = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))
        if level <= 0:
            number_of_layers = 0
        elif int(level) == 1:
            number_of_layers = 1
        elif level < 7:
            number_of_layers = (int(level) - 1) * 4
        else:
            number_of_layers = 24
        normales6 = [Vec3(norm) for norm in product((1, -1), repeat=3)]
        normales4 = [Vec3(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]
        distance6 = self.constants['r6'] * number_of_layers
        distance4 = self.constants['r4'] * number_of_layers
        self.borders = [(norm, distance4) for norm in normales4] + [(norm, distance6) for norm in normales6]
        self.coordinates = self._generate_coordinates(number_of_layers)
        self.cells = {coord: Cell(pos = coord) for coord in self.coordinates}
        self.cells[self.constants["center"]].model = 'models/Solid'
        self.cells[self.constants["center"]].color = color.black
        self.nuclei = {coord: Nucleus(pos = coord) for coord in self.coordinates}
        self.nuclei[self.constants["center"]].collision = True
        self.pieces = {coord: None for coord in self.coordinates}

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
        for el in self.cells.items():
            el.visible = new

    def switch_core_visibility(self):
        if not len(self.nuclei):
            return
        new = not self.nuclei[self.constants["center"]].visible
        for el in self.nuclei.items():
            el.visible = new

if __name__ == '__main__':
    print("This is not app!")