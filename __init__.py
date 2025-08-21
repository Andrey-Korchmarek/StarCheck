from dataclasses import dataclass as component
from system import *
from ursina import *

global GAME
GAME = 2

from test import TestProcessor
from render import RenderSystem
from gameboard import GameboardSystem

def system_manager(dev_mode=True, test_proc=False, render_sys=True, board_sys = True):
    def processor_manager():
        if test_proc:
            global test_processor
            test_processor = TestProcessor()
            add_processor(test_processor)
    processor_manager()
    if render_sys:
        global render_system
        render_system = RenderSystem(dev_mode)
        add_system(render_system, 0)
    if board_sys:
        global gameboard_system
        gameboard_system = GameboardSystem()
        add_system(gameboard_system, 3)