from __init__ import *
from core import Position

@component
class Renderable:
    rendering: Entity = None

@component
class Model:
    model: str = 'sphere'

@component
class Size:
    size: int = 1

@component
class Color:
    color = color.white

class RenderSystem(System):
    def __init__(self, development):
        self.development = development

    def process(self):
        global render
        render = Ursina(development_mode=self.development)
        for ent, rend in get_component(Renderable):
            rend.rendering = Entity()
        for ent, [rend, pos] in get_components(Renderable, Position):
            rend.rendering.position = pos.position
        for ent, [rend, mod] in get_components(Renderable, Model):
            rend.rendering.model = mod.model
        for ent, [rend, clr] in get_components(Renderable, Color):
            rend.rendering.color = clr.color
        #window.fullscreen = True
        EditorCamera()
        def keyboard_input(key):
            combined_key = input_handler.get_combined_key(key)
            if combined_key == 'shift+escape':
                quit()
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
        input_handler.input = keyboard_input
        render.run()

border = create_entity(Renderable(), Position(), Model(), Size(), Color())

if __name__ == '__main__':
    system_manager(dev_mode=True)
    process()
