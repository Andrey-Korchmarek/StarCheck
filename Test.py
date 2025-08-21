from __init__ import *

@component
class TestComponent:
    msg: str = "Default message."

class TestProcessor(esper.Processor):

    def process(self):
        for ent, [tst] in esper.get_components(TestComponent):
            print(tst.msg)

if __name__ == '__main__':
    test1 = esper.create_entity()
    esper.add_component(test1, TestComponent("Message test"))
    test2 = esper.create_entity()
    esper.add_component(test2, TestComponent())
    system_manager(test_proc=True)
    system.systemize()