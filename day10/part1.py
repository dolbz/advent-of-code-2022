instruction_map = {'noop': 1, 'addx': 2}

file = open('input.txt', 'r')
instructions = file.readlines()

x = 1
cycle_count = 0
instruction_pointer = 0
instruction_cycles_remaining = 0
total_signal_strength_at_interesting_points = 0

while instruction_pointer < len(instructions):
    # setup instruction
    instruction_line = instructions[instruction_pointer]
    instruction_and_operands = instruction_line.split()
    instruction_cycles_remaining = instruction_map[instruction_and_operands[0]]

    # execute instruction
    while instruction_cycles_remaining > 0:
        cycle_count += 1
        instruction_cycles_remaining -= 1

        if cycle_count == 20 or ((cycle_count - 20) % 40 == 0):
            total_signal_strength_at_interesting_points += cycle_count * x

    if instruction_and_operands[0] == 'addx':
        x += int(instruction_and_operands[1])

    # increment instruction pointer
    instruction_pointer += 1

print(total_signal_strength_at_interesting_points)
