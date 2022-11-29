from ursina import *

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.fullscreen = True
        # Entity(model='models/xyz_axis')
        verts = ((0, 0, 0), (1, 0, 0), (.5, 1, 0), (-.5, 1, 0))
        tris = (1, 2, 0, 2, 3, 0)
        uvs = ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
        norms = ((0, 0, -1),) * len(verts)
        colors = (color.red, color.blue, color.lime, color.black)

        e = Entity(model=Mesh(vertices=verts, triangles=tris, uvs=uvs, normals=norms, colors=colors), scale=2)
        verts = (Vec3(0, 0, 0), Vec3(0, 1, 0), Vec3(1, 1, 0), Vec3(2, 2, 0), Vec3(0, 3, 0), Vec3(-2, 3, 0))
        tris = ((0, 1), (3, 4, 5))

        lines = Entity(model=Mesh(vertices=verts, triangles=tris, mode='line', thickness=4), color=color.cyan, z=-1)
        points = Entity(model=Mesh(vertices=verts, mode='point', thickness=.05), color=color.red, z=-1.01)

        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.load_game()

    def load_game(self):
        pass

    def palette(self):
        Entity(model='models/Truncated_octahedron-Solid', position=Vec3(0, 0, 0), color=color.black)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(0, 4, 0), color=color.blue)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(4, 0, 0), color=color.blue)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(0, 0, 4), color=color.blue)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(0, -4, 0), color=color.blue)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(-4, 0, 0), color=color.blue)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(0, 0, -4), color=color.blue)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(2, 2, 2), color=color.green)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(-2, 2, -2), color=color.green)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(-2, -2, 2), color=color.green)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(2, -2, -2), color=color.green)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(-2, -2, -2), color=color.red)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(2, -2, 2), color=color.red)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(-2, 2, 2), color=color.red)
        Entity(model='models/Truncated_octahedron-Cut', position=Vec3(2, 2, -2), color=color.red)

    def input(self, key):
        super().input(key)

if __name__ == '__main__':
    print("This is not app!")