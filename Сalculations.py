from ursina import Vec3
from itertools import permutations, product
from math import sqrt

class GameBoard(object):
    def __init__(self):
        """Constructor"""
        center = (0, 0, 0)
        vertexes = set().union(*[list(permutations(elem)) for elem in [(0, u, d) for u in (1, -1) for d in (2, -2)]])
        edges = set().union(*[list(permutations((0, u, d))) for u in (1.5, -1.5) for d in (1.5, -1.5)])\
            .union(*[list(permutations((z, u, d))) for z in (0.5, -0.5) for u in (0.5, -0.5) for d in (2, -2)])
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
        start = {self.center}
        previous = set()



if __name__ == '__main__':
    print("This is not app!")
    board = GameBoard()
    print(board.edges)
