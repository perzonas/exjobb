import plotly.express as px
import plotly
import plotly.io as pio
import plotly.graph_objs as go
import glob
import os
import json
import pandas as pd


class Draw:

    bytes = []
    data = []

    def writeBoxPlots(self):
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
        thirdData = self.data[2]
        secondDataSent = []
        secondDataTried = []
        firstDataSent = []
        firstDataTried = []
        thirdDataSent = []
        thirdDataTried = []
        values = []
        test = []
        value = []
        for input in firstData:
            firstDataSent.append(input[0])
            firstDataTried.append(input[1])
        for input in secondData:
            secondDataSent.append(input[0])
            secondDataTried.append(input[1])
        for input in thirdData:
            thirdDataSent.append(input[0])
            thirdDataTried.append(input[1])

        for data in firstDataSent:
            values.append(data)
            value.append("Bytes sent")
            test.append("5 sec broadcast rate /\n 5.4% disconnect rate")
        for data in firstDataTried:
            values.append(data)
            value.append("Bytes tried to send")
            test.append("5 sec broadcast rate /\n 5.4% disconnect rate")
        for data in secondDataSent:
            values.append(data)
            value.append("Bytes sent")
            test.append("35 sec broadcast rate /\n 1.35% disconnect rate")
        for data in secondDataTried:
            values.append(data)
            value.append("Bytes tried to send")
            test.append("35 sec broadcast rate /\n 1.35% disconnect rate")
        for data in thirdDataSent:
            values.append(data)
            value.append("Bytes sent")
            test.append("5 sec broadcast rate /\n 1.35% disconnect rate")
        for data in thirdDataTried:
            values.append(data)
            value.append("Bytes tried to send")
            test.append("5 sec broadcast rate /\n 1.35% disconnect rate")

        print(firstDataSent)
        print(firstDataTried)
        print(secondDataSent)
        print(secondDataTried)

        dataDict = {
            "Bytes": values,
            "Test: ": test,
            "Type": value
        }

        dataFrame = pd.DataFrame(dataDict)
        print(dataFrame)

        fig = px.box(dataFrame, x="Bytes", y="Type", color="Test: ", orientation='h', log_x=True, points=False)
        fig.update_traces(quartilemethod="inclusive")
        fig.update_xaxes(title_font=dict(size=18), tickfont=dict(size=16))
        fig.update_yaxes(tickangle=270, title_font=dict(size=18), tickfont=dict(size=16))
        fig.update_layout(legend_orientation='h')
        fig.show()
        plotly.offline.plot(fig, "file.html")















if __name__ == '__main__':
    data = Draw()
    data.writeBoxPlots()