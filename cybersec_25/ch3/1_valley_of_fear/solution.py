coordinates = [
    (0, 8, 3),
    (3, 1, 7),
    (3, 7, 2),
    (6, 0, 4),
    (7, 9, 0)
]

import re

with open('book.txt', 'r') as f:
    content = f.read()

paragraphs = re.split(r'\n\n', content)

lines_p = [p.splitlines() for p in paragraphs]

words = [[line.split() for line in lines] for lines in lines_p]

for c in coordinates:
    print(words[c[0]][c[1]][c[2]])