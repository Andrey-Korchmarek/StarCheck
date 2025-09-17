#
class Singltone:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singltone, cls).__new__(cls)
        return cls._instance

settings = Singltone()

settings.development_mode = False
settings.rendering = True
settings.GAME = "load"
settings.BoardSize = 2
settings.FEN = dict()
settings.EFEN = dict(
    NUCLEUS = dict(),
    PIECES = dict()
)
settings.active_player: str = None
settings.active_unit: int = None