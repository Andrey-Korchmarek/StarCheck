from __init__ import *
from core import Position


@component
class Renderable:
    rendering: Entity = None

class RenderProcessor(Processor):

    def process(self):
        for ent, rend in get_component(Renderable):
            rend.rendering = Entity()

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

    def plus_size(self):
        for ent, [rend, sz] in get_components(Renderable, Size):
            sz.size += 1
            rend.rendering.scale = sz.size

    def minus_size(self):
        for ent, [rend, sz] in get_components(Renderable, Size):
            sz.size -= 1
            rend.rendering.scale = sz.size

    def process(self):
        for ent, [rend, sz] in get_components(Renderable, Size):
            rend.rendering.scale = sz.size
        set_handler("plus_size", self.plus_size)
        set_handler("minus_size", self.minus_size)

@component
class Colour:
    colour: Color = color.white

class ColourProcessor(Processor):

    def process(self):
        for ent, [rend, clr] in get_components(Renderable, Colour):
            rend.rendering.color = clr.colour

@component
class Transparent:
    alpha = 0.2

class TransparentProcessor(Processor):

    def process(self):
        for ent, [rend, trn] in get_components(Renderable, Transparent):
            rend.rendering.alpha = trn.alpha

def keyboard_input(key):
    global GAME
    combined_key = input_handler.get_combined_key(key)
    if combined_key == 'shift+escape':
        quit()
        GAME = 0
        return
    if key == 'e':
        dispatch_event("plus_size")
    if key == 'q':
        dispatch_event("minus_size")
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
    def __init__(self, development):
        self.render = Ursina(development_mode=development)

    def systemize(self):
        self.add_processor(RenderProcessor(), 5)
        self.add_processor(RenderPositionProcessor(), 4)
        self.add_processor(ModelProcessor(), 3)
        self.add_processor(SizeProcessor(), 0)
        self.add_processor(ColourProcessor(), 2)
        self.add_processor(TransparentProcessor(), 1)
        #window.fullscreen = True
        EditorCamera()
        input_handler.input = keyboard_input

#border = create_entity(Renderable(), Position(), Model(), Size(), Colour())

if __name__ == '__main__':
    system_manager()
    while GAME != 0:
        match GAME:
            case 1:
                print("Game is paused.")
                continue
            case 2:
                systemize()
                continue
            case _:
                print("Somthing wrong.")
                continue
