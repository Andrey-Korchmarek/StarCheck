from ursina import *

class Figure(object):
    def __init__(self, code: str, begin: Vec3):
        """Constructor"""
        vectors = [
               (4, 0, 0), (0, 4, 0), (0, 0, 4), #square faces
               (2, 2, 2), (2, 2, -2), (2, -2, 2), (-2, 2, 2), #hexagonal faces
               (4, 4, 0), (4, 0, 4), (0, 4, 4), #near hex-hex edges
               (4, -4, 0), (-4, 0, 4), (0, 4, -4), #distant hex-hex edges
               (16, 4, 4), (16, -4, 4), (16, -4, -4), (16, 4, -4), #square-hex edges X
               (4, 16, 4), (-4, 16, 4), (-4, 16, -4), (4, 16, -4), #square-hex edges Y
               (4, 4, 16), (4, -4, 16), (-4, -4, 16), (-4, 4, 16), #square-hex edges Z
               (8, 4, 0), (8, 0, 4), (8, -4, 0), (8, 0, -4), #vertexes X
               (0, 8, 4), (4, 8, 0), (0, 8, -4), (-4, 8, 0), #vertexes Y
               (4, 0, 8), (0, 4, 8), (-4, 0, 8), (0, -4, 8), #vertexes Z
        ]
        codes = dict(S=1, O=1, D=1, H=1, X=1, W=1, L=1, Z=1, G=1)
        self.position = begin

    def move(self):
        pass

    def capture(self):
        pass

    def kill(self):
        pass

if __name__ == '__main__':
    print("This is not app!")
    app = Ursina()
    vectors = [(0, 0, 0),
               (4, 0, 0), (0, 4, 0), (0, 0, 4), #square faces
               (2, 2, 2), (2, 2, -2), (2, -2, 2), (-2, 2, 2), #hexagonal faces
               (4, 4, 0), (4, 0, 4), (0, 4, 4), #near hex-hex edges
               (4, -4, 0), (-4, 0, 4), (0, 4, -4), #distant hex-hex edges
               (16, 4, 4), (16, -4, 4), (16, -4, -4), (6, 4, -4), #square-hex edges X
               (4, 16, 4), (-4, 16, 4), (-4, 16, -4), (4, 16, -4), #square-hex edges Y
               (4, 4, 16), (4, -4, 16), (-4, -4, 16), (-4, 4, 16), #square-hex edges Z
               (8, 4, 0), (8, 0, 4), (8, -4, 0), (8, 0, -4), #vertexes X
               (0, 8, 4), (4, 8, 0), (0, 8, -4), (-4, 8, 0), #vertexes Y
               (4, 0, 8), (0, 4, 8), (-4, 0, 8), (0, -4, 8), #vertexes Z
               ]
    vectors2 = [(0, 0, 0), (8, 4, 0), (8, 0, 4), (8, -4, 0), (8, 0, -4)]
    color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
    turns = [Entity(model='models/Solid', position=pos, color=color_calc[sum(pos) % 8]) for pos in vectors]
    one_by_one = iter(turns)
    result = list()
    prev = next(one_by_one)
    prev.color = color.black
    def input(key):
        global prev
        global result
        if key == 'space':
            prev.color = color.black
            prev = next(one_by_one)
            prev.color = color.red
        if key == 'd':
            prev.visible = False
        if key == 'p':
            x, y, z = prev.position
            result.append((int(x), int(y), int(z)))
            prev.color = color.blue
            print(result)

    EditorCamera()
    app.run()