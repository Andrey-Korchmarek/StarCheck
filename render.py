from __init__ import *
import pieces
import core


class Renderable:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = dict(position=Vec3(0, 0, 0),
                           model="sphere",
                           texture=None,
                           color=color.gray,
                           alpha=1.0,
                           rotation=(0, 0, 0),
                           scale=1,
                           visible=True,
                           collider=None,
                           collision=False,
                           on_click=todo_nothing,
                           on_double_click=todo_nothing,
                           enabled=True)
        self.kwargs.update(kwargs)
        self.rendering: Entity = None


@component
class Cell:
    visible: bool = False


@component
class Nucleus:
    enabled = False


@component
class Size:
    size: int = 1


class RenderProcessor(Processor):
    def __init__(self):
        self.render = Ursina(development_mode=settings.development_mode)
        for ent, rend in get_component(Renderable):
            rend.rendering = Entity(position=rend.kwargs.get('position'),
                                    model=rend.kwargs.get('model'),
                                    texture=rend.kwargs.get('texture'),
                                    color=rend.kwargs.get('color'),
                                    alpha=rend.kwargs.get('alpha'),
                                    rotation=rend.kwargs.get('rotation'),
                                    scale=rend.kwargs.get('scale'),
                                    visible=rend.kwargs.get('visible'),
                                    collider=rend.kwargs.get('collider'),
                                    collision=rend.kwargs.get('collision'),
                                    on_click=rend.kwargs.get('on_click'),
                                    on_double_click=rend.kwargs.get('on_double_click'),
                                    enabled=rend.kwargs.get('enabled'))
        set_handler("change board visible", self.showorhide_board)
        set_handler("plus_size", self.plus_size)
        set_handler("minus_size", self.minus_size)
        set_handler("change selection", self.change_selection)
        input_handler.input = self.keyboard_input
        #window.fullscreen = True
        EditorCamera()

    def showorhide_board(self):
        for ent, [rend, hide] in get_components(Renderable, Cell):
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

    def change_selection(self):
        for ent, nucl in get_component(Nucleus):
            nucl.enabled = False
        for ent, wal in get_component(pieces.Walkable):
            remove_component(ent, pieces.Walkable)
        for ent, att in get_component(pieces.UnderAttack):
            remove_component(ent, pieces.UnderAttack)
        for ent, des in get_component(pieces.UnderDestroy):
            remove_component(ent, pieces.UnderDestroy)
        for ent, [rend, na] in get_components(Renderable, pieces.Nonactive):
            rend.rendering.color = na.color
        for ent, [rend, act, sd] in get_components(Renderable, pieces.Selected, pieces.Side):
            if settings.active_player == sd.side:
                rend.rendering.color = act.active
            else:
                rend.rendering.color = act.nonactive

    def keyboard_input(self, key):
        combined_key = input_handler.get_combined_key(key)
        if combined_key == 'shift+escape':
            settings.GAME = "stop"
        if key == 'e':
            esper.dispatch_event("plus_size")
        if key == 'q':
            esper.dispatch_event("minus_size")
        if key == 'tab':
            esper.dispatch_event("change board visible")
        if key == 'w':
            dispatch_event("walk needed")
        if key == 's':
            dispatch_event("select", None)
        if key == 'a':
            dispatch_event("attack needed")
        if key == 'd':
            dispatch_event("destroy needed")
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
        for ent, [rend, nuc] in get_components(Renderable, Nucleus):
            rend.rendering.on_double_click = todo_nothing
            rend.rendering.enabled = nuc.enabled
        for ent, [rend, pic] in get_components(Renderable, pieces.Piece):
            if (not has_component(ent, pieces.Selected)
                    and not has_component(ent, pieces.UnderAttack)
                    and not has_component(ent, pieces.UnderDestroy)):
                rend.rendering.color = pic.color
                rend.rendering._on_click = lambda new=ent: dispatch_event("select", new)
                rend.rendering.on_double_click = todo_nothing
        for ent, [rend, wal] in get_components(Renderable, pieces.Walkable):
            if None != settings.active_unit:
                if settings.active_player == try_component(settings.active_unit, pieces.Side).side:
                    rend.rendering.color = wal.active
                    rend.rendering.on_double_click = lambda new=ent: dispatch_event("walk", new)
                    rend.rendering.enabled = True #TODO Заменить этот костыль чем-то более элегантным
                else:
                    rend.rendering.color = wal.nonactive
                    rend.rendering.enabled = True #TODO Заменить этот костыль чем-то более элегантным
        for ent, [rend, att] in get_components(Renderable, pieces.UnderAttack):
            if None != settings.active_unit:
                if settings.active_player == try_component(settings.active_unit, pieces.Side).side:
                    rend.rendering.color = att.active
                    rend.rendering._on_click = todo_nothing
                    rend.rendering.on_double_click = lambda new=ent: dispatch_event("attack", new)
                else:
                    rend.rendering.color = att.nonactive
        for ent, [rend, des] in get_components(Renderable, pieces.UnderDestroy):
            if None != settings.active_unit:
                if settings.active_player == try_component(settings.active_unit, pieces.Side).side:
                    rend.rendering.color = des.active
                    rend.rendering._on_click = todo_nothing
                    rend.rendering.on_double_click = lambda new=ent: dispatch_event("destroy", new)
                else:
                    rend.rendering.color = des.nonactive
        for ent, [rend, cap] in get_components(Renderable, pieces.Captured):
            rend.rendering.disable()
        for ent, [rend, cap] in get_components(Renderable, pieces.Destroyed):
            rend.rendering.disable()
        for ent, [rend, pos, pic] in get_components(Renderable, core.Position, pieces.Piece):
            rend.rendering.position = pos.position
        self.render.step()


if __name__ == '__main__':
    pass
