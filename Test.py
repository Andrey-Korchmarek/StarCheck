from GameBoard import *
from ursina import *
from Unit import *

if __name__ == '__main__':
    print(len(FORMS_WALK_VECTORS))
    app = Ursina()
    def update():
        for key, value in held_keys.items():
            if value != 0:
                print(key, value)
    app.run()