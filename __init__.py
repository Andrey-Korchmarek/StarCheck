from settings import settings
from dataclasses import dataclass as component
from esper import *
from system import *
from ursina import *

import gameboard
import render

def init(test_proc=False, render_sys=True):
    gameboard.create_gameboard(settings.BoardSize)
    if render_sys:
        add_processor(render.RenderProcessor(), 0)
