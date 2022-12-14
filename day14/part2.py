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


class RockPath:
    def __init__(self) -> None:
        self.path_points = list()

    def add_point(self, point: Point):
        self.path_points.append(point)


def parse_input_file():
    file = open('input.txt', 'r')
    lines = file.readlines()

    rock_paths = list()

    max_x = 0
    max_y = 0

    for line in lines:
        rock_path = RockPath()
        rock_paths.append(rock_path)

        points = line.split(' -> ')
        for point in points:
            point_parts = point.split(',')
            x = int(point_parts[0])
            y = int(point_parts[1])
            rock_path.add_point(Point(x, y))

            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

    cave = list()

    # reversed x and y makes the part 2 solution harder so reverse them again 😭
    for x in range(max_x+1):
        cave.append(list())
        for y in range(max_y+3):  # + 3 because of the extra 2 spaces for the floor
            cave[x].append('.')

    cave[500][0] = '+'

    for rock_path in rock_paths:
        i = 0
        path_points = rock_path.path_points
        while i < len(path_points) - 1:
            start_point = path_points[i]
            end_point = path_points[i + 1]

            if start_point.x != end_point.x:
                # must be a horizontal rock
                start_x = min(start_point.x, end_point.x)
                end_x = max(start_point.x, end_point.x)
                for x in range(start_x, end_x + 1):
                    cave[x][start_point.y] = '#'
            elif start_point.y != end_point.y:
                # must be vertical rock
                start_y = min(start_point.y, end_point.y)
                end_y = max(start_point.y, end_point.y)
                for y in range(start_y, end_y + 1):
                    cave[start_point.x][y] = '#'

            i += 1

    for i in range(len(cave)):
        cave[i][-1] = '#'

    return cave


def print_cave(cave):
    for y in range(len(cave[0])):
        for x in range(len(cave)):
            print(cave[x][y], end='')
        print()


def simulate_one_unit_of_sand(cave):
    current_pos = Point(500, 0)

    at_rest = False
    while not at_rest:
        if cave[current_pos.x][current_pos.y + 1] == '.':
            current_pos = Point(current_pos.x, current_pos.y + 1)
            continue

        if current_pos.x == len(cave) - 1:
            # add an additional x column
            empty_cave_column = len(cave[0]) * '.'
            empty_cave_column = [x for x in empty_cave_column]
            empty_cave_column[-1] = '#'
            cave.append(empty_cave_column)

        if cave[current_pos.x - 1][current_pos.y + 1] == '.':
            current_pos = Point(current_pos.x - 1, current_pos.y + 1)
        elif cave[current_pos.x + 1][current_pos.y + 1] == '.':
            current_pos = Point(current_pos.x + 1, current_pos.y + 1)
        else:
            # no more options to move. We must be at rest at current_pos
            cave[current_pos.x][current_pos.y] = 'o'
            at_rest = True
            if current_pos.x == 500 and current_pos.y == 0:
                # new termination condition if we've come to rest at the sand origin
                return False

    return True


def send_in_the_sand(cave):
    sand_count = 1

    while simulate_one_unit_of_sand(cave):
        sand_count += 1
    return sand_count


cave = parse_input_file()
print_cave(cave)
print()

units_of_sand = send_in_the_sand(cave)
print_cave(cave)

print(units_of_sand)
