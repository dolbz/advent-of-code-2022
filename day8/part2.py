def find_distance(this_tree_height, trees):
  count = 0
  for height in trees:
    count += 1
    if this_tree_height <= height:
      break

  return count

def view_right(row, column):
  this_tree_height = rows[row][column]
  trees_right = rows[row][column+1:]

  return find_distance(this_tree_height, trees_right)

def view_left(row, column):
  this_tree_height = rows[row][column]
  trees_left = rows[row][:column][::-1]

  return find_distance(this_tree_height, trees_left)

def view_up(row, column):
  this_tree_height = rows[row][column]
  trees_up = columns[column][:row][::-1]

  return find_distance(this_tree_height, trees_up)

def view_down(row, column):
  this_tree_height = rows[row][column]
  trees_down = columns[column][row+1:]
  return find_distance(this_tree_height, trees_down)

file = open('input.txt', 'r')
rows = file.read().splitlines()

columns = list()

edge_size = len(rows)

highest_scenic_score = 0

for i in range(edge_size):
  columns.append("")
  for j in range(edge_size):
    columns[i] += rows[j][i]

for row in range(edge_size):
  for column in range(edge_size):
    right = view_right(row, column)
    left = view_left(row, column)
    up = view_up(row, column)
    down = view_down(row, column)

    scenic_score = right * left * up * down
    if scenic_score > highest_scenic_score:
      highest_scenic_score = scenic_score
  

print(highest_scenic_score)