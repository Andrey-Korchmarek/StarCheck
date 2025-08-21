from typing import Any as _Any

from __init__ import *
from core import Position
from settings import settings
from render import *
from math import sqrt, isclose
from itertools import permutations, product
import numpy as np

# Хранилище параметров усечённого октаэдра: длинна стороны, радиусы вписанной сфер шестиугольников и квадратов,
# радиус полувписанной сферы, радиус описанной сферы, координаты начальной ячейки в генераторе сот
CONSTANTS = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))
NORMALES = [(1,1,1),(2,0,0),(0,2,0),(0,0,2),(1,-1,1),(1,1,-1),(-1,1,1),
            (-1,-1,-1),(-2,0,0),(0,-2,0),(0,0,-2),(-1,1,-1),(-1,-1,1),(1,-1,-1)]


@component
class Hidden:
    hidden = False



"""
Генерация границ большого усечённого октаэдра, форму которого должны принять генерируемое множество сот.
Нормали каждой стороны уже известны, они генерируются прямо здесь,
и т к квадраты и шестиугольники находятся на разном расстоянии, отдельно для каждой группы сторон.
Потом определяется расстояние смещения нормалей, группируется в пары с самими нормалями. и возвращается.
"""
def generate_borders(size):
    normales6 = [np.array(norm) for norm in product((1, -1), repeat=3)]
    normales4 = [np.array(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]
    return [(norm / np.linalg.norm(norm), np.linalg.norm(norm * size)) for norm in normales4 + normales6]

"""
Генерация множеств интересующих нас координат ячеек соты из усечённых октаэдров.
Генерируем послойно, начиная из центра:
-для нового слоя из координат предыдущего слоя генерируем множество всех соседних клеток
-удаляем из нового слоя все координаты которые были сгенерированы ранее
-отрезаем координаты, которые вылезают за границы нужной нам области в виде большого усечённого октаэдра
-повторяем цикл пока таким образом не сгенерируем пустое множество
В процессе генерации сохраняем ячейки строго на границе в отдельное множество.
"""
def generate_coordinates(borders):
    solid: set = set()
    previous: set
    next: set = {CONSTANTS['center']} if borders[0][1] else set()
    hollow: set = set()
    brd = {CONSTANTS['center']} if isclose(borders[0][1], CONSTANTS['r4']) else set()

    faces = set(product((1, -1), repeat=3)).union(*[set(permutations((i, 0, 0))) for i in (2, -2)])
    faces = [Vec3(dot) for dot in faces]
    while next:
        solid.update(next)
        hollow.update(brd)
        previous = next.copy()
        next.clear()
        next.update(*[{pre + new * 2 for new in faces} for pre in previous])
        next.difference_update(solid)
        next = {point for point in next
                if all([x > 0.0 or isclose(x, 0.0, abs_tol=0.1) for x in [np.dot(norm, np.array(point)) + l for norm, l in borders]])}
        brd = {point for point in next
                if any([isclose(x, 0.0, abs_tol=0.1)
                        for x in [np.dot(norm, np.array(point)) + l for norm, l in borders]])}

    return dict(solid=solid, hollow=hollow)
"""
Генерируем кольцо траектории внутри полой фигуры из ячеек.
Получаем точку, индекс и множество ячеек.
Множество - ячейки сот образующие полый усечённый октаэдр.
Точка должна быть координатой одной из ячеек множества.
Индекс - одна из соседних с точкой ячеек.
-Находим все ячейки множества не дальше трёх радиусов описанной окружности ячейки от точки
-По индексу выбираем одну из найденных ячеек
-Из всех ячеек множества выбираем те, что находятся на плоскости, определяемой центром координат,
вектором в данную точку и вектором из данной точки в выбранную соседнюю ячейку и возвращаем полученное кольцо
"""
def generate_ring(point, index, shell):
    if point not in shell:
        return -1
    else:
        target = [x for x in shell if ursinamath.distance(point, x) < CONSTANTS["R"] * 3]
        if 0 <= index < len(target):
            dot = target[index]
            return [x for x in shell if isclose(np.linalg.det(np.array([x, point, dot - point])), 0.0, abs_tol=0.9)]
        else:
            return -1


level = {
    0: 0,
    1: 1,
    2: 2,
    3: 4
}
s = settings.BoardSize
border = create_entity(Position(),
                       Transparent(),
                       Renderable(),
                       Model("assets/models/Solid"),
                       Size(s),
                       Colour(color.gray))
"""
gameboard = generate_coordinates(generate_borders(s))

for el in gameboard["solid"]:
    clr = int(sum(el) % 8)
    create_entity(Position(el),
                  Hidden(),
                  Renderable(),
                  Model(),
                  Colour(color_calc[clr]))
"""

class BorderProcessor(Processor):
    def __init__(self):
        self.CONSTANTS = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))
        self.NORMALES = [(1,1,1),(2,0,0),(0,2,0),(0,0,2),(1,-1,1),(1,1,-1),(-1,1,1),
            (-1,-1,-1),(-2,0,0),(0,-2,0),(0,0,-2),(-1,1,-1),(-1,-1,1),(1,-1,-1)]
        self.shift = np.array([-4/3,-4/3,-4/3])
        self.FACES = [Vec3(n) * 2 for n in self.NORMALES]

    def process(self):
        size = settings.BoardSize
        brds = [np.array(n) for n in self.NORMALES]
        self.borders = [(norm / np.linalg.norm(norm), np.linalg.norm(norm * size)) for norm in brds]
        black_normales = [np.linalg.norm(n*size) - np.dot(n/np.linalg.norm(n), self.shift*size)/np.linalg.norm(self.shift*size) for n in brds[:7]]
        self.black_borders = [(n / np.linalg.norm(n), bn) for n in brds[:7] for bn in black_normales]


