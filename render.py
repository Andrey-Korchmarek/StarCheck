import system
from __init__ import *
from ursina import Keys
from core import Position

@component
class Renderable:
    rendering: ursina.Entity = None

class RenderProcessor(esper.Processor):

    def process(self):
        spisok = esper.get_component(Renderable)
        print(len(spisok))
        for ent, rend in spisok:
            rend.rendering = ursina.Entity()

class RenderPositionProcessor(esper.Processor):

    def process(self):
        for ent, [rend, pos] in esper.get_components(Renderable, Position):
            rend.rendering.position = pos.position

@component
class Hidden:
    hidden: bool = True

class HiddenProcessor(esper.Processor):

    def change_visible(self):
        for ent, [rend, hide] in esper.get_components(Renderable, Hidden):
            hide.hidden = not hide.hidden
            #print(ent, rend.rendering)
            rend.rendering.visible = not hide.hidden

    def process(self):
        for ent, [rend, hide] in esper.get_components(Renderable, Hidden):
            #print(ent)
            rend.rendering.visible = not hide.hidden
        esper.set_handler("change visible", self.change_visible)

@component
class Model:
    model: str = 'sphere'

class ModelProcessor(esper.Processor):

    def process(self):
        for ent, [rend, mod] in esper.get_components(Renderable, Model):
            rend.rendering.model = mod.model

@component
class Size:
    size: int = 1


class SizeProcessor(esper.Processor):

    def plus_size(self):
        for ent, [rend, sz] in esper.get_components(Renderable, Size):
            sz.size += 1
            rend.rendering.scale = sz.size

    def minus_size(self):
        for ent, [rend, sz] in esper.get_components(Renderable, Size):
            sz.size -= 1
            rend.rendering.scale = sz.size

    def process(self):
        for ent, [rend, sz] in esper.get_components(Renderable, Size):
            rend.rendering.scale = sz.size
        esper.set_handler("plus_size", self.plus_size)
        esper.set_handler("minus_size", self.minus_size)

@component
class Colour:
    colour: ursina.Color = ursina.color.white

class ColourProcessor(esper.Processor):

    def process(self):
        for ent, [rend, clr] in esper.get_components(Renderable, Colour):
            rend.rendering.color = clr.colour

@component
class Transparent:
    alpha = 0.2

class TransparentProcessor(esper.Processor):

    def process(self):
        for ent, [rend, trn] in esper.get_components(Renderable, Transparent):
            rend.rendering.alpha = trn.alpha

def keyboard_input(key):
    global GAME
    combined_key = ursina.input_handler.get_combined_key(key)
    if combined_key == 'shift+escape':
        quit()
    if key == 'e':
        esper.dispatch_event("plus_size")
    if key == 'q':
        esper.dispatch_event("minus_size")
    if key == 'tab':
        esper.dispatch_event("change visible")
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
        ursina.held_keys[key[:-3]] = 0
    else:
        ursina.held_keys[key] = 1

class RenderSystem(system.System):
    def __init__(self, development):
        self.render = ursina.Ursina(development_mode=development)

    def systemize(self):
        self.add_processor(RenderProcessor(), 5)
        self.add_processor(RenderPositionProcessor(), 4)
        self.add_processor(ModelProcessor(), 3)
        self.add_processor(SizeProcessor(), 0)
        self.add_processor(ColourProcessor(), 2)
        self.add_processor(TransparentProcessor(), 1)
        self.add_processor(HiddenProcessor(), 4)
        self.process()
        #window.fullscreen = True
        ursina.EditorCamera()
        ursina.input_handler.input = keyboard_input
        self.render.run()

if __name__ == '__main__':
    init()
    system.systemize()