import collections
import math
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


def read_input_file():
    file = open('input.txt', 'r')
    input = file.read().strip()
    return input


def fetch_next_rock(rocks_queue):
    rock = rocks_queue[0]
    rocks_queue.rotate(-1)

    return rock


def can_move_down(rock, cave):
    potential_new_origin = Point(rock_pos.x, rock_pos.y - 1)

    if potential_new_origin.y == -1:
        return False

    for sprite_y, sprite_line in enumerate(rock):
        for sprite_x, sprite_char in enumerate(sprite_line):
            if sprite_char == '#':
                if cave[potential_new_origin.y + sprite_y][potential_new_origin.x + sprite_x] != '.':
                    return False
    return True


def apply_jet_to_rock(rock, rock_pos, jet_dir, cave):
    if jet_dir == '>':
        x_diff = 1
    else:
        x_diff = -1

    potential_new_origin = Point(rock_pos.x + x_diff, rock_pos.y)

    for sprite_y, sprite_line in enumerate(rock):
        for sprite_x, sprite_char in enumerate(sprite_line):
            if sprite_char == '#':
                if potential_new_origin.x + sprite_x > 6:
                    return rock_pos
                if potential_new_origin.x + sprite_x < 0:
                    return rock_pos
                if cave[potential_new_origin.y + sprite_y][potential_new_origin.x + sprite_x] != '.':
                    return rock_pos

    # we've checked everything. Return jetted position
    return potential_new_origin


def cement_rock_into_position(rock, rock_pos, cave, highest_rock_y):
    for sprite_y, sprite_line in enumerate(rock):
        for sprite_x, sprite_char in enumerate(sprite_line):
            if sprite_char == '#':
                rock_part_y = rock_pos.y + sprite_y
                cave[rock_part_y][rock_pos.x + sprite_x] = '#'

                if (rock_part_y+1 > highest_rock_y):
                    highest_rock_y = rock_part_y + 1
    return highest_rock_y


def print_cave(cave, rock, rock_pos):
    cave_height = len(cave)

    for i, row in enumerate(reversed(cave)):
        drawing_row = list(row)
        drawing_y = cave_height - i - 1

        sprite_y = drawing_y - rock_pos.y

        if sprite_y >= 0 and sprite_y < len(rock):
            sprite_row = rock[sprite_y]
            for i in range(len(sprite_row)):
                if sprite_row[i] == '#':
                    drawing_row[rock_pos.x + i] = '@'
        row_string = ''.join(drawing_row)
        print(f'|{row_string}|')

    print('+-------+')


rocks_queue = collections.deque()
rocks_queue.append(['####'])

rocks_queue.append(['.#.',
                    '###',
                    '.#.'])

rocks_queue.append(['###',  # Upside down so the zero based indexing makes it the right way up...
                    '..#',
                    '..#'])

rocks_queue.append(['#',
                    '#',
                    '#',
                    '#'])

rocks_queue.append(['##',
                    '##'])


cave = list()  # each element is a row represented as a list of chars

jets_string = read_input_file()
jets_index = 0

rocks_stopped = 0
highest_rock_y = 0
highest_rock_y_at_calc_point = 0
total_calculated_height = 0

further_rocks = sys.maxsize

while further_rocks > 0:
    rock = fetch_next_rock(rocks_queue)
    further_rocks -= 1

    rock_pos = Point(2, highest_rock_y + 3)

    while len(cave) < highest_rock_y + 3 + len(rock):
        cave.append(['.', '.', '.', '.', '.', '.', '.'])

    # There are several magic values identified by experimentation below...

    # 281 identified as a repeat point by keeping hash of jet index -> new rock type
    # If an index/rock type combo already exists in the hash it means we're on a repeat
    # and therefore it should keep repeating in future iterations. This was proved for this
    # point by running several iterations
    if jets_index == 281:
        remaining_rocks_count = 1000000000000 - rocks_stopped

        # 1725 is the number of rocks in each cycle of the repetition
        # so this will give us the no. of iterations required to get to the insane
        # number of rocks settled.
        full_iterations_required = math.floor(remaining_rocks_count / 1725)
        further_rocks = (remaining_rocks_count % 1725)-1

        # 2728 is the height of rocks added in each iteration of the repititon
        total_calculated_height = highest_rock_y + \
            (full_iterations_required * 2728)

        highest_rock_y_at_calc_point = highest_rock_y

    while True:
        # move and fall cycle
        jet_dir = jets_string[jets_index]
        jets_index += 1
        if jets_index == len(jets_string):
            jets_index = 0

        rock_pos = apply_jet_to_rock(rock, rock_pos, jet_dir, cave)
        #print_cave(cave, rock, rock_pos)

        if can_move_down(rock, cave):
            rock_pos = Point(rock_pos.x, rock_pos.y-1)
        else:
            highest_rock_y = cement_rock_into_position(
                rock, rock_pos, cave, highest_rock_y)
            rocks_stopped += 1
            break

print(total_calculated_height + (highest_rock_y - highest_rock_y_at_calc_point))
