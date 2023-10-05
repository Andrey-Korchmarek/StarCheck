from ursina import Vec3
from math import sqrt, isclose
from itertools import permutations, product
import numpy as np

# Хранилище параметров усечённого октаэдра: длинна стороны, радиусы вписанной сфер шестиугольников и квадратов,
# радиус полувписанной сферы, радиус описанной сферы, координаты начальной ячейки в генераторе сот
CONSTANTS = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))

# Вычисление расстояния границ генерации сот в радиусах вписанных сфер
def border_distance(layers: int) -> int:
    if 0 == layers:
        return 0
    elif 1 == layers:
        return 1
    elif 2 == layers:
        return 2
    else:
        return 2 + (layers - 2) * 2

"""
Генерация границ большого усечённого октаэдра, форму которого должны принять генерируемое множество сот.
Нормали каждой стороны уже известны, они генерируются прямо здесь, и т к квадраты и шестиугольники находятся на разном
расстоянии, отдельно для каждой группы сторон.
Потом определяется расстояние смещения нормалей, группируется в пары с самими нормалями. и возвращается.
"""
def generate_borders(size):
    number_of_layers = border_distance(size)
    normales6 = [Vec3(norm) for norm in product((1, -1), repeat=3)]
    normales4 = [Vec3(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]
    distance6 = CONSTANTS['r6'] * number_of_layers
    distance4 = CONSTANTS['r4'] * number_of_layers
    return [(norm, distance4) for norm in normales4] + [(norm, distance6) for norm in normales6]

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
        next = {point for point in next if all([int(x) >= 0 for x in [sum(norm * point) + l for norm, l in borders]])}
        brd = {point for point in next
                if any([isclose(x, 0.0, abs_tol=0.9) for x in [sum(norm * point) + l for norm, l in borders]])}

    return dict(solid=solid, hollow=hollow)

def generate_ring(point, index, shell):
    if point not in shell:
        return -1
    else:
        faces = set(product((1, -1), repeat=3)).union(*[set(permutations((i, 0, 0))) for i in (2, -2)])
        faces = [Vec3(dot) for dot in faces]
        target = [point + x for x in faces]
        target = [t for t in target if t in shell]
        if 0 <= index < len(target):
            dot = target[index]
            return [x for x in shell if isclose(np.linalg.det(np.array([x, point, dot - point])), 0.0, abs_tol=0.9)]
        else:
            return -1

if __name__ == '__main__':
    board = generate_coordinates(generate_borders(7))
    shell = board["hollow"]
    print(generate_ring(Vec3(0, 12, 0), 0, shell))
