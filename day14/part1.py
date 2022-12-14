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

    # x and y reversed to aid printing out the cave
    for y in range(max_y+1):
        cave.append(list())
        for x in range(max_x+1):
            cave[y].append('.')

    cave[0][500] = '+'

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
                    cave[start_point.y][x] = '#'
            elif start_point.y != end_point.y:
                # must be vertical rock
                start_y = min(start_point.y, end_point.y)
                end_y = max(start_point.y, end_point.y)
                for y in range(start_y, end_y + 1):
                    cave[y][start_point.x] = '#'

            i += 1

    return cave


def print_cave(cave):
    for i, line in enumerate(cave):
        line = ''.join(line)
        print(f'{i:3} {line}')


def simulate_one_unit_of_sand(cave):
    current_pos = Point(500, 0)

    at_rest = False
    while not at_rest:
        if current_pos.y == len(cave) - 1 or current_pos.x == len(cave[0]) - 1:
            return False

        if cave[current_pos.y + 1][current_pos.x] == '.':
            current_pos = Point(current_pos.x, current_pos.y + 1)
        elif cave[current_pos.y + 1][current_pos.x - 1] == '.':
            current_pos = Point(current_pos.x - 1, current_pos.y + 1)
        elif cave[current_pos.y + 1][current_pos.x + 1] == '.':
            current_pos = Point(current_pos.x + 1, current_pos.y + 1)
        else:
            # no more options to move. We must be at rest at current_pos
            cave[current_pos.y][current_pos.x] = 'o'
            at_rest = True

    return True


def send_in_the_sand(cave):
    sand_count = 0

    while simulate_one_unit_of_sand(cave):
        sand_count += 1
    return sand_count


cave = parse_input_file()
print_cave(cave)
print()

units_of_sand = send_in_the_sand(cave)
print_cave(cave)

print(units_of_sand)
