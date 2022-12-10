import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


def symbol_for_point(point, rope_knots):
    for i, knot in enumerate(rope_knots):
        current_pos = knot[-1]
        if current_pos == point:
            return 'H' if i == 0 else f'{i}'

    if point == Point(0, 0):
        return 'S'
    else:
        return '.'


def draw_current_state(rope_knots):
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0

    for knot in rope_knots:
        current_pos = knot[-1]

        if current_pos.x > max_x:
            max_x = current_pos.x
        if current_pos.y > max_y:
            max_y = current_pos.y
        if current_pos.x < min_x:
            min_x = current_pos.x
        if current_pos.y < min_y:
            min_y = current_pos.y

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            symbol = symbol_for_point(Point(x, max_y-y), rope_knots)
            print(symbol, end='')
        print()

    print()


file = open('input.txt', 'r')
moves = file.readlines()

rope_knots = list()

for i in range(10):
    rope_knots.append(list())
    rope_knots[i].append(Point(0, 0))

for move in moves:
    parts = move.split()

    direction = parts[0]
    num_of_steps = int(parts[1])

    x_diff = 0
    y_diff = 0

    match direction:
        case 'U':
            y_diff = 1
        case 'D':
            y_diff = -1
        case 'L':
            x_diff = -1
        case 'R':
            x_diff = 1

    print(f'Move: {move}')
    for step_num in range(num_of_steps):

        # move the head
        head_pos = rope_knots[0][-1]
        new_head_pos = Point(head_pos.x + x_diff, head_pos.y + y_diff)
        rope_knots[0].append(new_head_pos)

        # work out movement for each subsequent knot
        for knot_num in range(1, 10):
            current_knot_pos = rope_knots[knot_num][-1]
            preceding_knot_pos = rope_knots[knot_num-1][-1]

            relative_x_diff = preceding_knot_pos.x - current_knot_pos.x
            relative_y_diff = preceding_knot_pos.y - current_knot_pos.y

            if abs(relative_x_diff) > 1 or abs(relative_y_diff) > 1:
                if relative_x_diff == 2:
                    relative_x_diff = 1
                if relative_y_diff == 2:
                    relative_y_diff = 1
                if relative_x_diff == -2:
                    relative_x_diff = -1
                if relative_y_diff == -2:
                    relative_y_diff = -1

                new_pos = Point(current_knot_pos.x + relative_x_diff,
                                current_knot_pos.y + relative_y_diff)

                rope_knots[knot_num].append(new_pos)

    # draw_current_state(rope_knots)

print(len(set(rope_knots[9])))
