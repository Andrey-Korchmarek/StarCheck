from settings import settings
from dataclasses import dataclass as component
import esper
import system
import ursina
from ursina import Vec3, color

import gameboard
from test import TestProcessor
from render import RenderSystem

esper.set_handler("create gameboard", gameboard.create_gameboard)

def init(dev_mode=True, test_proc=False, render_sys=True):
    esper.dispatch_event("create gameboard")
    if render_sys:
        global render_system
        render_system = RenderSystem(dev_mode)
        system.add_system(render_system, 0)