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


class Sensor:
    def __init__(self, sensor_point: Point, closest_beacon: Point):
        self.sensor_point = sensor_point
        self.closest_beacon = closest_beacon
        self.manhattan_distance_to_beacon = abs(
            sensor_point.x - closest_beacon.x) + abs(sensor_point.y - closest_beacon.y)

    def coverage_of_line(self, y):
        # find all positions in line y with a manhattan distance < the manhattan distance to the beacon

        # 0 for x as we're finding the distance directly in line
        directly_in_line_distance = abs(self.sensor_point.y - y)

        if (directly_in_line_distance <= self.manhattan_distance_to_beacon):
            # there is some coverage on this line
            remaining_distance = self.manhattan_distance_to_beacon - directly_in_line_distance
            min_x = self.sensor_point.x - remaining_distance
            max_x = self.sensor_point.x + remaining_distance

            points_in_range = [*range(min_x, max_x + 1)]

            if self.closest_beacon.y == y:
                points_in_range.remove(self.closest_beacon.x)

            return points_in_range
        else:
            return None


def parse_input_file():
    file = open('input.txt', 'r')
    lines = file.readlines()

    sensors = list()

    for line in lines:
        line_parts = line.strip().split()
        sensor_x = int(line_parts[2][2:-1])
        sensor_y = int(line_parts[3][2:-1])
        sensor_point = Point(sensor_x, sensor_y)

        closest_beacon_x = int(line_parts[8][2:-1])
        closest_beacon_y = int(line_parts[9][2:])
        closest_beacon_point = Point(closest_beacon_x, closest_beacon_y)

        sensors.append(Sensor(sensor_point, closest_beacon_point))

    return sensors


sensors = parse_input_file()

coverage = set()
for sensor in sensors:
    line_coverage = sensor.coverage_of_line(2_000_000)
    if line_coverage is not None:
        line_coverage = set(line_coverage)
        coverage = coverage.union(line_coverage)

print(len(coverage))
