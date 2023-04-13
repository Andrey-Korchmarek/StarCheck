import itertools
from GameBoard import *
from Сalculations import *
from ursina import *
from Unit import *
from collections import namedtuple
from __init__ import *
from Player import *



if __name__ == '__main__':
    app = Ursina(fullscreen=True, borderless=True)
    #s = "AEFYMVNITHXWLZGDOS"
    #b = [Button(a, scale=.05, color=color.peach, text_color=color.black, x=-0.86, y=(0.46 - 0.05*i)) for a, i in zip(s, range(18))]
    #t = [Button('0', scale=.05, color=color.peach, pressed_color=color.peach, text_color=color.black, x=-0.81, y=(0.46 - 0.05*i)) for i in range(18)]
    p1 = Player(True)
    p2 = Player(False)
    def input(key):
        if key == 'escape':
            application.quit()
    EditorCamera()
    app.run()
    """
    from ursina import Ursina, ButtonGroup

    
    window.fullscreen = True # переводим окно в полноэкранный режим
    #window.width = window.screen_width
    print(window.size)
    window.height = window.screen_resolution[1]
    window_panel = WindowPanel(title='TEST', scale_y = 1, scale_x = 0.2, width=0, y=0, background=color.white)

    window_panel.x = window.left.x + window_panel.width # устанавливаем позицию окна по левой границе экрана

    def input(key):
        if key == 'm':
            window_panel.scale_y = 1
            print(window_panel.scale_y)
        if key == 'n':
            window_panel.scale_y -= 1
            window_panel.y = 0
            print(window_panel.scale_y)

    side = True
    from Player import _Catched
    catching_units = {name: _Catched(name) for name in PIECE_NAMES[1:]}
    #cu = ButtonGroup("A E F Y M V N I T H X W L Z G D O S".split(' '), width=20)
    bg = ButtonGroup(('None', 'x', 'y', 'z'), selected_color=color.red)

    wp = WindowPanel(
        title="side",
        y=0.5,
        x=-0.5,
        scale_y = 0.02,
        color=color.red if side else color.blue,
        content=list(chain(*[[el.button, el.text_field] for el in catching_units.values()])) + [bg, ],
    )
    for el in catching_units.values():
        el.button.on_click = Func(el.set_count, el.get_count() + 1)
    def value_changed():
        if 'z' == bg.value:
            wp.lock = (1, 1, 0)
        elif 'y' == bg.value:
            wp.lock = (1, 0, 1)
        elif 'x' == bg.value:
            wp.lock = (0, 1, 1)
        elif 'None' == bg.value:
            wp.lock = (1, 1, 1)
        else:
            wp.lock = (0, 0, 0)
    bg.on_value_changed = value_changed
    """