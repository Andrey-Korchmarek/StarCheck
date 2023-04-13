
from ursina import Entity, Vec3
from __init__ import WHITE, BLACK, Piece, PieceForm, PIECE_TEXTURES, PIECE_FORMS, PIECE_SYMBOLS, PIECE_NAMES, Legalmove, VECTORS, FORMS_WALK_VECTORS, FORMS_ATTACK_VECTORS, FORMS_DESTROY_VECTORS



class Unit(Entity):
    def __init__(self, piece: Piece, board):
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
            #billboard=True,
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