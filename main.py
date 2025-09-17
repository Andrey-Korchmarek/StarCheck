from __init__ import *
import gameboard
import render
import pieces

def init():
    gameboard.create_gameboard(settings.BoardSize)
    pieces.create_start_pieces(settings.BoardSize)
    add_processor(pieces.MovementProcessor(), 1)
    if settings.rendering:
        add_processor(render.RenderProcessor(), 0)
    else:
        pass #TODO Создать систему перемещения фигур без отображения
    settings.GAME = "run"

while True:
    match settings.GAME:
        case "load":
            init()
        case "run":
            process()
        case "stop":
            quit()

if __name__ == '__main__':
    pass