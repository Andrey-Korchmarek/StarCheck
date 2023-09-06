from __init__ import *
from ursina import Vec3

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
        "symbol": None,
        "name": None,
        "texture": None,
        "walk_mask": ''.zfill(92),
        "attack_mask": ''.zfill(92),
        "destroy_mask": ''.zfill(92),
    },
    # Пешка №1, передвигается ортогонально, захватывает диагонально, стреляет триагонально
    1: {
        "symbol": 'a',
        "name": "warrior",
        "texture": "ladybug",
        "walk_mask": P_means_PAUNS[:14] + ''.zfill(92 - 14),
        "attack_mask": ''.zfill(25) + P_means_PAUNS[25:50] + ''.zfill(92 - 50),
        "destroy_mask": ''.zfill(50) + P_means_PAUNS[50:74] + ''.zfill(92 - 74),
    },
    # Пешка №2, передвигается ортогонально, захватывает триагонально, стреляет диагонально
    2: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Пешка №3, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    3: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Пешка №4, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    4: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Пешка №5, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    5: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Пешка №6, передвигается диагонально, захватывает триагонально, стреляет ортогонально
    6: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Ладья, передвигается, захватывает и стреляет ортогонально на любое число клеток
    7: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Слон, передвигается, захватывает и стреляет диагонально на любое число клеток
    8: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Рух, передвигается, захватывает и стреляет триагонально на любое число клеток
    9: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Конь, передвигается прыжками на комбинацию из движений на 1 клетку в каждом направлении
    # на расстояние ближайших к Ферзю клеток, которые тот не может атаковать
    10: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Ферзь, передвигается, захватывает и стреляет на любое число клеток в любом одном направлении
    11: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
    # Король, передвигается, захватывает и стреляет на 1 клетку в любом одном направлении
    # Когда любая фигура противника получает возможность захватить или застрелить Короля, его Игроку объявляется ШАХ
    # Когда Король захвачен или застрелен игра заканчивается поражением Игрока, владевшего этим королём
    12: {
        "symbol": -1,
        "name": -1,
        "texture": -1,
        "walk_mask": -1,
        "attack_mask": -1,
        "destroy_mask": -1,
    },
}

class PieceForm:
    def __init__(self, index):
        if index in pieceFormsValues.keys():
            self.symbol = pieceFormsValues[index]["symbol"]
            self.name = pieceFormsValues[index]["name"]
            self.texture = 'textures/' + pieceFormsValues[index]["texture"]
            self.walk_mask = pieceFormsValues[index]["walk_mask"]
            self.attack_mask = pieceFormsValues[index]["attack_mask"]
            self.destroy_mask = pieceFormsValues[index]["destroy_mask"]
        else:
            # TODO: add exception
            pass

startingPositionOfPieces = {
    3: {
        WHITE: [Piece(Vec3(x), formId, WHITE) for x, formId in zip(
            [(4, 4, 4), (2, 2, 2), (4, 4, 0), (4, 0, 4), (0, 4, 4), (4, 0, 8), (0, 4, 8), (8, 0, 4), (8, 4, 0), (4, 8, 0), (0, 8, 4)],
            [12, 11, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        )
        ],
        BLACK: [Piece(Vec3(x), formId, BLACK) for x, formId in zip(
            [(-4, -4, -4), (-2, -2, -2), (-4, -4, 0), (-4, 0, -4), (0, -4, -4), (-4, 0, -8), (0, -4, -8), (-8, 0, -4),
             (-8, -4, 0), (-4, -8, 0), (0, -8, -4)],
            [12, 11, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        )
        ],
    }
}

def getStartPositionOfPieses(boardSize):
    return startingPositionOfPieces[boardSize]