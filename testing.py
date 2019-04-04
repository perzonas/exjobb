import time

while True:

    reproduce = None
    action = ""

    ### Read file that holds local updates ###
    file = open("localstates/local2", "r")
    text = file.readlines()

    if text:
        action = text[0]
        print(action)
        if len(text) > 1:
            reproduce = text[1:]
            print(reproduce)
    file.close()

    ### Update the file and remove the line that will be performed if there was an update in the file ###
    if text:
        file = open("localstates/local2", "w")
        if reproduce:
            for line in reproduce:
                file.write(line)
        else:
            file.write("")
        file.close()

    time.sleep(2)
