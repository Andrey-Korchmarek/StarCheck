from ursina import Vec3, Entity, color
from itertools import permutations, product
from math import sqrt

class GameBoard(object):
    def __init__(self, number_of_layers):
        """Constructor"""
        constants = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))
        faces = set(product((1, -1), repeat=3)).union(*[set(permutations((i, 0, 0))) for i in (2, -2)])
        faces = [Vec3(dot) for dot in faces]
        if number_of_layers <= 0:
            border = 0
        elif int(number_of_layers) == 1:
            border = 1
        elif number_of_layers < 7:
            border = (number_of_layers - 1) * 4
        else:
            border = 24
        normales6 = [Vec3(norm) for norm in product((1, -1), repeat=3)]
        normales4 = [Vec3(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]
        def is_point_in_borders(point):
            distance6 = constants['r6'] * border
            distance4 = constants['r4'] * border
            normales = set([sum(vec * point) + distance4 for vec in normales4])\
                .union([sum(vec * point) + distance6 for vec in normales6])
            return all([x >= 0.0 for x in normales])
        coordinates: set = set()
        previous: set
        next: set = {constants['center']} if border > 0 else set()
        while next:
            coordinates.update(next)
            previous = next.copy()
            next.clear()
            next.update(*[{pre + new * 2 for new in faces} for pre in previous])
            next.difference_update(coordinates)
            next = {x for x in next if is_point_in_borders(x)}
        coordinates.remove(constants['center'])
        coordinates = list(coordinates)
        self.cells = [Entity(model='models/Solid', visible=False, color=color.black)]
        color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
        self.cells.extend([Entity(model='models/Cell', visible=False, position=pos, color=color_calc[sum(pos) % 8]) for pos in coordinates])

    def changing_visibility(self):
        new = not self.cells[0].visible
        for el in self.cells:
            el.visible = new

