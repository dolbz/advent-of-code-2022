import collections
import sys

file = open('input.txt', 'r')
input = file.read()

unique_count = int(sys.argv[1])

char_queue = collections.deque(maxlen=unique_count)

for i, char in enumerate(input):
  char_queue.append(char)
  queue_set = set(char_queue)
  if len(queue_set) == unique_count:
    print(i+1)
    break