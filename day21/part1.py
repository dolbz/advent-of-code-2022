class Operation:
    def __init__(self, operator, left_operand, right_operand):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand


def read_input_file():
    file = open('input.txt', 'r')
    lines = file.readlines()

    # example lines...
    # ljgn: 2
    # sjmn: drzm * dbpl

    monkeys = dict()

    for line in lines:
        line_parts = line.strip().split()

        monkey_name = line_parts[0][:-1]

        if len(line_parts) == 2:
            # it's a constant
            monkeys[monkey_name] = int(line_parts[1])
        else:
            monkeys[monkey_name] = Operation(
                operator=line_parts[2],
                left_operand=line_parts[1],
                right_operand=line_parts[3]
            )
    return monkeys


def evaluate_from_root(monkeys):
    return evaluate_monkey_operation(monkeys, 'root')


def evaluate_monkey_operation(monkeys, monkey_name):
    monkey_op = monkeys[monkey_name]

    if type(monkey_op) is int:
        return monkey_op

    left_value = evaluate_monkey_operation(monkeys, monkey_op.left_operand)
    right_value = evaluate_monkey_operation(monkeys, monkey_op.right_operand)

    if monkey_op.operator == '+':
        return left_value + right_value
    if monkey_op.operator == '-':
        return left_value - right_value
    if monkey_op.operator == '*':
        return left_value * right_value
    if monkey_op.operator == '/':
        # stops us ending up with a floating point result. It appears as though all divisions have integer results
        return int(left_value / right_value)


monkeys = read_input_file()

result = evaluate_from_root(monkeys)

print(result)
