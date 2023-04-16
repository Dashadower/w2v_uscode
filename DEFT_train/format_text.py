import glob
import re

for index, file in enumerate(glob.glob("t*.txt")):
    print(file)
    data = open(file)
    removed_lines = []
    for line in data.readlines():
        removed_lines.append(re.sub(r'[^A-Za-z0-9 .]+', '', line.split(" ", 1)[1]))

    with open(f"formatted_{index}.txt", "w") as f:
        f.writelines(removed_lines)


