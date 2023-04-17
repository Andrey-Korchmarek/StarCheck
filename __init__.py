from ursina import Vec3
from collections import namedtuple
from itertools import chain

SIDE = [WHITE, BLACK, HOLE] = ['♙' ,'♟︎', '●']
SIDE_NAMES = ["black", "white"]

PieceForm = int
PIECE_FORMS = [A, E, F, Y, M, V, N, I, T, H, X, W, L, Z, G, D, O, S] = range(1, 19)
PIECE_SYMBOLS = [None, "a", "e", "f", "y", "m", "v", "n", "i", "t", "h", "x", "w", "l", "z", "g", "d", "o", "s"]
PIECE_NAMES = [None, 'warrior', 'soldier', 'fighter', 'faerie', 'imp', 'thopter', 'knight', 'mine', 'sputnik',
               'roar', 'rummage', 'lofty', 'onslaught', 'mad', 'magic', 'shielding', 'mercurial', 'sage']
PIECE_TEXTURES = ["none",] + ["stub" for _ in range(1, 17)] + ["vertical", "target"]

VECTORS = [
    (4, 0, 0), (0, 4, 0), (0, 0, 4), #square faces
    (2, 2, 2), (2, 2, -2), (2, -2, 2), (-2, 2, 2), #hexagonal faces
    (4, 4, 0), (4, 0, 4), (0, 4, 4), #near hex-hex edges
    (4, -4, 0), (-4, 0, 4), (0, 4, -4), #distant hex-hex edges
    (16, 4, 4), (16, -4, 4), (16, -4, -4), (16, 4, -4), #square-hex edges X
    (4, 16, 4), (-4, 16, 4), (-4, 16, -4), (4, 16, -4), #square-hex edges Y
    (4, 4, 16), (4, -4, 16), (-4, -4, 16), (-4, 4, 16), #square-hex edges Z
    (8, 4, 0), (8, 0, 4), (8, -4, 0), (8, 0, -4), #vertexes X
    (0, 8, 4), (4, 8, 0), (0, 8, -4), (-4, 8, 0), #vertexes Y
    (4, 0, 8), (0, 4, 8), (-4, 0, 8), (0, -4, 8), #vertexes Z
    (6, 2, 2), (6, 2, -2), (6, -2, 2), (2, 6, 2), (2, 6, -2), (-2, 6, 2), (2, 2, 6), (2, -2, 6), (-2, 2, 6), #knight
]

STEPS = {
    WHITE: list(chain.from_iterable([[Vec3(x), Vec3(x) * (-1)] for x in VECTORS])),
    BLACK: list(chain.from_iterable([[Vec3(x) * (-1), Vec3(x)] for x in VECTORS])),
    HOLE: [Vec3(0, 0, 0) for _ in range(92)]
}

Piece = namedtuple('Piece', 'point form side', defaults = [(0,0,0), None, HOLE])
Legalmove = namedtuple("Legalmove", "motion capture kill", defaults=[set(), set(), set()])

def todo_nothing():
    pass