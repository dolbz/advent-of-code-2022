def parse_packet(line):
    packet = None
    line = line.strip()

    line_index = 0
    list_stack = list()

    while line_index < len(line):
        current_char = line[line_index]

        if current_char == '[':
            new_list = list()
            if len(list_stack) > 0:
                list_stack[-1].append(new_list)
            list_stack.append(new_list)
        elif current_char == ']':
            packet = list_stack.pop()
        elif current_char == ',':
            pass
        else:
            start_index = line_index
            while line_index < len(line) and line[line_index] != ',' and line[line_index] != ']':
                line_index += 1

            list_stack[-1].append(int(line[start_index:line_index]))
            line_index -= 1

        line_index += 1
    return packet


def parse_input_file():
    file = open('input.txt', 'r')
    lines = file.readlines()

    packet_pairs = list()

    packet_pairs_count = int((len(lines)/3) + 1)
    for pair_index in range(packet_pairs_count):
        left = parse_packet(lines[pair_index*3])
        right = parse_packet(lines[(pair_index*3)+1])
        packet_pairs.append((left, right))

    return packet_pairs


def are_in_order(left, right, depth=0):
    pad = depth * ' '
    print(f'{pad}Compare {left} vs {right}')
    pad += '  '

    # special case for if left has no items but right has some
    if len(left) == 0 and len(right) > 0:
        return True

    for index, item_left in enumerate(left):
        if index > len(right) - 1:
            # ran out of items on right
            print(
                f'{pad}Right side ran out of items, so inputs are not in the right order')
            return False

        item_right = right[index]

        if type(item_left) is int and type(item_right) is int:
            print(f'{pad}Compare {item_left} vs {item_right}')

        if type(item_left) is list or type(item_right) is list:
            if type(item_left) != list:
                print(f'{pad}promoting {item_left} to [{item_left}]')
                item_left = [item_left]
            if type(item_right) != list:
                print(f'{pad}promoting {item_right} to [{item_right}]')
                item_right = [item_right]
            sub_list_is_in_order = are_in_order(item_left, item_right, depth+2)
            if sub_list_is_in_order is not None:
                return sub_list_is_in_order
        elif item_left < item_right:
            print(f'{pad}  Left side is smaller, so inputs are in the right order')
            return True
        elif item_left > item_right:
            print(
                f'{pad}  Right side is smaller, so inputs are not in the right order')
            return False

        # special case for if left runs out of items but right has more
        if index == len(left) - 1 and len(right) > len(left):
            return True
    return None


packet_pairs = parse_input_file()

total_of_indices = 0
for i in range(len(packet_pairs)):
    (left, right) = packet_pairs[i]
    in_order = are_in_order(left, right)
    if in_order is None or in_order:
        total_of_indices += i+1
    print()


print(f'Sum of indices in order: {total_of_indices}')
