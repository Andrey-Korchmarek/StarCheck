from ursina import Vec3
from itertools import permutations, product
from math import sqrt

class GameBoard(object):
    def __init__(self):
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
        self.r4 = 2

    def generate_cell_pool(self, finish):
        result: set = set()
        previous: set
        next: set = set()
        next.add(self.center)
        for i in range(finish):
            result.update(next)
            previous = next.copy()
            next.clear()
            next.update(*[{pre + new*2 for new in self.faces} for pre in previous])
            next.difference_update(result)
        return result

class Figure(object):
    def __init__(self):
        king = {Vec3(-2, -6, -2), Vec3(2, 6, -2),
                Vec3(0, -4, 8), Vec3(-6, 2, -2),
                Vec3(0, -4, 0), Vec3(6, -2, 2),
                Vec3(-4, 0, 0), Vec3(6, 2, -2),
                Vec3(2, -2, 6), Vec3(2, 2, 6),
                Vec3(4, 4, 0), Vec3(4, 0, 8),
                Vec3(-8, -4, 0), Vec3(4, 0, -8),
                Vec3(-2, 6, -2), Vec3(-4, 0, 4),
                Vec3(-2, 2, -6), Vec3(8, -4, 0),
                Vec3(2, -6, -2), Vec3(4, 0, 0),
                Vec3(-2, -2, -6), Vec3(4, 0, 4),
                Vec3(-4, 0, -8), Vec3(-4, 0, -4),
                Vec3(-2, 6, 2), Vec3(2, -2, -6),
                Vec3(0, 0, -4), Vec3(0, 8, -4),
                Vec3(-6, -2, 2), Vec3(2, -2, -2),
                Vec3(-8, 4, 0), Vec3(-2, 2, 2),
                Vec3(-4, 4, 0), Vec3(-6, 2, 2),
                Vec3(-2, -2, -2), Vec3(2, 2, -6),
                Vec3(0, 4, -8), Vec3(-6, -2, -2),
                Vec3(4, -4, 0), Vec3(4, 0, -4),
                Vec3(-8, 0, 4), Vec3(6, -2, -2),
                Vec3(6, 2, 2), Vec3(-4, -8, 0),
                Vec3(8, 0, -4), Vec3(4, -8, 0),
                Vec3(-2, -6, 2), Vec3(2, -6, 2),
                Vec3(0, 4, 8), Vec3(8, 4, 0),
                Vec3(-4, 0, 8), Vec3(0, 4, -4),
                Vec3(8, 0, 4), Vec3(0, -8, 4),
                Vec3(-2, 2, 6), Vec3(2, 6, 2),
                Vec3(0, 0, 4), Vec3(-2, -2, 2),
                Vec3(2, 2, -2), Vec3(0, -4, -8),
                Vec3(0, 4, 0), Vec3(2, 2, 2),
                Vec3(-4, 8, 0), Vec3(4, 8, 0),
                Vec3(0, 8, 4), Vec3(-2, 2, -2),
                Vec3(2, -2, 2), Vec3(0, 4, 4),
                Vec3(0, -4, -4), Vec3(0, -8, -4),
                Vec3(-4, -4, 0), Vec3(-8, 0, -4),
                Vec3(0, -4, 4), Vec3(-2, -2, 6)}
        self.king = tuple(king)

if __name__ == '__main__':
    print("This is not app!")
    piece = Figure()
    print(len(piece.king))
    print(14 + 36 + 24)
    for k in piece.king:
        print(k)
