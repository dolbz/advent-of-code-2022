
file = open('input.txt', 'r')
lines = file.readlines()

largest_total = 0
current_total = 0

for line in lines:
    if line == '\n':
        current_total = 0
    else:
        current_total += int(line)

        if current_total > largest_total:
            largest_total = current_total

print(str(largest_total))
