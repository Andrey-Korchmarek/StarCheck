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

class RenderSystem(System):
    def __init__(self, development):
        self.development = development

    def process(self):
        global render
        render=Ursina(development_mode=self.development)
        for ent, [rend] in get_components(Renderable):
            rend.rendering = Entity()
        for ent, [rend, pos] in get_components(Renderable, Position):
            rend.rendering.position = pos.position
        for ent, [rend, mod] in get_components(Renderable, Model):
            rend.rendering.model = mod.model
        EditorCamera()
        def keyboard_input(key):
            combined_key = input_handler.get_combined_key(key)
            if combined_key == 'shift+escape':
                quit()
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

if __name__ == '__main__':
    border = create_entity(Renderable(), Position(), Model())
    system_manager(dev_mode=True)
    process()

    pos = Vec3(1, 2, 3)
    print(pos.z)