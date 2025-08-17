from dataclasses import dataclass as component
from system import *
from ursina import *

global GAME
GAME = True

from test import TestProcessor
from render import RenderSystem

def system_manager(dev_mode=True, test_proc=False, render_sys=True):
    def processor_manager():
        if test_proc:
            global test_processor
            test_processor = TestProcessor()
            add_processor(test_processor)
    processor_manager()
    if render_sys:
        global render_system
        render_system = RenderSystem()
        add_system(render_system)