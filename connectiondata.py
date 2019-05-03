import time
import json

listofdicts = []

for i in range(1, 9):
    file = open(("connectiondata/-%d.txt" % i), "r")
    lines = file.readlines()
    for line in lines:
        line = line.replace("\n", "")
    text = "".join(lines)
    print(i)
    json.loads(text)
    # listofdicts.append(json.loads())

print(listofdicts)
