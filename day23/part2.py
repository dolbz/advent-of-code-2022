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

    for i in range(-1, 2):
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

    no_elves_moved = True

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
                    no_elves_moved = False
                    if direction == 'N':
                        proposal_pos = Point(elf_pos.x, elf_pos.y + 1)
                    elif direction == 'E':
                        proposal_pos = Point(elf_pos.x + 1, elf_pos.y)
                    elif direction == 'S':
                        proposal_pos = Point(elf_pos.x, elf_pos.y - 1)
                    else:
                        proposal_pos = Point(elf_pos.x - 1, elf_pos.y)

                    break

        if proposal_pos not in proposal_positions:
            proposal_positions[proposal_pos] = list()
        proposal_positions[proposal_pos].append(elf_pos)
    return (proposal_positions, no_elves_moved)


def get_final_positions(position_proposals):
    final_positions = dict()

    for proposed_pos, proposers in position_proposals.items():
        if len(proposers) == 1:
            final_positions[proposed_pos] = True
        else:
            for proposer_pos in proposers:
                final_positions[proposer_pos] = True

    return final_positions


direction_check_order = ['N', 'S', 'W', 'E']

elf_positions = read_input_file()

round_num = 1

while True:
    (position_proposals, no_elves_moved) = get_move_proposals(
        elf_positions, direction_check_order)

    if no_elves_moved:
        break

    new_elf_positions = get_final_positions(position_proposals)

    if new_elf_positions == elf_positions:
        break

    elf_positions = new_elf_positions

    first_direction = direction_check_order.pop(0)
    direction_check_order.append(first_direction)
    round_num += 1
    if round_num % 100 == 0:
        print(f'Round number {round_num}')


print(f'First round with no moves: {round_num}')
