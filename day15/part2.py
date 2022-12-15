import collections

log_queue = collections.deque(maxlen=200)


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

    def calculate_covered_range(self, y, max_range):
        # find all positions in line y with a manhattan distance < the manhattan distance to the beacon

        # 0 for x as we're finding the distance directly in line
        directly_in_line_distance = abs(self.sensor_point.y - y)

        if (directly_in_line_distance <= self.manhattan_distance_to_beacon):
            # there is some coverage on this line
            remaining_distance = self.manhattan_distance_to_beacon - directly_in_line_distance
            min_x = self.sensor_point.x - remaining_distance
            max_x = self.sensor_point.x + remaining_distance

            min_x = 0 if min_x < 0 else min_x
            max_x = max_range if max_x > max_range else max_x

            return Range(min_x, max_x)
        else:
            return None


class Range:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.start}-{self.end}"


class LineSearch:
    def __init__(self, max_range) -> None:
        self.possible_ranges = list()
        self.possible_ranges.append(Range(0, max_range))
        self.all_ruled_out = False

    def has_single_option_remaining(self):
        return len(self.possible_ranges) == 1 and self.possible_ranges[0].start == self.possible_ranges[0].end

    def remaining_option(self):
        return self.possible_ranges[0].start

    def rule_out_range(self, rule_out_range):
        new_possible_ranges = list()

        # Case 1:
        # pppppppp         r.s > p.s and r.s <= p.e and r.e > p.e
        #     rrrrrrrrr
        #
        # Case 2:
        # pppppppp        r.s > p.s and r.e < p.e
        #    rrr
        #
        # Case 3:
        #   pppppp       r.s < p.s and r.e >= p.s and r.e < p.e
        # rrrrr
        #
        # Case 4:
        #   ppp
        # rrrrrrrr      p.s >= r.s and p.e <= r.e
        #
        # Case 5:
        # pppppp       r.s == p.s and r.e < p.e
        # rr
        #
        # Case 6:
        # pppppp       r.s > p.s and r.e == p.e
        #    rrr
        #
        # Case 7:
        # pppp
        #      rrrrr

        for possible_range in self.possible_ranges:
            if rule_out_range.start > possible_range.start and rule_out_range.start <= possible_range.end and rule_out_range.end > possible_range.end:
                log_queue.append('case 1')
                # Case 1: start falls within possible range
                # end falls outside so remove end part of range from this one and check next
                new_possible_ranges.append(
                    Range(possible_range.start, rule_out_range.start - 1)
                )
            elif rule_out_range.start > possible_range.start and rule_out_range.end < possible_range.end:
                log_queue.append("case 2")
                # Case 2: the rule_out_range is wholly contained within this possible range
                new_possible_ranges.append(
                    Range(possible_range.start, rule_out_range.start - 1)
                )
                new_possible_ranges.append(
                    Range(rule_out_range.end + 1, possible_range.end)
                )
            elif rule_out_range.start < possible_range.start and rule_out_range.end >= possible_range.start and rule_out_range.end < possible_range.end:
                log_queue.append("case 3")
                # Case 3: end falls within possible_range
                new_possible_ranges.append(
                    Range(rule_out_range.end + 1, possible_range.end)
                )
            elif rule_out_range.start <= possible_range.start and rule_out_range.end >= possible_range.end:
                log_queue.append("case 4")
                # Case 4: Rule out the entire range
                # don't add possible range to the new_possible_ranges list
                pass
            elif rule_out_range.start == possible_range.start and rule_out_range.end < possible_range.end:
                # Case 5: Rule out range exactly at the start of possible range
                log_queue.append('case 5')
                new_possible_ranges.append(
                    Range(rule_out_range.end + 1, possible_range.end))
            elif rule_out_range.start > possible_range.start and rule_out_range.end == possible_range.end:
                # Case 6: Rule out range exactly at the end of possible range
                log_queue.append('case 6')
                new_possible_ranges.append(
                    Range(possible_range.start, rule_out_range.start - 1))
            else:
                log_queue.append("case 7")
                # Case 7:
                # no overlap of rule_out_range and possible_range so keep possible range as possible
                new_possible_ranges.append(possible_range)
        self.possible_ranges = new_possible_ranges

        if len(self.possible_ranges) == 0:
            self.all_ruled_out = True
        log_queue.append(f'After rule out {self.possible_ranges}')


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
max_range = 4_000_000

for line_num in range(max_range):
    line_search = LineSearch(max_range)
    for sensor in sensors:
        covered_range = sensor.calculate_covered_range(line_num, max_range)
        if covered_range is not None:
            log_queue.append(f'Got cover {covered_range}')
            line_search.rule_out_range(covered_range)
            if line_search.all_ruled_out:
                log_queue.append('Early rule out')
                break
    if line_search.has_single_option_remaining():
        for log in log_queue:
            print(log)
        print(f'Got it {line_search.remaining_option()},{line_num}')
        print((line_search.remaining_option() * 4_000_000) + line_num)
        break
    else:
        log_queue.append(f'Line {line_num} fully ruled out')
