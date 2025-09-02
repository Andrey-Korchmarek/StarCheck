from __init__ import *
import core
import render
from itertools import chain

"""
Любое действие фигур ограничено клетками поля.
Каждой фигуре доступно три варианта действий - передвижение, захват и выстрел.
Передвижение - фигура меняет своё положение на поле, цель передвижения обязана быть пустой клеткой.
Захват - фигура меняет своё положение на поле, цель захвата обязана быть клеткой с вражеской фигурой, 
вражеская фигура при этом побеждается.
Выстрел - вражеская фигура побеждается фигурой Игрока, при этом фигура не меняет положение на поле.
Пешки - фигуры, чей ход отличатся для передвижения, захвата и выстрела,
а ходят они только на 1 клетку и только вперёд, всего их 6 видов.
"""

P_means_PAUNS = "01010101010101010101000000010101010101010101010101010101010101010101010101010101010101010101"

pieceFormsValues = {
    # Заглушка. Ничего не делает, без текстуры и имени
    0: {
        "symbol": '',
        "name": 'None',
        "texture": None,
        "walk_mask": ''.zfill(92),
        "attack_mask": ''.zfill(92),
        "destroy_mask": ''.zfill(92),
    },
    # Пешка №1, передвигается ортогонально, захватывает диагонально, стреляет триагонально
    1: {
        "symbol": 'a',
        "name": "warrior",
        "texture": "assets/textures/stub",
        "walk_mask": P_means_PAUNS[:14] + ''.zfill(92 - 14),
        "attack_mask": ''.zfill(25) + P_means_PAUNS[25:50] + ''.zfill(92 - 50),
        "destroy_mask": ''.zfill(50) + P_means_PAUNS[50:74] + ''.zfill(92 - 74),
    },
    # Пешка №2, передвигается ортогонально, захватывает триагонально, стреляет диагонально
    2: {
        "symbol": "e",
        "name": "soldier",
        "texture": "assets/textures/stub",
        "walk_mask": P_means_PAUNS[:14] + ''.zfill(92 - 14),
        "attack_mask": ''.zfill(50) + P_means_PAUNS[50:74] + ''.zfill(92 - 74),
        "destroy_mask": ''.zfill(25) + P_means_PAUNS[25:50] + ''.zfill(92 - 50),
    },
    # Пешка №3, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    3: {
        "symbol": "f",
        "name": 'fighter',
        "texture": "assets/textures/stub",
        "walk_mask": ''.zfill(14) + ''.zfill(25 - 14) + P_means_PAUNS[25:50] + ''.zfill(92 - 50),
        "attack_mask": ''.zfill(50) + P_means_PAUNS[50:74] + ''.zfill(92 - 74),
        "destroy_mask": P_means_PAUNS[:14] + ''.zfill(92 - 14),
    },
    # Пешка №4, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    4: {
        "symbol": "y",
        "name": 'faerie',
        "texture": "assets/textures/stub",
        "walk_mask": ''.zfill(14) + ''.zfill(25 - 14) + P_means_PAUNS[25:50] + ''.zfill(92 - 50),
        "attack_mask": P_means_PAUNS[:14] + ''.zfill(92 - 14),
        "destroy_mask": ''.zfill(50) + P_means_PAUNS[50:74] + ''.zfill(92 - 74),
    },
    # Пешка №5, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    5: {
        "symbol": "m",
        "name": 'imp',
        "texture": "assets/textures/stub",
        "walk_mask": ''.zfill(50) + P_means_PAUNS[50:74] + ''.zfill(92 - 74),
        "attack_mask": P_means_PAUNS[:14] + ''.zfill(92 - 14),
        "destroy_mask": ''.zfill(25) + P_means_PAUNS[25:50] + ''.zfill(92 - 50),
    },
    # Пешка №6, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    6: {
        "symbol": "v",
        "name": 'thopter',
        "texture": "assets/textures/stub",
        "walk_mask": ''.zfill(50) + P_means_PAUNS[50:74] + ''.zfill(92 - 74),
        "attack_mask": ''.zfill(25) + P_means_PAUNS[25:50] + ''.zfill(92 - 50),
        "destroy_mask": P_means_PAUNS[:14] + ''.zfill(92 - 14),
    },
    # Ладья, передвигается, захватывает и стреляет ортогонально на любое число клеток
    7: {
        "symbol": "h",
        "name": 'roar',
        "texture": "stub",
        "walk_mask": 'I' * 14 + ''.zfill(92 - 14),
        "attack_mask": 'I' * 14 + ''.zfill(92 - 14),
        "destroy_mask": 'I' * 14 + ''.zfill(92 - 14),
    },
    # Слон, передвигается, захватывает и стреляет диагонально на любое число клеток
    8: {
        "symbol": "x",
        "name": 'rummage',
        "texture": "stub",
        "walk_mask": ''.zfill(25) + 'I' * (50 - 25) + ''.zfill(92 - 50),
        "attack_mask": ''.zfill(25) + 'I' * (50 - 25) + ''.zfill(92 - 50),
        "destroy_mask": ''.zfill(25) + 'I' * (50 - 25) + ''.zfill(92 - 50),
    },
    # Рух, передвигается, захватывает и стреляет триагонально на любое число клеток
    9: {
        "symbol": "w",
        "name": 'lofty',
        "texture": "stub",
        "walk_mask": ''.zfill(50) + 'I' * (74 - 50) + ''.zfill(92 - 74),
        "attack_mask": ''.zfill(50) + 'I' * (74 - 50) + ''.zfill(92 - 74),
        "destroy_mask": ''.zfill(50) + 'I' * (74 - 50) + ''.zfill(92 - 74),
    },
    # Конь, передвигается прыжками на комбинацию из движений на 1 клетку в каждом направлении
    # на расстояние ближайших к Ферзю клеток, которые тот не может атаковать
    10: {
        "symbol": "n",
        "name": 'knight',
        "texture": "stub",
        "walk_mask": ''.zfill(74) + '1' * (92 - 74),
        "attack_mask": ''.zfill(74) + '1' * (92 - 74),
        "destroy_mask": ''.zfill(74) + '1' * (92 - 74),
    },
    # Ферзь, передвигается, захватывает и стреляет на любое число клеток в любом одном направлении
    11: {
        "symbol": "o",
        "name": 'mercurial',
        "texture": "vertical",
        "walk_mask": 'I' * 14 + ''.zfill(25 - 14) + 'I' * (74 - 25) + ''.zfill(92 - 74),
        "attack_mask": 'I' * 14 + ''.zfill(25 - 14) + 'I' * (74 - 25) + ''.zfill(92 - 74),
        "destroy_mask": 'I' * 14 + ''.zfill(25 - 14) + 'I' * (74 - 25) + ''.zfill(92 - 74),
    },
    # Король, передвигается, захватывает и стреляет на 1 клетку в любом одном направлении
    # Когда любая фигура противника получает возможность захватить или застрелить Короля, его Игроку объявляется ШАХ
    # Когда Король захвачен или застрелен игра заканчивается поражением Игрока, владевшего этим королём
    12: {
        "symbol": "s",
        "name": 'sage',
        "texture": "assets/textures/target",
        "walk_mask": '1' * 14 + ''.zfill(25 - 14) + '1' * (74 - 25) + ''.zfill(92 - 74),
        "attack_mask": '1' * 14 + ''.zfill(25 - 14) + '1' * (74 - 25) + ''.zfill(92 - 74),
        "destroy_mask": '1' * 14 + ''.zfill(25 - 14) + '1' * (74 - 25) + ''.zfill(92 - 74),
    },
}

