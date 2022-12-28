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


def extract_column_indexed_map(row_indexed_map):
    longest_row = 0

    for row in row_indexed_map:
        row_len = len(row)
        if row_len > longest_row:
            longest_row = row_len

    num_of_rows = len(row_indexed_map)
    column_indexed_map = list()
    for x in range(longest_row):
        new_column = list()
        found_tiles_in_column = False

        for y in range(num_of_rows):
            if x >= len(row_indexed_map[y]):
                continue
            current_tile = row_indexed_map[y][x]
            if found_tiles_in_column and current_tile == ' ':
                continue
            if current_tile != ' ':
                found_tiles_in_column = True
            new_column.append(current_tile)

        column_indexed_map.append(''.join(new_column))

    return column_indexed_map


def read_input_file():
    file = open('input.txt', 'r')
    lines = file.read().splitlines()

    row_indexed_map = lines[:-2]
    column_indexed_map = extract_column_indexed_map(row_indexed_map)

    directions_chars = list(lines[-1])
    directions = parse_directions(directions_chars)

    return (row_indexed_map, column_indexed_map, directions)


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


def move_tiles(row_indexed_map, column_indexed_map, pos, current_orienation, num_of_tiles):
    x_index_offset = 0
    y_index_offset = 0

    if current_orienation == '>':
        x_index_offset = 1
    elif current_orienation == '<':
        x_index_offset = -1
    elif current_orienation == 'v':
        y_index_offset = 1
    elif current_orienation == '^':
        y_index_offset = -1

    for _ in range(num_of_tiles):

        next_y = pos.y + y_index_offset
        next_x = pos.x + x_index_offset

        if x_index_offset != 0:
            # moving x direction
            current_row = row_indexed_map[pos.y]

            if next_x == len(current_row):
                row = row_indexed_map[next_y]
                # find index of first tile
                first_space_index = row.find('.')
                first_wall_index = row.find('#')
                if first_wall_index == -1:
                    next_x = first_space_index
                else:
                    next_x = min(first_space_index, first_wall_index)
            elif next_x < 0:
                # find index of last non-space tile
                next_x = len(current_row) - 1

            if current_row[next_x] == ' ':
                next_x = len(current_row) - 1
        if y_index_offset != 0:
            # moving y direction
            current_column = column_indexed_map[pos.x]
            if next_y == len(current_column):
                column = column_indexed_map[next_x]

                first_space_index = column.find('.')
                first_wall_index = column.find('#')
                if first_wall_index == -1:
                    next_y = first_space_index
                else:
                    next_y = min(first_space_index, first_wall_index)
            elif next_y < 0:
                # find index of last non-space tile
                next_y = len(current_column) - 1

            if current_column[next_y] == ' ':
                next_y = len(current_column) - 1

        next_position_char = row_indexed_map[next_y][next_x]

        if next_position_char == '.':
            pos = Point(next_x, next_y)
        elif next_position_char == '#':
            return pos

    return pos


(row_indexed_map, column_indexed_map, directions) = read_input_file()

start_point_x = row_indexed_map[0].index('.')

pos = Point(start_point_x, 0)
orientation = '>'

for direction in directions:
    if type(direction) is int:
        pos = move_tiles(row_indexed_map, column_indexed_map,
                         pos, orientation, direction)
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
