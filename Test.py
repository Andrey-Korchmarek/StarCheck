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
    center = Entity(position = (0,0,0), color = color.black, visible = True, ignore_input = True, model = 'sphere', collision = True, collider = 'sphere')
    source = Entity(position = (4,4,4), color = color.peach, visible = True, ignore_input = True, model = 'sphere', collision = True, collider = 'sphere')
    steps = [
        (
            Entity(position=source.position + Vec3(x), color=color.white, visible=True, ignore_input=True, model='sphere', collision=True, collider='sphere'),
            Entity(position=source.position - Vec3(x), color=color.white, visible=True, ignore_input=True, model='sphere', collision=True, collider='sphere'),
        )
        for x in VECTORS
    ]
    pauns = ''
    anomales = []
    for pl, mn in steps:
        if distance(pl, center) < distance(mn, center):
            pauns += '10'
        elif distance(pl, center) > distance(mn, center):
            pauns += '01'
        else:
            pauns += '!!'
            anomales.append(pl)
            anomales.append(mn)
    print(len(pauns))
    print('pauns = "',pauns, '"')
    for el in anomales:
        el.color = color.red
        print(el.position - source.position)
    def input(key):
        global count
        if key == 'space':
            pass
        if key == 'escape':
            application.quit()
    EditorCamera()
    app.run()