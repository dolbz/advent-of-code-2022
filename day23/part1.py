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
    lines = file.read().splitlines()

    elf_positions = dict()

    num_of_lines = len(lines)

    for line_num, line in enumerate(lines):
        for x, entry in enumerate(line):
            if entry == '#':
                elf_positions[Point(x, num_of_lines - line_num)] = True

    return elf_positions


def check_clear_direction(direction, elf_positions, elf_pos):
    x_sweep = False

    x_start = elf_pos.x
    y_start = elf_pos.y

    if direction == 'N':
        x_sweep = True
        y_start = elf_pos.y + 1
    elif direction == 'E':
        x_start = elf_pos.x + 1
    elif direction == 'S':
        x_sweep = True
        y_start = elf_pos.y - 1
    else:
        x_start = elf_pos.x - 1

    # BUG fixed in part 2 but apparently doesn't cause any difference to the result
    # for part 1 (for my input). Range should be from -1 to +1 but we're doing 0 - 2 below
    for i in range(3):
        x = x_start
        y = y_start

        if x_sweep:
            x = x_start + i
        else:
            y = y_start + i

        pos_to_check = Point(x, y)

        if pos_to_check in elf_positions:
            return False
    return True


def get_move_proposals(elf_positions, direction_check_order):
    proposal_positions = dict()

    for elf_pos in elf_positions:
        proposal_pos = elf_pos
        if (
                Point(elf_pos.x - 1, elf_pos.y - 1) in elf_positions or
                Point(elf_pos.x, elf_pos.y - 1) in elf_positions or
                Point(elf_pos.x + 1, elf_pos.y - 1) in elf_positions or

                Point(elf_pos.x - 1, elf_pos.y) in elf_positions or
                Point(elf_pos.x + 1, elf_pos.y) in elf_positions or

                Point(elf_pos.x - 1, elf_pos.y + 1) in elf_positions or
                Point(elf_pos.x, elf_pos.y + 1) in elf_positions or
                Point(elf_pos.x + 1, elf_pos.y + 1) in elf_positions
        ):
            for direction in direction_check_order:
                is_clear = check_clear_direction(
                    direction, elf_positions, elf_pos)

                if is_clear:
                    if direction == 'N':
                        proposal_pos = Point(elf_pos.x, elf_pos.y + 1)
                    elif direction == 'E':
                        proposal_pos = Point(elf_pos.x + 1, elf_pos.y)
                    elif direction == 'S':
                        proposal_pos = Point(elf_pos.x, elf_pos.y - 1)
                    else:
                        proposal_pos = Point(elf_pos.x - 1, elf_pos.y)

                    # BUG fixed in part 2. There should be a break here otherwise we will continue the
                    # for loop and end up with the last position being proposed in all cases.
                    # Apparently this bug didn't impact the result for part 1 (for my input)

        if proposal_pos not in proposal_positions:
            proposal_positions[proposal_pos] = list()
        proposal_positions[proposal_pos].append(elf_pos)
    return proposal_positions


def get_final_positions(position_proposals):
    final_positions = dict()

    for proposed_pos, proposers in position_proposals.items():
        if len(proposers) == 1:
            final_positions[proposed_pos] = True
        else:
            for proposer_pos in proposers:
                final_positions[proposer_pos] = True

    return final_positions


def get_empty_tile_count_within_elf_positions_rect(elf_positions):
    min_x = sys.maxsize
    max_x = -sys.maxsize

    min_y = sys.maxsize
    max_y = -sys.maxsize

    for pos in elf_positions:
        if pos.x < min_x:
            min_x = pos.x
        elif pos.x > max_x:
            max_x = pos.x

        if pos.y < min_y:
            min_y = pos.y
        elif pos.y > max_y:
            max_y = pos.y

    bounding_rect_x_size = max_x - min_x + 1
    bounding_rect_y_size = max_y - min_y + 1

    total_tiles = bounding_rect_x_size * bounding_rect_y_size

    empty_tile_count = total_tiles - len(elf_positions)

    return empty_tile_count


direction_check_order = ['N', 'S', 'W', 'E']

elf_positions = read_input_file()

for round_number in range(10):
    position_proposals = get_move_proposals(
        elf_positions, direction_check_order)

    elf_positions = get_final_positions(position_proposals)

    first_direction = direction_check_order.pop(0)
    direction_check_order.append(first_direction)

empty_tile_count = get_empty_tile_count_within_elf_positions_rect(
    elf_positions)

print(empty_tile_count)
