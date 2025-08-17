from __init__ import *
from core import Position


@component
class Renderable:
    rendering: Entity = None

class RenderPositionProcessor(Processor):

    def process(self):
        for ent, [rend, pos] in get_components(Renderable, Position):
            rend.rendering.position = pos.position

@component
class Model:
    model: str = 'sphere'

class ModelProcessor(Processor):

    def process(self):
        for ent, [rend, mod] in get_components(Renderable, Model):
            rend.rendering.model = mod.model

@component
class Size:
    size: int = 1


class SizeProcessor(Processor):

    def process(self):
        pass

@component
class Color:
    color = color.white

class ColorProcessor(Processor):

    def process(self):
        for ent, [rend, clr] in get_components(Renderable, Color):
            rend.rendering.color = clr.color

def keyboard_input(key):
    global GAME
    combined_key = input_handler.get_combined_key(key)
    if combined_key == 'shift+escape':
        quit()
        GAME = False
    if key == 'e':
        for ent, [rend, sz] in get_components(Renderable, Size):
            sz.size += 1
            rend.rendering.scale = sz.size
    if key == 'q':
        for ent, [rend, sz] in get_components(Renderable, Size):
            sz.size -= 1
            rend.rendering.scale = sz.size
    if key == 'w':
        pass
    if key == 's':
        pass
    if key == 'a':
        pass
    if key == 'd':
        pass
    #####
    if key.endswith('hold') or key == Keys.scroll_down or key == Keys.scroll_up:
        return

    key = key.replace('mouse down', 'mouse')

    if key.endswith(' up') and key != 'page up' and key != 'gamepad dpad up':
        held_keys[key[:-3]] = 0
    else:
        held_keys[key] = 1

class RenderSystem(System):
    #def __init__(self, development):
    #    self.development = development

    def systemize(self):
        global render
        render = Ursina(development_mode=True)
        for ent, rend in get_component(Renderable):
            rend.rendering = Entity()
        self.add_processor(RenderPositionProcessor())
        self.add_processor(ModelProcessor())
        self.add_processor(ColorProcessor())
        self.process()
        #window.fullscreen = True
        EditorCamera()
        input_handler.input = keyboard_input
        render.step()

border = create_entity(Renderable(), Position(), Model(), Size(), Color())

if __name__ == '__main__':
    system_manager()
    while GAME:
        systemize()
