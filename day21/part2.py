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


def evaluate_monkey_operation(monkeys, monkey_name):
    monkey_op = monkeys[monkey_name]

    if monkey_name == 'humn':
        return None

    if type(monkey_op) is int:
        return monkey_op

    left_value = evaluate_monkey_operation(monkeys, monkey_op.left_operand)
    right_value = evaluate_monkey_operation(monkeys, monkey_op.right_operand)

    if left_value == None or right_value == None:
        return None

    if monkey_op.operator == '+':
        return left_value + right_value
    if monkey_op.operator == '-':
        return left_value - right_value
    if monkey_op.operator == '*':
        return left_value * right_value
    if monkey_op.operator == '/':
        # stops us ending up with a floating point result. It appears as though all divisions have integer results
        return int(left_value / right_value)


def invert_monkey_operation_to_find_unknown(monkeys, unknown_side_monkey, known_outcome):
    if (unknown_side_monkey == 'humn'):
        return known_outcome

    unknown_side_op = monkeys[unknown_side_monkey]

    left_result = evaluate_monkey_operation(
        monkeys, unknown_side_op.left_operand)
    right_result = evaluate_monkey_operation(
        monkeys, unknown_side_op.right_operand)

    if left_result == None:
        unknown_side_monkey = unknown_side_op.left_operand
        result = right_result
    elif right_result == None:
        unknown_side_monkey = unknown_side_op.right_operand
        result = left_result
    else:
        print('should\'t happen')

    if unknown_side_op.operator == '+':
        expected_outcome = known_outcome - result
    if unknown_side_op.operator == '-':
        if left_result == None:
            expected_outcome = known_outcome + result
        if right_result == None:
            expected_outcome = result - known_outcome
    if unknown_side_op.operator == '/':
        if left_result == None:
            expected_outcome = known_outcome * result
        if right_result == None:
            expected_outcome = result / known_outcome
    if unknown_side_op.operator == '*':
        expected_outcome = int(known_outcome / result)

    return invert_monkey_operation_to_find_unknown(
        monkeys, unknown_side_monkey, expected_outcome)


def find_human_unknown(monkeys):
    root_operation = monkeys['root']
    left_result = evaluate_monkey_operation(
        monkeys, root_operation.left_operand)
    right_result = evaluate_monkey_operation(
        monkeys, root_operation.right_operand)

    if left_result == None:
        unknown_side_monkey = root_operation.left_operand
        result = right_result
    elif right_result == None:
        unknown_side_monkey = root_operation.right_operand
        result = left_result

    return invert_monkey_operation_to_find_unknown(monkeys, unknown_side_monkey, result)


monkeys = read_input_file()
result = find_human_unknown(monkeys)

print(result)
