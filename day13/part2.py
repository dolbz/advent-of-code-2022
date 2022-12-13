import functools


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

    packets = list()

    for line in lines:
        if len(line) > 1:
            packets.append(parse_packet(line))

    return packets


def are_in_order(left, right, depth=0):
    pad = depth * ' '
    #print(f'{pad}Compare {left} vs {right}')
    pad += '  '
    # special case for if left has no items but right has some
    if len(left) == 0 and len(right) > 0:
        return True
    for index, item_left in enumerate(left):
        #print(f'index {index} left {left}')
        if index > len(right) - 1:
            # ran out of items on right
            #print(f'{pad}Right side ran out of items, so inputs are not in the right order')
            return False

        item_right = right[index]

        # if type(item_left) is int and type(item_right) is int:
        #print(f'{pad}Compare {item_left} vs {item_right}')

        if type(item_left) is list or type(item_right) is list:
            if type(item_left) != list:
                #print(f'{pad}promoting {item_left} to [{item_left}]')
                item_left = [item_left]
            if type(item_right) != list:
                #print(f'{pad}promoting {item_right} to [{item_right}]')
                item_right = [item_right]
            sub_list_is_in_order = are_in_order(item_left, item_right, depth+2)
            if sub_list_is_in_order is not None:
                return sub_list_is_in_order
        elif item_left < item_right:
            #print(f'{pad}  Left side is smaller, so inputs are in the right order')
            return True
        elif item_left > item_right:
            #print(f'{pad}  Right side is smaller, so inputs are not in the right order')
            return False
        # special case for if left runs out of items but right has more
        if index == len(left) - 1 and len(right) > len(left):
            return True
    return None


def compare(left, right):
    # the existing are_in_order(left, right) function almost makes a perfect comparison function
    # adapt its result for what we need to sort the list fully
    in_order = are_in_order(left, right)

    if in_order is None or in_order:
        return -1
    else:
        return 1


packets = parse_input_file()
sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))

divider_indices_product = 1

for i, packet in enumerate(sorted_packets):
    # look specifically for the [[2]] and [[6]] packets that were added
    if len(packet) == 1 and type(packet[0]) is list and len(packet[0]) == 1 and (packet[0][0] == 2 or packet[0][0] == 6):
        divider_indices_product *= i+1

    print(f'{i+1}: {packet}')

print()
print(f'Decoder key: {divider_indices_product}')
