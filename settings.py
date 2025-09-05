#
SIDE = [WHITE, BLACK, HOLE] = ['♙', '♟︎', '●']

class Singltone:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singltone, cls).__new__(cls)
        return cls._instance

settings = Singltone()
settings.development_mode = True
settings.GAME = "load"
settings.BoardSize = 2
settings.FEN = dict()
settings.EFEN = dict(
    NUCLEUS = dict(),
    PIECES = dict()
)
settings.active_player = WHITE
settings.active_unit = None