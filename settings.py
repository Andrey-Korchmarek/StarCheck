#
class Singltone:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singltone, cls).__new__(cls)
        return cls._instance

settings = Singltone()
settings.GAME = "load"
settings.BoardSize = 4