class CellposProcessor(Processor):

    def process(self):
        sys = get_system(GameboardSystem)
        size = settings.BoardSize
        limit = sys.get_processor(BorderProcessor)
        acr = 0.1
        solid: set = set()
        previous: set
        next: set = {Vec3(0,0,0)} if size > 0 else set()
        hollow: set = set()
        brd: set = {Vec3(0,0,0)} if size == 1 else set()

        while next:
            solid.update(next)
            hollow.update(brd)
            previous = next.copy()
            next.clear()
            next.update(*[{pre + new for new in limit.FACES} for pre in previous])
            next.difference_update(solid)
            next = {point for point in next
                    if all([x > 0.0 or isclose(x, 0.0, abs_tol=acr) for x in
                            [np.dot(norm, np.array(point)) + l for norm, l in limit.borders]])}
            brd = {point for point in next
                   if any([isclose(x, 0.0, abs_tol=acr)
                           for x in [np.dot(norm, np.array(point)) + l for norm, l in limit.borders]])}
        self.solid = solid
        self.hollow = hollow
        self.black_camp: set = {point for point in solid
                                if all([x > 0.0 or isclose(x, 0.0, abs_tol=acr) for x in
                                        [np.dot(norm, np.array(point)) + l for norm, l in limit.black_borders]])}

class CellProcessor(Processor):

    def process(self):
        sys = get_system(GameboardSystem)
        coordinates = sys.get_processor(CellposProcessor)
        color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
        for el in coordinates.solid:
            ent = create_entity(Position(el),
                          Hidden(),
                          Renderable(),
                          Model())
            if el in coordinates.black_camp:
                add_component(ent, Colour(color.black))
            else:
                clr = int(sum(el) % 8)
                add_component(ent, Colour(color_calc[clr]))



class GameboardSystem(System):

    def systemize(self):
        self.add_processor(BorderProcessor(), 2)
        self.add_processor(CellposProcessor(), 1)
        self.add_processor(CellProcessor(), 0)







if __name__ == '__main__':
    system_manager()
    systemize()
    get_system(RenderSystem).render.run()