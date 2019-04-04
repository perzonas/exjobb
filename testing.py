import time
import json

data = (1, "hi", 98)
print(data)
string = json.dumps(data)
print(string)
(a, b, c) = json.loads(string)
print(a, b, c)
data = (a, b, c)
print(data)
time.sleep(2)