SIDE = [WHITE, BLACK, HOLE] = ['♙', '♟︎', '●']
SIDE_NAMES = ["black", "white", "hole"]

VECTORS = [
    (4, 0, 0), (0, 4, 0), (0, 0, 4),  # square faces
    (2, 2, 2), (2, 2, -2), (2, -2, 2), (-2, 2, 2),  # hexagonal faces
    (4, 4, 0), (4, 0, 4), (0, 4, 4),  # near hex-hex edges
    (4, -4, 0), (-4, 0, 4), (0, 4, -4),  # distant hex-hex edges
    (16, 4, 4), (16, -4, 4), (16, -4, -4), (16, 4, -4),  # square-hex edges X
    (4, 16, 4), (-4, 16, 4), (-4, 16, -4), (4, 16, -4),  # square-hex edges Y
    (4, 4, 16), (4, -4, 16), (-4, -4, 16), (-4, 4, 16),  # square-hex edges Z
    (8, 4, 0), (8, 0, 4), (8, -4, 0), (8, 0, -4),  # vertexes X
    (0, 8, 4), (4, 8, 0), (0, 8, -4), (-4, 8, 0),  # vertexes Y
    (4, 0, 8), (0, 4, 8), (-4, 0, 8), (0, -4, 8),  # vertexes Z
    (6, 2, 2), (6, 2, -2), (6, -2, 2), (2, 6, 2), (2, 6, -2), (-2, 6, 2), (2, 2, 6), (2, -2, 6), (-2, 2, 6),  # knight
]

