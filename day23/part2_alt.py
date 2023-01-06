# Alternative implementation for part 2. Uses more of an OO approach and does significantly less redundant
# work each round. I created this when my part 1 implementation never completed for part 2 and I figured it needed
# a less computationally expensive approach.
#
# This implementation _is_ significantly faster but even after a million rounds it still didn't complete.
# On further investigation there was one elf moving continously between the same few positions so it never
# could complete.
#
# It turns out there were bugs in my part 1 implementation (now commented in the part1.py file) that made the
# solution incorrect (but not incorrect enough to get the wrong result for part 1)

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


class ElfPositions:
    def __init__(self, positions_dict):
        self.positions = positions_dict
        self.elfs_with_neighbours = dict()
        self.direction_check_order = ['N', 'S', 'W', 'E']

        for pos in self.positions:
            neighbours = self.get_neighbours(pos)
            if (len(neighbours) > 0):
                # Has a neighbour. Add to neighbour collection
                self.elfs_with_neighbours[pos] = True
                for neighbour in neighbours:
                    self.elfs_with_neighbours[neighbour] = True

    def get_neighbours(self, pos):
        neighbours = list()

        for x in range(pos.x-1, pos.x+2):
            for y in range(pos.y-1, pos.y+2):
                point_to_check = Point(x, y)
                if (point_to_check == pos):
                    continue

                if point_to_check in self.positions:
                    neighbours.append(point_to_check)

        return neighbours

    def move_elf(self, old_pos, new_pos):
        self.positions.pop(old_pos)
        self.positions[new_pos] = True

        # the old pos can't be in the cells with neighbours collection
        # any more as there's no elf there
        if old_pos in self.elfs_with_neighbours:
            self.elfs_with_neighbours.pop(old_pos)

    def update_neighbours(self, newly_occupied_positions):
        updated_elfs_with_neighbours = dict()

        # tidy up existing positions that may or may not have neighbours
        # following the moves
        for elf_with_neighbour in self.elfs_with_neighbours:
            neighbours = self.get_neighbours(elf_with_neighbour)
            if (len(neighbours) > 0):
                # Has a neighbour. Add to neighbour collection
                updated_elfs_with_neighbours[elf_with_neighbour] = True
                for neighbour in neighbours:
                    updated_elfs_with_neighbours[neighbour] = True

        # then add any new cells with neighbours based on the new positions
        for new_position in newly_occupied_positions:
            neighbours = self.get_neighbours(new_position)
            if (len(neighbours) > 0):
                # Has a neighbour. Add to neighbour collection
                updated_elfs_with_neighbours[new_position] = True
                for neighbour in neighbours:
                    updated_elfs_with_neighbours[neighbour] = True

        self.elfs_with_neighbours = updated_elfs_with_neighbours

    def apply_proposals(self, position_proposals):
        new_positions = list()

        no_elves_moved = True

        for proposed_pos, proposers in position_proposals.items():
            if len(proposers) == 1:
                no_elves_moved = False
                self.move_elf(proposers[0], proposed_pos)
                new_positions.append(proposed_pos)

        self.update_neighbours(new_positions)
        return no_elves_moved

    def perform_round(self):
        # Part 1 - get proposed positions
        proposal_positions = dict()
        no_elves_moved = True

        for elf_pos in self.elfs_with_neighbours:
            for direction in self.direction_check_order:
                is_clear = self.check_clear_direction(direction, elf_pos)

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

                    if proposal_pos not in proposal_positions:
                        proposal_positions[proposal_pos] = list()
                    proposal_positions[proposal_pos].append(elf_pos)
                    break

        first_direction = self.direction_check_order.pop(0)
        self.direction_check_order.append(first_direction)

        if no_elves_moved:
            return no_elves_moved

        # Part 2 - apply the proposals if possible
        no_elves_moved = self.apply_proposals(proposal_positions)

        return no_elves_moved

    def check_clear_direction(self, direction, elf_pos):
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

            if pos_to_check in self.positions:
                return False
        return True


def read_input_file():
    file = open('input.txt', 'r')
    lines = file.read().splitlines()

    elf_positions = dict()

    num_of_lines = len(lines)

    for line_num, line in enumerate(lines):
        for x, entry in enumerate(line):
            if entry == '#':
                elf_positions[Point(x, num_of_lines - line_num)] = True

    return ElfPositions(elf_positions)


elf_positions = read_input_file()

round_num = 1

while True:
    if elf_positions.perform_round():
        break

    round_num += 1
    if round_num % 100 == 0:
        print(f'Round number {round_num}')
        print(
            f'Number of elfs with neighbours: {len(elf_positions.elfs_with_neighbours)}')

print(f'First round with no moves: {round_num}')
