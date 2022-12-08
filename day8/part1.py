file = open('input.txt', 'r')
rows = file.readlines()

columns = list()
visibilities = list()

edge_size = len(rows)

for i in range(edge_size):
  columns.append("")
  visibilities.append(list())
  for j in range(edge_size):
    columns[i] += rows[j][i]
    visibilities[i].append(False)

for i in range(edge_size):
  largest_tree_left = -1
  largest_tree_right = -1
  largest_tree_down = -1
  largest_tree_up = -1

  row = rows[i]
  column = columns[i]

  for j in range(edge_size):
    left_tree_size = int(row[j])
    right_tree_size = int(row[edge_size-j-1])

    down_tree_size = int(column[j])
    up_tree_size = int(column[edge_size-j-1])

    if left_tree_size > largest_tree_left:
      largest_tree_left = left_tree_size
      visibilities[i][j] = True
    if right_tree_size > largest_tree_right:
      largest_tree_right = right_tree_size
      visibilities[i][edge_size-j-1] = True
    if down_tree_size > largest_tree_down:
      largest_tree_down = down_tree_size
      visibilities[j][i] = True
    if up_tree_size > largest_tree_up:
      largest_tree_up = up_tree_size
      visibilities[edge_size-j-1][i] = True

visible_tree_count = 0
for row in visibilities:
  for value in row:
    if value:
      visible_tree_count += 1

print(visible_tree_count)