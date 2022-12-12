import math


class Test:
    def __init__(self, divisor, true_monkey, false_money):
        self.divisor = divisor
        self.true_monkey = true_monkey
        self.false_monkey = false_money

    def __str__(self) -> str:
        output = f'  Test: divisible by {self.divisor}\n'
        output += f'    If true: throw to monkey {self.true_monkey}\n'
        output += f'    If false: throw to monkey {self.false_monkey}\n'
        return output

    def perform(self, worry_value):
        if worry_value % self.divisor == 0:
            return self.true_monkey
        else:
            return self.false_monkey


class Operation:
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.operation = operation

    def __str__(self):
        return f'  Operation: new = {self.left} {self.operation} {self.right}'

    def perform(self, old_value):
        left = self.left
        right = self.right

        if left == 'old':
            left = old_value
        if right == 'old':
            right = old_value

        match self.operation:
            case '*':
                return int(left) * int(right)
            case '+':
                return int(left) + int(right)


class Monkey:
    def __init__(self, items, operation, test):
        self.inspection_count = 0
        self.items = items
        self.operation = operation
        self.test = test

    def __str__(self):
        items_str = ', '.join(map(str, self.items))
        output = 'Monkey:\n'
        output += f'  Starting items: {items_str}\n'
        output += f'{self.operation}\n'
        output += f'{self.test}'

        return output


def parse_monkey(monkey_lines):
    items_line = monkey_lines[1]
    operation_line = monkey_lines[2]

    items = list(map(int, items_line[18:].split(', ')))

    operation_parts = operation_line[19:].split()
    operation = Operation(
        operation_parts[0], operation_parts[2], operation_parts[1])

    divisor = int(monkey_lines[3].split()[-1])
    true_monkey = int(monkey_lines[4].split()[-1])
    false_monkey = int(monkey_lines[5].split()[-1])
    test = Test(divisor, true_monkey, false_monkey)

    return Monkey(items, operation, test)


def parse_input_file():
    file = open('input.txt', 'r')
    lines = file.readlines()

    monkey_info = list()

    for i in range(int(len(lines)/7)+1):
        monkey_info.append(parse_monkey(lines[i*7:(i+1)*7]))
    return monkey_info


monkey_info = parse_input_file()

for _ in range(20):
    for i, monkey in enumerate(monkey_info):
        while len(monkey.items) != 0:
            monkey.inspection_count += 1
            item = monkey.items.pop(0)

            # inspect item
            new_value = monkey.operation.perform(item)
            new_value = math.floor(new_value / 3)

            # perform test
            monkey_to_throw_to = monkey.test.perform(new_value)
            monkey_info[monkey_to_throw_to].items.append(new_value)

inspection_totals = list()
for monkey in monkey_info:
    inspection_totals.append(monkey.inspection_count)
sorted_numbers = sorted(inspection_totals, reverse=True)

print(sorted_numbers[0] * sorted_numbers[1])
