
from ursina import Vec3
from math import sqrt
from itertools import permutations, product

CONSTANTS = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))

def todo_nothing():
    pass

def generate_borders(size):
    if size <= 0:
        number_of_layers = 0
    elif int(size) == 1:
        number_of_layers = 1
    elif size < 7:
        number_of_layers = (int(size) - 1) * 4
    else:
        number_of_layers = 24
    normales6 = [Vec3(norm) for norm in product((1, -1), repeat=3)]
    normales4 = [Vec3(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]
    distance6 = CONSTANTS['r6'] * number_of_layers
    distance4 = CONSTANTS['r4'] * number_of_layers
    return [(norm, distance4) for norm in normales4] + [(norm, distance6) for norm in normales6]

def generate_coordinates(borders):
    result: set = set()
    previous: set
    next: set = {CONSTANTS['center']} if borders[0][1] else set()

    faces = set(product((1, -1), repeat=3)).union(*[set(permutations((i, 0, 0))) for i in (2, -2)])
    faces = [Vec3(dot) for dot in faces]
    while next:
        result.update(next)
        previous = next.copy()
        next.clear()
        next.update(*[{pre + new * 2 for new in faces} for pre in previous])
        next.difference_update(result)
        next = {point for point in next if all([x >= 0.0 for x in [sum(norm * point) + d for norm, d in borders]])}
    return result

if __name__ == '__main__':
    print("This is not app!")


