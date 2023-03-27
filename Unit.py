from ursina import *
from collections import namedtuple
import GameBoard

Side = bool
SIDE = [WHITE, BLACK] = [True, False]
SIDE_NAMES = ["black", "white"]

Piece = namedtuple('Piece', 'side point form', defaults = [None])
PieceForm = int
PIECE_FORMS = [A, E, F, Y, M, V, N, I, T, H, X, W, L, Z, G, D, O, S] = range(1, 19)
PIECE_SYMBOLS = [None, "a", "e", "f", "y", "m", "v", "n", "i", "t", "h", "x", "w", "l", "z", "g", "d", "o", "s"]
PIECE_NAMES = [None, 'warrior', 'soldier', 'fighter', 'faerie', 'imp', 'thopter', 'knight', 'mine', 'sputnik',
               'roar', 'rummage', 'lofty', 'onslaught', 'mad', 'magic', 'shielding', 'mercurial', 'sage']
PIECE_TEXTURES = ["stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub",
                  "stub", "stub", "stub", "stub", "stub", "stub", "stub", "stub", "none"]

Legalmove = namedtuple("Legalmove", "source motion capture kill", defaults=[None, set(), set(), set()])
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
class Unit(Entity):
    def __init__(self, piece: Piece, board: GameBoard):
        self.side = piece.side
        self.form: PieceForm = self.unit_form(piece.form)
        self.board = board
        super().__init__(
            model='sphere',
            texture='textures/' + PIECE_TEXTURES[self.form],
            collision=True,
            collider='sphere',
            position=Vec3(piece.point),
            scale=1.5,
            billboard=True,
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

    def on_click(self):
        #По клику на фигуру она становится выбранной и все её возможные ходы становятся видимыми
        super().on_click()
        pass

    def on_double_click(self):
        # По двойному клику на фигуру её ест или убивает выбранная фигура, если они разного цвета
        super().on_double_click()
        pass

    def legal_move_generator(self) -> Legalmove:
        #Генерируется множества пустых клеток на которые можно пойти и врагов которых можно съесть или убить
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