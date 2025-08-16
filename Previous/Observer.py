from __init__ import  *

class Observer(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Observer, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.cells = set()
        self.pieces = {}
        self.activePlayer = -1
        self. selectedUnit = -1

    def addCells(self, list):
        self.cells.update(list)

    def addPieces(self, color, list):
        if WHITE == color:
            self.white.update(list)
        elif BLACK == color:
            self.black.update(list)
        else:
            pass