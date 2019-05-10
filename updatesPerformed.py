import os

for i in range(3):
    if i == 0:
        file = open("connectiondata/updatesinfo2.txt", "r")
    elif i == 1:
        file = open("connectiondata/updatesinfo3.txt", "r")
    else:
        file = open("connectiondata/updatesinfo.txt", "r")
    lines = file.readlines()
    file.close()
    saved_data = []
    for line in lines:
        temp = line.split(",")
        saved_data.append((temp[0], temp[2]))

    saved_data.sort()
    highest_updates = 0
    total_updates = 0
    for tuple in saved_data:
        total_updates += int(tuple[1])
        if int(tuple[1]) > highest_updates:
            highest_updates = int(tuple[1])

    if i == 0:
        average = "Average total updates/hour: %f\n" % (total_updates/3/len(saved_data))
        vehicleaverage = "Average updates every hour/vehicles: %f\n" % ((total_updates/3/len(saved_data))/13)
        file = open("connectiondata/updateinformation2.txt", "w")
    elif i == 1:
        average = "Average total updates/hour: %f\n" % (total_updates / len(saved_data))
        vehicleaverage = "Average updates every hour/vehicles: %f\n" % ((total_updates / len(saved_data)) / 13)
        file = open("connectiondata/updateinformation3.txt", "w")
    else:
        average = "Average total updates/hour: %f\n" % ((total_updates*2) / len(saved_data))
        vehicleaverage = "Average updates every hour/vehicles: %f\n" % (((total_updates*2) / len(saved_data)) / 13)
        file = open("connectiondata/updateinformation.txt", "w")


    file.write(average)
    file.write(vehicleaverage)
    if i == 0:
        file.write("Highest number of updates in a 3 hour window: %d\n" % highest_updates)
    elif i == 1:
        file.write("Highest number of updates in a 1 hour window: %d\n" % highest_updates)
    else:
        file.write("Highest number of updates in a 30min window: %d\n" % highest_updates)
    file.write("Number of active vehicles during testing: 13\n")
    os.chmod("connectiondata/updateinformation.txt", 0o777)
    file.close()