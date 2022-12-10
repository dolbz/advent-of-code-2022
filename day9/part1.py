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


file = open('input.txt', 'r')
moves = file.readlines()

head_positions = list()
tail_positions = list()

head_positions.append(Point(0, 0))
tail_positions.append(Point(0, 0))

for move in moves:
    parts = move.split()

    direction = parts[0]
    num_of_steps = int(parts[1])

    x_diff = 0
    y_diff = 0

    match direction:
        case 'U':
            y_diff = 1
        case 'D':
            y_diff = -1
        case 'L':
            x_diff = -1
        case 'R':
            x_diff = 1

    for i in range(num_of_steps):
        current_head_pos = head_positions[-1]
        current_tail_pos = tail_positions[-1]

        new_head_pos = Point(current_head_pos.x + x_diff,
                             current_head_pos.y + y_diff)
        new_tail_pos = current_tail_pos

        if abs(new_head_pos.x - current_tail_pos.x) > 1 or abs(new_head_pos.y - current_tail_pos.y) > 1:
            new_tail_pos = Point(new_head_pos.x + (x_diff*-1),
                                 new_head_pos.y + (y_diff*-1))
            print(new_tail_pos)

        head_positions.append(new_head_pos)
        if current_tail_pos != new_tail_pos:
            tail_positions.append(new_tail_pos)

print(len(set(tail_positions)))
