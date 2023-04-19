from ursina import Button, color, Func
from __init__ import PIECE_SYMBOLS, WHITE


class _Catched(object):
    def __init__(self, sign, xb, xt, y, clr):
        self._sign = sign
        self._count = 0
        self.unpressed_color = clr
        self.button = Button(self._sign, scale=.05, color=clr, text_color=color.black, x=xb, y=y)
        self.text_field = Button('0', scale=.05, color=color.white, pressed_color=color.white, text_color=color.black, x=xt, y=y)

    def get_name(self):
        return self._sign
    def get_count(self):
        return self._count
    def set_count(self, delta):
        self._count += delta
        self.text_field.text = str(self._count)

class _Panel(object):
    def __init__(self, side):
        start_y = 0.46
        button_x = -0.86 if (side == WHITE) else 0.86
        text_x = -0.81 if (side == WHITE) else 0.81
        scale = 0.05
        b_color = color.peach if (side == WHITE) else color.cyan
        string = ''.join(PIECE_SYMBOLS[1:]).upper()
        self.table = [_Catched('None', button_x, text_x, start_y, b_color), ] +\
                     [_Catched(s, button_x, text_x, start_y - scale * i, b_color) for s, i in zip(string, range(1, 19))]
        self.table[0].text_field.text = '-'
        self.selection = self.table[0]
        self.selection.button.on_click = self.clean_selection
        for el in self.table[1:]:
            el.button.on_click = Func(self.select, el)

    def select(self, b: _Catched):
        if self.selection == b:
            return
        else:
            self.selection.button.color = self.selection.unpressed_color
            self.selection = b
            self.selection.button.color = self.selection.button.pressed_color
    def clean_selection(self):
        self.selection.button.color = self.selection.unpressed_color
        self.selection = self.table[0]

class Player(object):
    def __init__(self, side):
        self.side = side
        self.catching_units = _Panel(side)
    def set_collider(self, value: bool):
        self.catching_units.clean_selection()
        for el in self.catching_units.table:
            el.button.collider = 'box' if value else None

    def add_capture(self, form: int):
        self.catching_units.table[form].set_count(1)

    def drop_capture(self):
        form = self.catching_units.table.index(self.catching_units.selection)
        self.catching_units.table[form].set_count(-1)
        self.catching_units.clean_selection()
        return form

    def generate_units(self, boardSize):
        from Unit import Piece
        if 0 == boardSize or 1 == boardSize:
            return []
        elif 2 == boardSize:
            return [Piece((2, 2, 2) if (self.side == WHITE) else (-2, -2, -2), 18, self.side), ]
        elif 3 == boardSize:
            if (self.side == WHITE):
                pls = {(2, 6, -2), (6, -2, 2), (6, 2, -2), (2, -2, 6), (2, 2, 6), (4, 4, 0), (4, 0, 8), (4, 0, 4),
                       (-2, 6, 2), (6, 2, 2), (0, 4, 8), (8, 0, 4), (8, 4, 0), (-2, 2, 6), (2, 6, 2),  (4, 8, 0),
                       (0, 8, 4), (0, 4, 4)}
                return [Piece((4, 4, 4), 18, self.side), Piece((2, 2, 2), 17, self.side),
                        Piece((4, 4, 0), 12, self.side), Piece((4, 0, 4), 11, self.side), Piece((0, 4, 4), 10, self.side),
                        Piece((4, 0, 8), 6, self.side), Piece((0, 4, 8), 5, self.side), Piece((8, 0, 4), 4, self.side),
                        Piece((8, 4, 0), 3, self.side), Piece((4, 8, 0), 2, self.side), Piece((0, 8, 4), 1, self.side),
                        ]
            else:
                return [Piece((-4, -4, -4), 18, self.side), Piece((-2, -2, -2), 16, self.side),
                        Piece((-4, -4, 0), 12, self.side), Piece((-4, 0, -4), 11, self.side), Piece((0, -4, -4), 10, self.side),
                        Piece((-4, 0, -8), 6, self.side), Piece((0, -4, -8), 5, self.side), Piece((-8, 0, -4), 4, self.side),
                        Piece((-8, -4, 0), 3, self.side), Piece((-4, -8, 0), 2, self.side), Piece((0, -8, -4), 1, self.side),]
        else:
            return []

if __name__ == '__main__':
    print("This is not app")