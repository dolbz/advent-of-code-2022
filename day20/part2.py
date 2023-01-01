def read_input_file():
    file = open('input.txt', 'r')
    lines = file.readlines()

    return [(int(line) * 811589153, False) for line in lines]


encrypted_message = read_input_file()

for _ in range(len(encrypted_message)):
    current_index = 0
    current_number = 0

    for index, (number, already_processed) in enumerate(encrypted_message):
        if not already_processed:
            current_index = index
            current_number = number
            break
    new_index = current_index + current_number

    if new_index >= len(encrypted_message):
        new_index = new_index % (len(encrypted_message) - 1)
    elif new_index < 0:
        true_change = (abs(current_number) % (len(encrypted_message) - 1)) * -1
        new_index = len(encrypted_message) - 1 + true_change

    encrypted_message.pop(current_index)
    encrypted_message.insert(new_index, (number, True))

message_numbers_only = [number for (number, _) in encrypted_message]
print(message_numbers_only)

while message_numbers_only[0] != 0:
    num = message_numbers_only.pop(0)
    message_numbers_only.append(num)

coord1 = message_numbers_only[1000 % len(message_numbers_only)]
coord2 = message_numbers_only[2000 % len(message_numbers_only)]
coord3 = message_numbers_only[3000 % len(message_numbers_only)]

print(f'{coord1}, {coord2}, {coord3}')
print(coord1 + coord2 + coord3)
