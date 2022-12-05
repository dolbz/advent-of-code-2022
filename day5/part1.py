def main():
  file = open('input.txt', 'r')
  lines = file.readlines()

  stack_config_lines = list()
  instruction_lines = list()

  after_break = False

  for line in lines:
    if len(line) == 1:
      after_break = True
      continue
    if (after_break):
      instruction_lines.append(line)
    else:
      stack_config_lines.append(line)

  stacks = extract_stacks_from_lines(stack_config_lines[:-1])
  instructions = extract_instructions_from_lines(instruction_lines)

  perform_moves(stacks, instructions)

  top_of_stacks = ''
  for stack in stacks:
    top_of_stacks += stack.pop()
  
  print(top_of_stacks)

def extract_instructions_from_lines(instruction_lines):
  instructions = list()
  for instruction_line in instruction_lines:
    parts = instruction_line.split()
    instructions.append((int(parts[1]), int(parts[3]), int(parts[5])))

  return instructions

def extract_stacks_from_lines(stackConfigLines):
  stacks_collection = list()

  for _ in range(int(len(stackConfigLines[0]) / 4)):
    stacks_collection.append(list())

  for line in reversed(stackConfigLines):
    for i, character in enumerate(line):
      if (i - 1) % 4 == 0 and character != ' ':
        stacks_collection[int((i-1) / 4)].append(character)

  return stacks_collection

def perform_moves(stacks, instructions):
  for (num, start_stack, end_stack) in instructions:
    for _ in range(num):
      item = stacks[start_stack-1].pop()
      stacks[end_stack-1].append(item)

main()