STEPS = {
    WHITE: list(chain.from_iterable([[Vec3(x), Vec3(x) * (-1)] for x in VECTORS])),
    BLACK: list(chain.from_iterable([[Vec3(x) * (-1), Vec3(x)] for x in VECTORS]))
}

startingPositionOfPieces = {
    2: {
        WHITE: [(Vec3(x), formId, WHITE) for x, formId in zip(
            [(2, 2, 2), (4, 0, 0), (0, 4, 0), (0, 0, 4), (2, -2, 2), (2, 2, -2), (-2, 2, 2)],
            [12, 6, 5, 4, 3, 2, 1])],
        BLACK: [(Vec3(x), formId, BLACK) for x, formId in zip(
            [(-2, -2, -2), (-4, 0, 0), (0, -4, 0), (0, 0, -4), (-2, 2, -2), (-2, -2, 2), (2, -2, -2)],
            [12, 6, 5, 4, 3, 2, 1])],
    },
    3: {
        WHITE: [(Vec3(x), formId, WHITE) for x, formId in zip(
            [(2, 2, 2), ],
            [12])],
        BLACK: [(Vec3(x), formId, BLACK) for x, formId in zip(
            [(-2, -2, -2), ],
            [12])],
    }
}


@component
class Piece:
    color = color.gray
    type_id: int = 0
    type_symbol: str = ''
    type_name: str = 'None'


@component
class Side:
    side: str = None


@component
class Move:
    walk_mask: str = ''.zfill(92)
    attack_mask: str = ''.zfill(92)
    destroy_mask: str = ''.zfill(92)

@component
class Selected:
    color = color.green

@component
class Nonactive:
    color = color.white

@component
class Walkable:
    color = color.yellow

@component
class UnderAttack:
    color = color.orange

@component
class Captured:
    pass

@component
class UnderDestroy:
    color = color.red

@component
class Destroyed:
    pass

def create_start_pieces(size):
    for side in startingPositionOfPieces[size].values():
        for pos, id, c in side:
            settings.FEN = pieceFormsValues[id]['symbol'].upper() if c == WHITE else pieceFormsValues[id]['symbol']
            ent = create_entity(core.Position(pos),
                                Piece(type_id=id, type_symbol=pieceFormsValues[id]['symbol'],
                                      type_name=pieceFormsValues[id]['name']),
                                Side(c),
                                Move(walk_mask=pieceFormsValues[id]['walk_mask'],
                                     attack_mask=pieceFormsValues[id]['attack_mask'],
                                     destroy_mask=pieceFormsValues[id]['destroy_mask']),
                                render.Renderable(position=pos, scale=sqrt(3),
                                                  texture=pieceFormsValues[id]['texture'],
                                                  rotation=(-45, 180, -45) if c == BLACK else (-45, 0, -45),
                                                  collider='sphere', collision=True))
            settings.EFEN['PIECES'][pos] = ent

