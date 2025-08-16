from dataclasses import dataclass as component
from esper import *
del globals()['Processor']
from esper import Processor as System
del globals()['add_processor']
from esper import add_processor as add_system
del globals()['remove_processor']
from esper import remove_processor as remove_system
del globals()['get_processor']
from esper import get_processor as get_system
from ursina import *

from test import TestSystem
from render import RenderSystem

def system_manager(test_sys=False, render_sys=True):
    if test_sys:
        global test_system
        test_system = TestSystem()
        add_system(test_system)
    if render_sys:
        global render_system
        render_system = RenderSystem()
        add_system(render_system)