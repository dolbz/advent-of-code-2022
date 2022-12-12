from queue import PriorityQueue
import string
import sys


class Position:
    def __init__(self, height, x, y):
        self.height = height
        self.x = x
        self.y = y
        self.navigable_neighbours = list()

    def __lt__(self, other):
        return False


def append_neighbour_if_navigable(pos, neighbour):
    if neighbour.height <= pos.height + 1:
        pos.navigable_neighbours.append(neighbour)


def parse_input_file_to_graph():
    file = open('input.txt', 'r')
    lines = file.readlines()

    height_to_char = dict(enumerate(string.ascii_lowercase, 1))
    char_to_height = dict((v, k) for k, v in height_to_char.items())

    position_matrix = list()
    possible_starts = list()
    end_position = None

    for y, line in enumerate(lines):
        position_matrix.append(list())

        for x, pos in enumerate(line):
            if pos == '\n':
                continue
            position = None
            if pos == 'S' or pos == 'a':
                position = Position(1, x, y)
                possible_starts.append(position)
            elif pos == 'E':
                position = Position(26, x, y)
                end_position = position
            else:
                position = Position(char_to_height[pos], x, y)

            position_matrix[y].append(position)

    for y in range(len(position_matrix)):
        for x in range(len(position_matrix[y])):
            pos = position_matrix[y][x]

            if x > 0:
                left_pos = position_matrix[y][x-1]
                append_neighbour_if_navigable(pos, left_pos)
            if x < len(position_matrix[y]) - 1:
                right_pos = position_matrix[y][x+1]
                append_neighbour_if_navigable(pos, right_pos)
            if y > 0:
                above_pos = position_matrix[y-1][x]
                append_neighbour_if_navigable(pos, above_pos)
            if y < len(position_matrix) - 1:
                below_pos = position_matrix[y+1][x]
                append_neighbour_if_navigable(pos, below_pos)

    return (possible_starts, end_position)


def heuristic_distance(from_pos: Position, to_pos: Position):
    return abs(from_pos.x - to_pos.x) + abs(from_pos.y - to_pos.y)


def find_shortest_path_from(from_position, to_position):
    # Uses A* path finding algorithm as a naive exhaustive search was running too slow
    frontier = PriorityQueue()
    frontier.put(from_position, 0)
    cost_so_far: dict[Position, int] = {}
    cost_so_far[from_position] = 0

    while not frontier.empty():
        current: Position = frontier.get()

        # commented as we want an exhaustive search to find shortest. Not _a_ path
        # if current == to_position:
        #     break

        for next in current.navigable_neighbours:
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_distance(next, to_position)
                frontier.put(next, priority)

    if (to_position in cost_so_far):
        return cost_so_far[to_position]
    else:
        return sys.maxsize


(possible_starts, end_position) = parse_input_file_to_graph()
hops = list()

for i, possible_start in enumerate(possible_starts):
    print(f'Searching {i} of {len(possible_starts)}')
    hops.append(find_shortest_path_from(possible_start, end_position))

print(min(hops))
