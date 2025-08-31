from __init__ import *
import core
import render
from math import sqrt, isclose
from itertools import permutations, product
import numpy as np

# Хранилище параметров усечённого октаэдра: длинна стороны, радиусы вписанной сфер шестиугольников и квадратов,
# радиус полувписанной сферы, радиус описанной сферы, координаты начальной ячейки в генераторе сот
CONSTANTS = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))
NORMALES = [(1, 1, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, -1, 1), (1, 1, -1), (-1, 1, 1),
            (-1, -1, -1), (-2, 0, 0), (0, -2, 0), (0, 0, -2), (-1, 1, -1), (-1, -1, 1), (1, -1, -1)]
NPNRMLS = [np.array(n) for n in NORMALES]
FACES = [Vec3(n) * 2 for n in NORMALES]

"""
Генерация множеств интересующих нас координат ячеек соты из усечённых октаэдров.
Генерируем послойно, начиная из центра:
-для нового слоя из координат предыдущего слоя генерируем множество всех соседних клеток
-удаляем из нового слоя все координаты которые были сгенерированы ранее
-отрезаем координаты, которые вылезают за границы нужной нам области в виде большого усечённого октаэдра
-повторяем цикл пока таким образом не сгенерируем пустое множество
В процессе генерации сохраняем ячейки строго на границе в отдельное множество.
"""

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
def generate_coordinates(size):
    borders = [(norm / np.linalg.norm(norm), np.linalg.norm(norm * size)) for norm in NPNRMLS]
    acr = 0.1
    solid: set = set()
    previous: set
    next: set = {Vec3(0, 0, 0)} if size > 0 else set()
    hollow: set = set()
    brd: set = {Vec3(0, 0, 0)} if size == 1 else set()

    while next:
        solid.update(next)
        hollow.update(brd)
        previous = next.copy()
        next.clear()
        next.update(*[{pre + new for new in FACES} for pre in previous])
        next.difference_update(solid)
        next = {point for point in next
                if all([x > 0.0 or isclose(x, 0.0, abs_tol=acr) for x in
                        [np.dot(norm, np.array(point)) + l for norm, l in borders]])}
        brd = {point for point in next
               if any([isclose(x, 0.0, abs_tol=acr)
                       for x in [np.dot(norm, np.array(point)) + l for norm, l in borders]])}
    return dict(solid=solid, hollow=hollow)

def create_gameboard(size):
    border = create_entity(render.Renderable(position=Vec3(0, 0, 0),
                                             model="assets/models/Solid",
                                             color=color.gray,
                                             alpha=0.2,
                                             scale=size),
                           render.Size(size))
    coordinates = generate_coordinates(size)
    color_calc = {0: color.gray, 2: color.red, 6: color.green, 4: color.blue}
    for el in coordinates["solid"]:
        settings.FEN[el] = None
        clr = int(sum(el) % 8)
        create_entity(render.Cell(),
                      render.Renderable(position=el,
                                 model="assets/models/Cell",
                                 color=color_calc[clr],
                                 visible=False))
        ent = create_entity(core.Position(el), render.Nucleus(),
                            render.Renderable(position=el,
                                       color=color.yellow,
                                       collider='sphere', collision=True,
                                       enabled=False))
        settings.EFEN['NUCLEUS'][el] = ent

if __name__ == '__main__':
    pass
