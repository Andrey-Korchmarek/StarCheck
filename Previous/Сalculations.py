
from ursina import Vec3
from math import sqrt
from itertools import permutations, product

CONSTANTS = dict(a=sqrt(2), r6=sqrt(3), r4=2.0, p=1.5 * sqrt(2), R=sqrt(5), center=Vec3(0, 0, 0))

def mdl(vec: Vec3) -> float:
    return sqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z)

def border_distance(layers: int) -> int:
    if 0 == layers:
        return 0
    elif 1 == layers:
        return 1
    else:
        return (layers - 1) * 4

def generate_borders(size):
    number_of_layers = border_distance(size)
    normales6 = [Vec3(norm) for norm in product((1, -1), repeat=3)]
    normales4 = [Vec3(norm) for norm in set().union(*[set(permutations((i, 0, 0))) for i in (2, -2)])]
    distance6 = CONSTANTS['r6'] * number_of_layers
    distance4 = CONSTANTS['r4'] * number_of_layers
    brd = [(norm, distance4) for norm in normales4] + [(norm, distance6) for norm in normales6]
    p =  Vec3(-1, -1, -1) * (number_of_layers * 2 + 1 - (size - 1) * 3)
    pls = [(n, r+sum(n*p)/mdl(n)) for n, r in brd if n in [(1,1,1),(2,0,0),(0,2,0),(0,0,2),(-1,1,1),(1,-1,1),(1,1,-1)]]
    m = Vec3(1, 1, 1) * (number_of_layers * 2 + 1 - (size - 1) * 3)
    mns = [(n, r+sum(n*m)/mdl(n)) for n, r in brd if -n in [(1,1,1),(2,0,0),(0,2,0),(0,0,2),(-1,1,1),(1,-1,1),(1,1,-1)]]
    return dict(limits = brd, plus = pls, minus = mns)

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
        next = {point for point in next if all([x >= 0.0 for x in [sum(norm * point) + l for norm, l in borders]])}
    return result

if __name__ == '__main__':
    print("This is not app!")


