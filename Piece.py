from ursina import *

PieceType = int
PIECE_TYPES = [A, E, F, Y, I, V, N, M, T, H, X, W, L, Z, G, D, O, S] = range(1, 19)
PIECE_SYMBOLS = [None, "a", "e", "f", "y", "i", "v", "n", "m", "t", "h", "x", "w", "l", "z", "g", "d", "o", "s"]
PIECE_NAMES = [None, 'warrior', 'soldier', 'fighter', 'faerie', 'imp', 'thopter', 'knight', 'mine', 'sputnik',
               'roar', 'rummage', 'lofty', 'onslaught', 'mad', 'magic', 'shielding', 'mercurial', 'sage']

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
class Piece(Entity):
    def __init__(self, begin = (2, 2, 2), code: str = 'stub', **kwargs):
        """Constructor"""
        super().__init__(**kwargs)
        vectors = [
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
        ]
        codes = dict(S=1, O=1, D=1, H=1, X=1, W=1, L=1, Z=1, G=1, stub='stub')
        self.position = begin
        self.model = "sphere"
        self.scale = 1.5
        self.texture = 'textures/'.__add__(codes[code])

    def change_position(self, new):
        pass

    def move(self):
        pass

    def capture(self):
        pass

    def kill(self):
        pass

if __name__ == '__main__':
    print("This is not app!")
    app = Ursina()
    vectors = [
        (4, 0, 0), (0, 4, 0), (0, 0, 4), #square faces
        (2, 2, 2), (2, 2, -2), (2, -2, 2), (-2, 2, 2), #hexagonal faces
        (4, 4, 0), (4, 0, 4), (0, 4, 4), #near hex-hex edges
        (4, -4, 0), (-4, 0, 4), (0, 4, -4), #distant hex-hex edges
        (16, 4, 4), (16, -4, 4), (16, -4, -4), (6, 4, -4), #square-hex edges X
        (4, 16, 4), (-4, 16, 4), (-4, 16, -4), (4, 16, -4), #square-hex edges Y
        (4, 4, 16), (4, -4, 16), (-4, -4, 16), (-4, 4, 16), #square-hex edges Z
        (8, 4, 0), (8, 0, 4), (8, -4, 0), (8, 0, -4), #vertexes X
        (0, 8, 4), (4, 8, 0), (0, 8, -4), (-4, 8, 0), #vertexes Y
        (4, 0, 8), (0, 4, 8), (-4, 0, 8), (0, -4, 8), #vertexes Z
        (6, 2, 2), (6, 2, -2), (6, -2, 2), (2, 6, 2), (2, 6, -2), (-2, 6, 2), (2, 2, 6), (2, -2, 6), (-2, 2, 6), #knight
    ]
    vectors = [Vec3(x) for x in vectors]
    vectors2 = {f + e + v
                for f in vectors[:7] + [-x for x in vectors[:7]]
                for e in vectors[7:25] + [-x for x in vectors[7:25]]
                for v in vectors[25:37] + [-x for x in vectors[25:37]]}
    quin = set().union([x for x in vectors], [-x for x in vectors],
                       [x * 2 for x in vectors], [(-x) * 2 for x in vectors],
                       [x * 3 for x in vectors], [(-x) * 3 for x in vectors],
                       [x * 4 for x in vectors], [(-x) * 4 for x in vectors])
    vectors2.difference_update(quin)
    vectors2 = list(vectors2)
    vectors3 = [Vec3(0, 0, 0), ]
    for vec in vectors2:
        x, y, z = vec
        x = int(x)
        y = int(y)
        z = int(z)
        if (abs(x) % 4) == (abs(y) % 4) == (abs(z) % 4):
            vectors3.append(vec)
    color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
    turns = [Entity(model='models/Solid', visible=False, position=pos, color=color_calc[sum(pos) % 8]) for pos in vectors3]
    y = turns[0]
    turns = [x for x in turns if distance(x, y) < 7.0]
    for i, x in enumerate(turns):
        print(i, x.position, distance(x, y))
    one_by_one = iter(turns)
    result = list()
    prev = next(one_by_one)
    prev.visible = True
    prev.color = color.black
    def input(key):
        global prev
        global result
        if key == 'space':
            prev.color = color_calc[sum(prev.position) % 8]
            prev = next(one_by_one)
            prev.visible = True
            prev.color = color.black
        if key == 'd':
            prev.visible = False
        if key == 'p':
            x, y, z = prev.position
            result.append((int(x), int(y), int(z)))
            prev.color = color.white
            print(turns.index(prev), (int(x), int(y), int(z)))
            print(result)

    EditorCamera()
    app.run()