import itertools
from GameBoard import *
from Сalculations import *
from ursina import *
from Unit import *
from collections import namedtuple
from __init__ import *
from Player import *



if __name__ == '__main__':
    print(VECTORS.id((16, 4, 4)))
    """
    app = Ursina(fullscreen=True, borderless=True)
    plus = Entity(
            model='sphere',
            texture='textures/' + "A+X_398x192.png",
            collision=True,
            collider='sphere',
            position=Vec3(2, 2, 2),
            scale=1.5,
            #billboard=True,
        )
    minus = Entity(
            model='sphere',
            texture='textures/' + "A+X_398x192.png",
            collision=True,
            collider='sphere',
            position=Vec3(-2, -2, -2),
            scale=1.5,
            #billboard=True,
        )
    center = Entity(model="models/custom_cube.obj", texture="textures/rubik_texture.png")
    plus.rotate((-30, 45, 0))
    minus.rotate((30, -135, 180))
    count = Vec3(0,0,0)
    def input(key):

        global count
        i = 15
        if key == 'x':
            minus.rotate((0, i, 0))
            count.y += i
            print(count)
        if key == 'c':
            minus.rotate((0, 0, i))
            count.z += i
            print(count)
        if key == 'space':
            print(held_keys['z'])
        if key == 'left control':
            print(held_keys['spase'])
        if key == 'escape':
            application.quit()
    EditorCamera()
    app.run()
    """