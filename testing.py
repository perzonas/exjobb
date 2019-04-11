import time
import json
from DbConnect import *

data = (1, "hi", 98)
print(data)
string = json.dumps(data)
print(string)
(a, b, c) = json.loads(string)
print(a, b, c)
data = (a, b, c)
print(data)


content = {'customers': [], 'heaps': [], 'loads': [], 'loads_waybills': [],
                                      'materials': [(1, 'gravel', 1554371143, '345')], 'table_properties': [],
                                      'targets': [], 'waybills': []}


if slavedbentryexist("2", "2", "materials", [1, 'gravel', 1554371143, '345']):
    print("Truesd")
else:
    print("FALSE")
time.sleep(20)