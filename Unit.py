
from ursina import Entity, Vec3
from __init__ import *

def _pieces_walk_mask(type: int):
    masks = [
        ''.zfill(92),#none
        '1' * 92,  # stub ---- warrior
        '1' * 92,  # stub ---- soldier
        '1' * 92,  # stub ---- fighter
        '1' * 92,  # stub ---- faerie
        '1' * 92,  # stub ---- imp
        '1' * 92,  # stub ---- thopter
        '1' * 92,  # stub ---- knight
        ''.zfill(92),# mine
        '1' * 92,# stub ---- sputnik
        'I' * 14 + ''.zfill(92 - 14),# roar
        ''.zfill(14) + 'I' * (50 - 14) + ''.zfill(92 - 50),# rummage
        ''.zfill(50) + 'I' * (74 - 50) + ''.zfill(92 - 74),# lofty
        '0' * 74 + 'I' * 18, # onslaught
        '1' * 92,  # stub ---- mad
        '1' * 92,  # stub ---- magic
        '1' * 92, #stub ----- shielding
        'I' * 74 + ''.zfill(92 - 74),# mercurial
        '1' * 74 + ''.zfill(92 - 74),# sage
    ]
    return masks[type]

def _pieces_attack_mask(type: int):
    masks = [
        ''.zfill(92),#none
        '1' * 92,  # stub ---- warrior
        '1' * 92,  # stub ---- soldier
        '1' * 92,  # stub ---- fighter
        '1' * 92,  # stub ---- faerie
        '1' * 92,  # stub ---- imp
        '1' * 92,  # stub ---- thopter
        '1' * 92,  # stub ---- knight
        ''.zfill(92),# mine
        '1' * 92,# stub ---- sputnik
        'I' * 14 + ''.zfill(92 - 14),# roar
        ''.zfill(14) + 'I' * (50 - 14) + ''.zfill(92 - 50),# rummage
        ''.zfill(50) + 'I' * (74 - 50) + ''.zfill(92 - 74),# lofty
        '0' * 74 + 'I' * 18, # onslaught
        '1' * 92,  # stub ---- mad
        '1' * 92,  # stub ---- magic
        '1' * 92, #stub ----- shielding
        'I' * 74 + ''.zfill(92 - 74),# mercurial
        '1' * 74 + ''.zfill(92 - 74),# sage
    ]
    return masks[type]

def _pieces_destroy_mask(type: int):
    masks = [
        ''.zfill(92),#none
        '1' * 92,  # stub ---- warrior
        '1' * 92,  # stub ---- soldier
        '1' * 92,  # stub ---- fighter
        '1' * 92,  # stub ---- faerie
        '1' * 92,  # stub ---- imp
        '1' * 92,  # stub ---- thopter
        '1' * 92,  # stub ---- knight
        '1' * 74 + ''.zfill(92 - 74),# mine
        '1' * 92,# stub ---- sputnik
        'I' * 14 + ''.zfill(92 - 14),# roar
        ''.zfill(14) + 'I' * (50 - 14) + ''.zfill(92 - 50),# rummage
        ''.zfill(50) + 'I' * (74 - 50) + ''.zfill(92 - 74),# lofty
        '0' * 74 + 'I' * 18, # onslaught
        '1' * 92,  # stub ---- mad
        '1' * 92,  # stub ---- magic
        '1' * 92, #stub ----- shielding
        'I' * 74 + ''.zfill(92 - 74),# mercurial
        '1' * 74 + ''.zfill(92 - 74),# sage
    ]
    return masks[type]

class Unit(Entity):
    def __init__(self, piece: Piece, board_knowlege):
        self.side = piece.side
        self.form: PieceForm = self.unit_form(piece.form)
        self.move_mask = _pieces_walk_mask(self.form)
        self.capture_mask = _pieces_attack_mask(self.form)
        self.kill_mask = _pieces_destroy_mask(self.form)
        self.state_of_the_cell = board_knowlege
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

    def legal_move_generator(self) -> Legalmove:
        #Генерируется множества пустых клеток на которые можно пойти и врагов которых можно съесть или убить
        result = Legalmove()
        for vector1, sign1 in zip(VECTORS2[self.side], self.move_mask):
            if '0' == sign1:
                continue
            elif '1' == sign1:
                if '_' == self.state_of_the_cell(self.position + vector1):
                    result.motion.add(self.position + vector1)
            elif 'I' == sign1:
                count = 1
                while '_' == self.state_of_the_cell(self.position + vector1 * count):
                    result.motion.add(self.position + vector1 * count)
                    count += 1
        for vector2, sign2 in zip(VECTORS2[self.side], self.capture_mask):
            if '0' == sign2:
                continue
            elif '1' == sign2:
                if self.side + self.state_of_the_cell(self.position + vector2) in ("♙♟︎", "♟︎♙"):
                    result.capture.add(self.position + vector2)
            elif 'I' == sign2:
                count = 1
                while '_' == self.state_of_the_cell(self.position + vector2 * count):
                    count += 1
                if self.side + self.state_of_the_cell(self.position + vector2 * count) in ("♙♟︎", "♟︎♙"):
                    result.capture.add(self.position + vector2 * count)
        for vector3, sign3 in zip(VECTORS2[self.side], self.kill_mask):
            if '0' == sign3:
                continue
            elif '1' == sign3:
                if self.side + self.state_of_the_cell(self.position + vector3) in ("♙♟︎", "♟︎♙"):
                    result.kill.add(self.position + vector3)
            elif 'I' == sign3:
                count = 1
                while '_' == self.state_of_the_cell(self.position + vector3 * count):
                    count += 1
                if self.side + self.state_of_the_cell(self.position + vector3 * count) in ("♙♟︎", "♟︎♙"):
                    result.kill.add(self.position + vector3 * count)
        return result

if __name__ == '__main__':
    print("This is not app!")