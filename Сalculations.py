from ursina import Vec3, Entity, color
from itertools import permutations, product
from math import sqrt



class GameBoard(object):
    def __init__(self, number_of_layers):
        """Constructor"""
        center = (0, 0, 0)
        vertexes = set().union(*[list(permutations(elem)) for elem in [(0, u, d) for u in (1, -1) for d in (2, -2)]])
        edges = set().union(*[list(permutations((0, u, d))) for u in (1.5, -1.5) for d in (1.5, -1.5)])
        edges.update(*[list(permutations((z, u, d))) for z in (0.5, -0.5) for u in (0.5, -0.5) for d in (2, -2)])
        faces = set(product((1, -1), repeat=3)).union(*[set(permutations((i, 0, 0))) for i in (2, -2)])
        self.center = Vec3(center)
        self.vertexes = tuple(Vec3(dot) for dot in vertexes)
        self.edges = tuple(Vec3(dot) for dot in edges)
        self.faces = tuple(Vec3(dot) for dot in faces)
        self.a = sqrt(2)
        self.R = sqrt(5)
        self.p = 1.5 * sqrt(2)
        self.r6 = sqrt(3)
        self.r4 = 2.0
        if number_of_layers <= 0:
            self.border = 0
        elif int(number_of_layers) == 1:
            self.border = 1
        else:
            self.border = (number_of_layers - 1) * 4
        #self.border = number_of_layers
        self.normales6 = [Vec3(norm) for norm in product((1, -1), repeat=3)]
        self.normales4 = [Vec3(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]



    def _borders_check_(self, point):
        distance6 = self.r6 * self.border
        distance4 = self.r4 * self.border
        normales = set().union([sum(vec * point) + distance4 for vec in self.normales4], [sum(vec * point) + distance6 for vec in self.normales6])
        return all([x >= 0.0 for x in normales])

    def generate_cell_pool(self):
        result: set = set()
        previous: set
        next: set = {self.center} if self.border > 0 else set()
        while next:
            result.update(next)
            previous = next.copy()
            next.clear()
            next.update(*[{pre + new*2 for new in self.faces} for pre in previous])
            next.difference_update(result)
            next = {x for x in next if self._borders_check_(x)}
        return result

class Figure(object):
    def __init__(self):
        self.king = [
            Vec3(2, 2, 2), Vec3(-2, -2, -2),
            Vec3(2, 2, -2), Vec3(-2, -2, 2),
            Vec3(2, -2, 2), Vec3(-2, 2, -2),
            Vec3(-2, 2, 2), Vec3(2, -2, -2),
            Vec3(4, 0, 0), Vec3(-4, 0, 0),
            Vec3(0, 4, 0), Vec3(0, -4, 0),
            Vec3(0, 0, 4), Vec3(0, 0, -4),
            Vec3(4, 4, 0), Vec3(-4, -4, 0),
            Vec3(4, 0, 4), Vec3(-4, 0, -4),
            Vec3(0, 4, 4), Vec3(0, -4, -4),
            Vec3(4, -4, 0), Vec3(-4, 4, 0),
            Vec3(4, 0, -4), Vec3(-4, 0, 4),
            Vec3(0, 4, -4), Vec3(0, -4, 4),
            Vec3(6, 2, 2), Vec3(-6, -2, -2),
            Vec3(6, 2, -2), Vec3(-6, -2, 2),
            Vec3(6, -2, 2), Vec3(-6, 2, -2),
            Vec3(6, -2, -2), Vec3(-6, 2, 2),
            Vec3(2, 6, 2), Vec3(-2, -6, -2),
            Vec3(2, 6, -2), Vec3(-2, -6, 2),
            Vec3(-2, 6, 2), Vec3(2, -6, -2),
            Vec3(-2, 6, -2), Vec3(2, -6, 2),
            Vec3(2, 2, 6), Vec3(-2, -2, -6),
            Vec3(2, -2, 6), Vec3(-2, 2, -6),
            Vec3(-2, 2, 6), Vec3(2, -2, -6),
            Vec3(-2, -2, 6), Vec3(2, 2, -6),
            Vec3(8, 4, 0), Vec3(-8, -4, 0),
            Vec3(8, 0, 4), Vec3(-8, 0, -4),
            Vec3(8, -4, 0), Vec3(-8, 4, 0),
            Vec3(8, 0, -4), Vec3(-8, 0, 4),
            Vec3(4, 8, 0), Vec3(-4, -8, 0),
            Vec3(0, 8, 4), Vec3(0, -8, -4),
            Vec3(0, 8, -4), Vec3(0, -8, 4),
            Vec3(-4, 8, 0), Vec3(4, -8, 0),
            Vec3(4, 0, 8), Vec3(-4, 0, -8),
            Vec3(0, 4, 8), Vec3(0, -4, -8),
            Vec3(0, -4, 8), Vec3(0, 4, -8),
            Vec3(-4, 0, 8), Vec3(4, 0, -8),
        ]

def outside_to_inside_dot(position, delta = 12):
    dlen = 1/delta
    mask = tuple(abs(i) for i in position)
    z = mask.index(0)
    u = mask.index(1)
    d = mask.index(2)
    us = position[u]
    ds = position[d] // 2
    up = list(position)
    right = list(position)
    left = list(position)
    up[u] = us * (1 - dlen)
    right[z] = dlen
    right[d] = ds * (2 - dlen)
    left[z] = -dlen
    left[d] = ds * (2 - dlen)
    return [tuple(up), tuple(right), tuple(left)]

def fore_each(entitys: Entity):
    for e in entitys:
        e.disable()

def test(layer):
    board = GameBoard(layer)
    color_calculation = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
    cells = [Entity(model='models/Cell', position=pos, color=color_calculation[sum(pos) % 8]) for pos in
             board.generate_cell_pool()]


if __name__ == '__main__':
    print("This is not app!")

