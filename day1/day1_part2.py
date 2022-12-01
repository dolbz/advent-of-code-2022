
file = open('input.txt', 'r')
lines = file.readlines()

totals = list()
current_total = 0

for line in lines:
    if line == '\n':
        totals.append(current_total)
        current_total = 0
    else:
        current_total += int(line)

totals.append(current_total)
totals.sort(reverse=True)

top3_total = 0
for i in range(3):
    top3_total += totals[i]

print(str(top3_total))
