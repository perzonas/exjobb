import time
import math
import json

listofdicts = []
listoftuples = []
time_of_disconnect = []
listofstrength = []
total_time = 0
disconnect_time = 0
total_uptime = 0
total_downtime = 0
disconnected = False
started = 0
lowestSignal = 99
highestSignal = 0


### Read all files and add their dicts of information in a single list ###
for i in range(1, 9):
    file = open(("connectiondata/-%d.txt" % i), "r")
    lines = file.readlines()
    for line in lines:
        line = line.replace("\n", "")
    text = "".join(lines)
    list = json.loads(text)
    for dict in list:
        listofdicts.append(dict)
        listoftuples.append((math.floor(int(dict.get("timestamp"))/1000), dict.get("dataStatus")))
        listofstrength.append(dict.get("signalStrength"))


listoftuples.sort()
for i in range(len(listoftuples)-1):
    if listoftuples[i][0] != listoftuples[i+1][0]:
        temp = listoftuples[i+1][0]-listoftuples[i][0]
        total_time += temp
        if listoftuples[i][1] == 2:
            total_uptime += temp
            if disconnected:
                disconnected = False
                time_struct = time.localtime(started)
                time_of_disconnect.append((str(time_struct.tm_hour)+":"+str(time_struct.tm_min)+":"+str(time_struct.tm_sec), disconnect_time))
                disconnect_time = 0
        else:
            if not disconnected:
                disconnected = True
                started = listoftuples[i][0]
            total_downtime += temp
            disconnect_time += temp

listofstrength.sort()
for strength in listofstrength:
    if strength != 99:
        if strength < lowestSignal:
            lowestSignal = strength
        if strength > highestSignal:
            highestSignal = strength
    print(2*strength-113)



print(total_time)
print(total_downtime)
print(total_uptime)
print(time_of_disconnect)
print(lowestSignal)
print(highestSignal)



