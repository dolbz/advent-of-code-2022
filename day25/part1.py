def read_input_file():
    file = open('input.txt', 'r')
    return file.read().splitlines()


def parse_snafu_to_int(snafu_string):

    power_of_5 = 0

    int_value = 0

    for pos in reversed(snafu_string):
        if pos == '-':
            pos_int = -1
        elif pos == '=':
            pos_int = -2
        else:
            pos_int = int(pos)

        int_value += pos_int * pow(5, power_of_5)
        power_of_5 += 1

    return int_value


def convert_int_to_snafu(int_value):
    snafu_chars = list()
    carry_next_pos = 0
    while int_value > 0:
        value_at_pos = (int_value % 5) + carry_next_pos
        int_value //= 5

        carry_next_pos = 0

        if value_at_pos == 3:
            carry_next_pos = 1
            value_at_pos = '='
        elif value_at_pos == 4:
            carry_next_pos = 1
            value_at_pos = '-'
        elif value_at_pos == 5:
            carry_next_pos = 1
            value_at_pos = 0

        snafu_chars.insert(0, str(value_at_pos))

    if carry_next_pos == 1:
        snafu_chars.insert(0, str(1))

    return ''.join(snafu_chars)


snafu_lines = read_input_file()

numbers = list()

total = 0

for snafu_string in snafu_lines:
    int_equivalent = parse_snafu_to_int(snafu_string)
    total += int_equivalent

print(f'Total: {total}, as snafu: {convert_int_to_snafu(total)}')
