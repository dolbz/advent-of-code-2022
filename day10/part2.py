def renderToBuffer(screen_buffer, cycle_count, x):
    pos_in_line = cycle_count % 40
    if pos_in_line < x - 1 or pos_in_line > x + 1:
        screen_buffer[cycle_count] = '.'
    else:
        screen_buffer[cycle_count] = '#'


instruction_map = {'noop': 1, 'addx': 2}

file = open('input.txt', 'r')
instructions = file.readlines()

x = 1
cycle_count = 0
instruction_pointer = 0
instruction_cycles_remaining = 0
screen_buffer = list(' ' * 240)

while instruction_pointer < len(instructions):
    # setup instruction
    instruction_line = instructions[instruction_pointer]
    instruction_and_operands = instruction_line.split()
    instruction_cycles_remaining = instruction_map[instruction_and_operands[0]]

    # execute instruction
    while instruction_cycles_remaining > 0:
        renderToBuffer(screen_buffer, cycle_count, x)
        cycle_count += 1
        instruction_cycles_remaining -= 1

    if instruction_and_operands[0] == 'addx':
        x += int(instruction_and_operands[1])

    # increment instruction pointer
    instruction_pointer += 1

# render the screen buffer
if cycle_count != 0 and cycle_count % 240 == 0:
    for i in range(240):
        print() if i % 40 == 0 and i != 0 else ''
        print(screen_buffer[i], end='')
print()
