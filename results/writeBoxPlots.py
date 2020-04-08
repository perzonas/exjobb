import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
import glob
import os
import json


class Draw:

    bytes = []
    data = []

    def writeBoxPlots(self):
        print(px.data.iris())
        path = os.path.dirname(os.path.abspath(__file__))
        folders = os.listdir(path)
        bytes = []
        folders = filter(lambda x: ".py" not in x, folders)
        size = 0
        for folder in folders:
            files = glob.glob(folder + "/bytes*")
            size = len(files)
            for i in range(1, len(files) + 1):
                file = open(folder + "/bytes" + str(i), "r")
                line = file.read()
                file.close()
                try:
                    bytes.append(json.loads(line))
                except:
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    line = line.replace(" ", "")
                    line = line.split(",")
                    newList = []
                    for element in line:
                        try:
                            newList.append(float(element))
                        except:
                            print("################")
                            print(element)
                            print("################")
                    if not newList == []:
                        bytes.append(newList)
            self.data.append(bytes)
            bytes = []

        firstData = self.data[0]
        secondData = self.data[1]
        secondDataSent = []
        secondDataTried = []
        firstDataSent = []
        firstDataTried = []
        for input in firstData:
            firstDataSent.append(input[0])
            firstDataTried.append(input[1])
        for input in secondData:
            secondDataSent.append(input[0])
            secondDataTried.append(input[1])
        dataDict = {
            "Bytes Sent": {"A": firstDataTried,
                           "B": firstDataSent}
        }
        print(firstDataSent)
        print(firstDataTried)
        print(secondDataSent)
        print(secondDataTried)

        fig = px.box(dataDict, x="Bytes Sent", y="Bytes Sent")
        fig.update_traces(quartilemethod="inclusive")
        fig.show()















if __name__ == '__main__':
    data = Draw()
    data.writeBoxPlots()