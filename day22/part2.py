import math


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


def parse_directions(directions_chars):
    directions = list()

    current_distance_chars = list()
    for char in directions_chars:
        if char == 'L' or char == 'R':
            directions.append(int(''.join(current_distance_chars)))
            current_distance_chars = list()
            directions.append(char)
        else:
            current_distance_chars.append(char)

    directions.append(int(''.join(current_distance_chars)))

    return directions


def read_input_file():
    file = open('input.txt', 'r')
    lines = file.read().splitlines()

    the_map = lines[:-2]

    directions_chars = list(lines[-1])
    directions = parse_directions(directions_chars)

    return (the_map, directions)


def update_orientation(current_orientation, direction):
    if direction == 'L':
        if current_orientation == '^':
            return '<'
        if current_orientation == '<':
            return 'v'
        if current_orientation == 'v':
            return '>'
        if current_orientation == '>':
            return '^'
    else:
        if current_orientation == '^':
            return '>'
        if current_orientation == '>':
            return 'v'
        if current_orientation == 'v':
            return '<'
        if current_orientation == '<':
            return '^'


def get_possible_pos_for_next_step(pos, current_orientation):
    # Net layout for my large input
    # I manually worked out how the faces relate to each other.
    # I'm sure there's a programmatic way of doing this but I'm not
    # sure what that is. This works and isn't too bad for a 3D
    # cube.
    #
    #          up from E == A facing right
    #          left from E == B facing right
    #          up from F == A facing up
    #   EEFF   right from F == C facing left
    #   EEFF   down from F == D facing left
    #   DD     down from C == A facing left
    #   DD     right from D == F facing up
    # BBCC     left from D == B facing down
    # BBCC     right from C == F facing left
    # AA       down from C == A facing left
    # AA       left from B == E facing right
    #          up from B == D facing right
    #          left from A == E facing down
    #          right from A == C facing up
    #          down from A == F facing down
    a_x_range = range(50)
    a_y_range = range(150, 200)

    b_x_range = range(50)
    b_y_range = range(100, 150)

    c_x_range = range(50, 100)
    c_y_range = range(100, 150)

    d_x_range = range(50, 100)
    d_y_range = range(50, 100)

    e_x_range = range(50, 100)
    e_y_range = range(50)

    f_x_range = range(100, 150)
    f_y_range = range(50)

    x_index_offset = 0
    y_index_offset = 0

    if current_orientation == '>':
        x_index_offset = 1
    elif current_orientation == '<':
        x_index_offset = -1
    elif current_orientation == 'v':
        y_index_offset = 1
    elif current_orientation == '^':
        y_index_offset = -1

    next_y = pos.y + y_index_offset
    next_x = pos.x + x_index_offset
    next_orientation = current_orientation

    # Exhausively work out out next face and orientation if we go off any edge based on the current face
    if pos.x in a_x_range and pos.y in a_y_range:
        # we're in A
        # Face B above
        next_orientation_up = '^'
        next_x_up = pos.x
        next_y_up = pos.y - 1

        # Face F below
        next_orientation_down = 'v'
        next_x_down = f_x_range.start + (pos.x % 50)
        next_y_down = f_y_range.start

        # Face E to the left
        next_orientation_left = 'v'
        next_x_left = e_x_range.start + (pos.y % 50)
        next_y_left = e_y_range.start

        # Face C to the right
        next_orientation_right = '^'
        next_x_right = c_x_range.start + (pos.y % 50)
        next_y_right = c_y_range.stop - 1
    elif pos.x in b_x_range and pos.y in b_y_range:
        # we're in B
        # Face D above
        next_orientation_up = '>'
        next_x_up = d_x_range.start
        next_y_up = d_y_range.start + (pos.x % 50)

        # Face A below
        next_orientation_down = 'v'
        next_x_down = pos.x
        next_y_down = pos.y + 1

        # Face E to the left
        next_orientation_left = '>'
        next_x_left = e_x_range.start
        # need to invert the y position within the face
        next_y_left = (e_y_range.stop - 1) - (pos.y % 50)

        # Face C to the right
        next_orientation_right = '>'
        next_x_right = pos.x + 1
        next_y_right = pos.y
    elif pos.x in c_x_range and pos.y in c_y_range:
        # we're in C
        # Face D above
        next_orientation_up = '^'
        next_x_up = pos.x
        next_y_up = pos.y - 1

        # Face A below
        next_orientation_down = '<'
        next_x_down = a_x_range.stop - 1
        next_y_down = a_y_range.start + (pos.x % 50)

        # Face B to the left
        next_orientation_left = '<'
        next_x_left = pos.x - 1
        next_y_left = pos.y

        # Face F to the right
        next_orientation_right = '<'
        next_x_right = f_x_range.stop - 1
        # need to invert the y position within the face
        next_y_right = (f_y_range.stop - 1) - (pos.y % 50)
    elif pos.x in d_x_range and pos.y in d_y_range:
        # we're in D
        # Face E above
        next_orientation_up = '^'
        next_x_up = pos.x
        next_y_up = pos.y - 1

        # Face C below
        next_orientation_down = 'v'
        next_x_down = pos.x
        next_y_down = pos.y + 1

        # Face B to the left
        next_orientation_left = 'v'
        next_x_left = b_x_range.start + (pos.y % 50)
        next_y_left = b_y_range.start

        # Face F to the right
        next_orientation_right = '^'
        next_x_right = f_x_range.start + (pos.y % 50)
        next_y_right = f_y_range.stop - 1
    elif pos.x in e_x_range and pos.y in e_y_range:
        # we're in E
        # Face A above
        next_orientation_up = '>'
        next_x_up = a_x_range.start
        next_y_up = a_y_range.start + (pos.x % 50)

        # Face D below
        next_orientation_down = 'v'
        next_x_down = pos.x
        next_y_down = pos.y + 1

        # Face B to the left
        next_orientation_left = '>'
        next_x_left = b_x_range.start
        # need to invert the y position within the face
        next_y_left = (b_y_range.stop - 1) - (pos.y % 50)

        # Face F to the right
        next_orientation_right = '>'
        next_x_right = pos.x + 1
        next_y_right = pos.y
    elif pos.x in f_x_range and pos.y in f_y_range:
        # we're in F
        # Face A above
        next_orientation_up = '^'
        next_x_up = a_x_range.start + (pos.x % 50)
        next_y_up = a_y_range.stop - 1

        # Face D below
        next_orientation_down = '<'
        next_x_down = d_x_range.stop - 1
        next_y_down = d_y_range.start + (pos.y % 50)

        # Face E to the left
        next_orientation_left = '<'
        next_x_left = pos.x - 1
        next_y_left = pos.y

        # Face C to the right
        next_orientation_right = '<'
        next_x_right = c_x_range.stop - 1
        # need to invert the y position within the face
        next_y_right = (c_y_range.stop - 1) - (pos.y % 50)

    if math.floor(next_x / 50) != math.floor(pos.x / 50):
        # new side in x direction
        if x_index_offset == -1:
            # going left
            next_x = next_x_left
            next_y = next_y_left
            next_orientation = next_orientation_left
        elif x_index_offset == 1:
            # going right
            next_x = next_x_right
            next_y = next_y_right
            next_orientation = next_orientation_right
        else:
            print(
                "ERROR: No x index offset even though we should be moving in x direction")
    elif math.floor(next_y / 50) != math.floor(pos.y / 50):
        # new side in y direction
        if y_index_offset == -1:
            # going up
            next_x = next_x_up
            next_y = next_y_up
            next_orientation = next_orientation_up
        elif y_index_offset == 1:
            # going down
            next_x = next_x_down
            next_y = next_y_down
            next_orientation = next_orientation_down
        else:
            print(
                "ERROR: No y index offset even though we should be moving in y direction")

    return (Point(next_x, next_y), next_orientation)


def move_tiles(the_map, pos, current_orientation, num_of_tiles):
    for _ in range(num_of_tiles):

        (next_pos, next_orientation) = get_possible_pos_for_next_step(
            pos, current_orientation)

        next_position_char = the_map[next_pos.y][next_pos.x]

        if next_position_char == '.':
            pos = next_pos
            current_orientation = next_orientation
        elif next_position_char == '#':
            # We can stop further steps as we can't go any further in this direction
            return (pos, current_orientation)

    return (pos, current_orientation)


(the_map, directions) = read_input_file()

start_point_x = the_map[0].index('.')

pos = Point(start_point_x, 0)
orientation = '>'

for direction in directions:
    if type(direction) is int:
        (new_pos, new_orientation) = move_tiles(
            the_map, pos, orientation, direction)
        pos = new_pos
        orientation = new_orientation
    else:
        orientation = update_orientation(orientation, direction)

print(pos)

facing = 0
if orientation == 'v':
    facing = 1
elif orientation == '<':
    facing = 2
elif orientation == '^':
    facing = 3

password = (1000 * (pos.y+1)) + (4 * (pos.x+1)) + facing

print(password)
