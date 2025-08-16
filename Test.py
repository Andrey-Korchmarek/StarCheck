from __init__ import *

@component
class Position:
    position: Vec3 = Vec3(0, 0, 0)

@component
class Size:
    size: float = 1.0

@component
class Model:
    model: str = 'sphere'

@component
class Renderable:
    rendering: Entity = None

border = create_entity(Renderable(), Position(), Model())


@component
class TestComponent:
    msg: str = "Default message."

test1 = create_entity()
add_component(test1, TestComponent("Message test"))
test2 = create_entity()
add_component(test2, TestComponent())

class TestSystem(System):

    def process(self):
        for ent, [tst] in get_components(Renderable):
            print(tst.msg)

if __name__ == '__main__':
    system_manager(test_sys=True)
    process()