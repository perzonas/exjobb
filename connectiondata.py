import time
import math
import json
import os

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
number_of_signals = 0
sum_of_signals = 0
average_disconnect = []


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
average_disconnect.append(listoftuples[0][0])
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
                average_disconnect.append(started)
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
        number_of_signals += 1
        sum_of_signals += strength
        if strength < lowestSignal:
            lowestSignal = strength
        if strength > highestSignal:
            highestSignal = strength

average = sum_of_signals/number_of_signals
dBm = average*2-113
linelist = []


#### Create strings and print the values of the uptime and downtime of the connection ####

str_percentage = "Percentage of downtime: %f" % (total_downtime/total_time*100)
linelist.append(str_percentage)
print(str_percentage)
str_total_time = "Total number of seconds: %d" % total_time
linelist.append(str_total_time)
print(str_total_time)
str_total_downtime = "Total number of secodns disconnected: %d" % total_downtime
linelist.append(str_total_downtime)
print(str_total_downtime)
str_total_uptime = "Total number of seconds connected: %d" % total_uptime
linelist.append(str_total_uptime)
print(str_total_uptime)


#### Create strings and print values about the disconnects and their occurrence ####

str_timeof_disconnect = "Time of disconnect and Seconds each disconnect lasted: " + json.dumps(time_of_disconnect)
linelist.append(str_timeof_disconnect)
print(str_timeof_disconnect)
average_total = 0

for i in range(len(average_disconnect)-1):
    average_total += average_disconnect[i+1]-average_disconnect[i]
average_disconnect_between = average_total/(len(average_disconnect)-1)
seconds = average_disconnect_between%60
minutes = average_disconnect_between/60
hours = minutes/60
minutes = minutes%60
str_average_dc_time = "Average time between disconnects: %d:%d:%d" % (hours, minutes, seconds)
linelist.append(str_average_dc_time)
print(str_average_dc_time)


#### Create strings and print values about the signal strength and the signal performance ####


str_average_signal = ("Average signal strength: %f" % average)
linelist.append(str_average_signal)
str_average_dbm = ("dBm of average signal: %f" % dBm)
linelist.append(str_average_dbm)
str_lowest_signal = ("Lowest signal state measured: %d" % lowestSignal)
linelist.append(str_lowest_signal)
str_highest_signal = ("Highest signal strength recorded: %d" % highestSignal)
linelist.append(str_highest_signal)
print(str_average_signal)
print(str_average_dbm)
print(str_lowest_signal)
print(str_highest_signal)

connection = ""
if dBm >= -75:
    connection = "High (good voice and data)"
elif dBm >= -90:
    connection = "Medium (good voice and data)"
elif dBm >= -100:
    connection = "Poor (good voice, marginal data with drop outs)"
elif dBm >= -109:
    connection = "Very poor (Voice may be ok and no data)"
else:
    connection = "No signal"

str_signal_performance = ("Average signal strength is classified as: %s" % connection)
linelist.append(str_signal_performance)
print(str_signal_performance)


#### Add newline to all lines as writelines doesn't do this on it's own ####
for i in range(len(linelist)):
    linelist[i] = linelist[i]+"\n"


#### Write all the results to the connection data file ####
file = open("connectiondata/results.txt", "w")
os.chmod("connectiondata/results.txt", 0o777)
file.writelines(linelist)
file.close()





