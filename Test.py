from __init__ import *

funcs = []

for i in range(5):
    f = lambda: print(i)
    funcs.append(f)

for f in funcs:
    f()








@component
class TestComponent:
    msg: str = "Default message."

class TestProcessor(esper.Processor):

    def process(self):
        for ent, [tst] in esper.get_components(TestComponent):
            print(tst.msg)

if __name__ == '__main__':
    test1 = create_entity()
    add_component(test1, TestComponent("Message test"))
    test2 = create_entity()
    add_component(test2, TestComponent())
    add_processor(TestProcessor())
    process()
