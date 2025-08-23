from __init__ import *


class Renderable:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = dict(position=Vec3(0, 0, 0),
                           model="sphere",
                           color=color.white,
                           alpha=1.0,
                           scale=1,
                           visible=True)
        self.kwargs.update(kwargs)
        self.rendering: Entity = None


@component
class Hidden:
    visible: bool = False


@component
class Size:
    size: int = 1


class RenderProcessor(Processor):
    def __init__(self):
        self.render = Ursina(development_mode=settings.development_mode)
        for ent, rend in get_component(Renderable):
            rend.rendering = Entity(position=rend.kwargs.get('position'),
                                    model=rend.kwargs.get('model'),
                                    color=rend.kwargs.get('color'),
                                    alpha=rend.kwargs.get('alpha'),
                                    scale=rend.kwargs.get('scale'),
                                    visible=rend.kwargs.get('visible'))
        set_handler("tab", self.showorhide_board)
        set_handler("plus_size", self.plus_size)
        set_handler("minus_size", self.minus_size)
        input_handler.input = self.keyboard_input
        # window.fullscreen = True
        EditorCamera()

    def showorhide_board(self):
        for ent, [rend, hide] in get_components(Renderable, Hidden):
            hide.visible = not hide.visible
            rend.rendering.visible = hide.visible

    def plus_size(self):
        for ent, [rend, sz] in get_components(Renderable, Size):
            sz.size += 1
            rend.rendering.scale = sz.size

    def minus_size(self):
        for ent, [rend, sz] in get_components(Renderable, Size):
            sz.size -= 1
            rend.rendering.scale = sz.size

    def keyboard_input(self, key):
        combined_key = input_handler.get_combined_key(key)
        if combined_key == 'shift+escape':
            quit()
        if key == 'e':
            esper.dispatch_event("plus_size")
        if key == 'q':
            esper.dispatch_event("minus_size")
        if key == 'tab':
            esper.dispatch_event("tab")
        if key == 'w':
            pass
        if key == 's':
            pass
        if key == 'a':
            pass
        if key == 'd':
            pass
        #####
        #
        #####
        if key.endswith('hold') or key == Keys.scroll_down or key == Keys.scroll_up:
            return

        key = key.replace('mouse down', 'mouse')

        if key.endswith(' up') and key != 'page up' and key != 'gamepad dpad up':
            held_keys[key[:-3]] = 0
        else:
            held_keys[key] = 1

    def process(self):
        self.render.run()

if __name__ == '__main__':
    pass