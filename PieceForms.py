from __init__ import  *

"""
Пешки - фигуры, чей ход отличатся для передвижения, захвата и выстрела,
а ходят они только на 1 клетку и только вперёд, всего их 6 видов.
"""

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

    # Пешка №3, передвигается диагонально, захватывает триагонально, стреляет ортогонально
}



class PieceForm:
    def __init__(self, id):
        if id in pieceFormsValues.keys():
            self.symbol = pieceFormsValues[id]["symbol"]
            self.name = pieceFormsValues[id]["name"]
            self.texture = 'textures/' + pieceFormsValues[id]["texture"]
            self.walk_mask = pieceFormsValues[id]["walk_mask"]
            self.attack_mask = pieceFormsValues[id]["attack_mask"]
            self.destroy_mask = pieceFormsValues[id]["destroy_mask"]
        else:
            # TODO: add exception
            pass