from settings import settings
from dataclasses import dataclass as component
from esper import *
from system import *
from ursina import *

def todo_nothing():
    pass

import gameboard
import render
import pieces

def init(test_proc=False, render_sys=True):
    gameboard.create_gameboard(settings.BoardSize)
    pieces.create_start_pieces(settings.BoardSize)
    if render_sys:
        add_processor(render.RenderProcessor(), 0)