class MovementProcessor(Processor):
    def __init__(self):
        set_handler("select", self.select)
        set_handler("walk needed", self.walk_generate)
        set_handler("walk", self.walk)
        set_handler("attack needed", self.attack_generate)
        set_handler("attack", self.attack)
        set_handler("destroy needed", self.destroy_generate)
        set_handler("destroy", self.destroy)

    active_unit = None

    def select(self, new):
        if new == self.active_unit:
            return
        else:
            if None != self.active_unit:
                remove_component(self.active_unit, Selected)
                add_component(self.active_unit, Nonactive())
            self.active_unit = new
            if None != self.active_unit:
                add_component(self.active_unit, Selected())
            dispatch_event("change selection")

    def walk_generate(self):
        if None == self.active_unit:
            return
        for vector, sign in zip(STEPS[try_component(self.active_unit, Side).side],
                                try_component(self.active_unit, Move).walk_mask):
            match sign:
                case '0':
                    continue
                case '1':
                    new = try_component(self.active_unit, core.Position).position + vector
                    if new not in settings.EFEN['PIECES'].keys() and new in settings.EFEN['NUCLEUS'].keys():
                        try_component(settings.EFEN['NUCLEUS'][new], render.Nucleus).enabled = True
                case 'I':
                    count = 1
                    new = try_component(self.active_unit, core.Position).position + vector
                    while new not in settings.EFEN['PIECES'].keys() and new in settings.EFEN['NUCLEUS'].keys():
                        try_component(settings.EFEN['NUCLEUS'][new], render.Nucleus).enabled = True
                        count += 1
                        new = try_component(self.active_unit, core.Position).position + vector * count

    def walk(self, new):
        old_pos = try_component(self.active_unit, core.Position).position
        new_pos = try_component(new, core.Position).position
        try_component(self.active_unit, core.Position).position = new_pos
        settings.EFEN['PIECES'][new_pos] = settings.EFEN['PIECES'].pop(old_pos)
        self.select(None)

    def attack_generate(self):
        if None == self.active_unit:
            return
        for vector, sign in zip(STEPS[try_component(self.active_unit, Side).side],
                                try_component(self.active_unit, Move).attack_mask):
            match sign:
                case '0':
                    continue
                case '1':
                    new = try_component(self.active_unit, core.Position).position + vector
                    if new in settings.EFEN['PIECES'].keys():
                        add_component(settings.EFEN['PIECES'][new], UnderAttack())
                case 'I':
                    count = 1
                    new = try_component(self.active_unit, core.Position).position + vector
                    while new in settings.EFEN['NUCLEUS'].keys():
                        if new in settings.EFEN['PIECES'].keys():
                            add_component(settings.EFEN['PIECES'][new], UnderAttack())
                            break
                        else:
                            count += 1
                            new = try_component(self.active_unit, core.Position).position + vector * count

    def attack(self, new):
        old_pos = try_component(self.active_unit, core.Position).position
        new_pos = try_component(new, core.Position).position
        add_component(new, Captured())
        try_component(self.active_unit, core.Position).position = new_pos
        settings.EFEN['PIECES'][new_pos] = settings.EFEN['PIECES'].pop(old_pos)
        self.select(None)

    def destroy_generate(self):
        if None == self.active_unit:
            return
        for vector, sign in zip(STEPS[try_component(self.active_unit, Side).side],
                                try_component(self.active_unit, Move).destroy_mask):
            match sign:
                case '0':
                    continue
                case '1':
                    new = try_component(self.active_unit, core.Position).position + vector
                    if new in settings.EFEN['PIECES'].keys():
                        add_component(settings.EFEN['PIECES'][new], UnderDestroy())
                case 'I':
                    count = 1
                    new = try_component(self.active_unit, core.Position).position + vector
                    while new in settings.EFEN['NUCLEUS'].keys():
                        if new in settings.EFEN['PIECES'].keys():
                            add_component(settings.EFEN['PIECES'][new], UnderDestroy())
                            break
                        else:
                            count += 1
                            new = try_component(self.active_unit, core.Position).position + vector * count

    def destroy(self, new):
        new_pos = try_component(new, core.Position).position
        add_component(new, Destroyed())
        settings.EFEN['PIECES'].pop(new_pos)
        self.select(None)

    def process(self):
        pass
