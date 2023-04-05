
from ursina import Entity, Vec3, held_keys
from collections import namedtuple
from itertools import chain


Side = int
SIDE = [WHITE, BLACK] = [1, 2]
SIDE_NAMES = ["black", "white"]

Piece = namedtuple('Piece', 'point form side', defaults = [None, WHITE])
PieceForm = int
PIECE_FORMS = [A, E, F, Y, M, V, N, I, T, H, X, W, L, Z, G, D, O, S] = range(1, 19)
PIECE_SYMBOLS = [None, "a", "e", "f", "y", "m", "v", "n", "i", "t", "h", "x", "w", "l", "z", "g", "d", "o", "s"]
PIECE_NAMES = [None, 'warrior', 'soldier', 'fighter', 'faerie', 'imp', 'thopter', 'knight', 'mine', 'sputnik',
               'roar', 'rummage', 'lofty', 'onslaught', 'mad', 'magic', 'shielding', 'mercurial', 'sage']
PIECE_TEXTURES = ["none",] + ["stub" for _ in range(1, 20)]

Legalmove = namedtuple("Legalmove", "source motion capture kill", defaults=[None, set(), set(), set()])
VECTORS = list(chain.from_iterable([[Vec3(x), Vec3(x) * (-1)] for x in[
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
]]))
'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
FORMS_WALK_VECTORS = [
    ''.zfill(92),#none
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '10000000000000000000000000000000000000000000000010000000000000000000000000100000000000000000',#stub
    '11111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000',#sage
]
FORMS_ATTACK_VECTORS = FORMS_WALK_VECTORS
FORMS_DESTROY_VECTORS = FORMS_WALK_VECTORS

class Unit(Entity):
    def __init__(self, piece: Piece):
        self.side = piece.side
        self.form: PieceForm = self.unit_form(piece.form)
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
        if 0 == id or None == id:
            return 0
        elif id in PIECE_FORMS:
            return id
        else:
            id = id.__str__().lower()
        if id in PIECE_SYMBOLS:
            return PIECE_SYMBOLS.index(id)
        elif id in PIECE_NAMES:
            return PIECE_NAMES.index(id)
        else:
            return -1

    def as_empty(self, walkset: set, vector: Vec3) -> bool:
        point = self.position + vector
        if 0 == self.board.what_is_there(point):
            walkset.add(point)
            return True
        else:
            return False

    def to_enemy(self, enemyset: set, vector: Vec3):
        point = self.position + vector
        player = 1 if WHITE == self.side else 2
        wit = self.board.what_is_there(point)
        if None == wit:
            return False
        elif 0 == wit:
            return True
        elif wit == player:
            return False
        else:
            enemyset.add(point)
            return False

    def legal_move_generator(self) -> Legalmove:
        #Генерируется множества пустых клеток на которые можно пойти и врагов которых можно съесть или убить
        result = Legalmove(source = self)
        for id, s in enumerate(FORMS_WALK_VECTORS[self.form]):
            if '0' == s:
                continue
            elif '1' == s:
                self.as_empty(result.motion, VECTORS[id])
            elif 'I' == s:
                count = 1
                while self.as_empty(result.motion, VECTORS[id] * count):
                    count += 1
        for id, s in enumerate(FORMS_ATTACK_VECTORS[self.form]):
            if '0' == s:
                continue
            elif '1' == s:
                self.to_enemy(result.capture, VECTORS[id])
            elif 'I' == s:
                count = 1
                while self.to_enemy(result.capture, VECTORS[id] * count):
                    count += 1
        for id, s in enumerate(FORMS_DESTROY_VECTORS[self.form]):
            if '0' == s:
                continue
            elif '1' == s:
                self.to_enemy(result.kill, VECTORS[id])
            elif 'I' == s:
                count = 1
                while self.to_enemy(result.kill, VECTORS[id] * count):
                    count += 1
        return result

if __name__ == '__main__':
    print("This is not app!")