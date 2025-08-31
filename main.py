from __init__ import *
import gameboard
import render
import pieces

def init(test_proc=False, render_sys=True):
    gameboard.create_gameboard(settings.BoardSize)
    pieces.create_start_pieces(settings.BoardSize)
    add_processor(pieces.MovementProcessor(), 1)
    if render_sys:
        add_processor(render.RenderProcessor(), 0)
    settings.GAME = "run"

while settings.GAME:
    match settings.GAME:
        case "load":
            init()
        case "run":
            process()
        case "stop":
            quit()

if __name__ == '__main__':
    pass