from __init__ import *

class RenderSystem(System):

    def process(self):
        global render
        render=Ursina()
        for ent, [rend] in get_components(Renderable):
            rend.rendering = Entity()
        for ent, [rend, pos] in get_components(Renderable, Position):
            rend.rendering.position = pos.position
        for ent, [rend, mod] in get_components(Renderable, Model):
            rend.rendering.model = mod.model
        window.fullscreen=True
        EditorCamera()
        global render
        render.run()