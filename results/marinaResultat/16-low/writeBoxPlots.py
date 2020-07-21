import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import glob
import os
import json
from plotly.offline import plot


BYTES = 1
MERGE = 2
LATENCY = 3
SIZE = 4


class Draw:

    centralized = []
    perfect = []
    delta = []
    state = []

    bytes = []
    data = []

    def getFileType(self, testType):
        if testType == BYTES:
            return "/bytes"
        elif testType == MERGE:
            return "/mergelatency"
        elif testType == LATENCY:
            return "/messagelatency"
        else:
            return "/messagesize"

    def getColor(self, system):
        if system == 'Centrally Managed':
            return 'rgb(5, 5, 134)'
        elif system == 'Reference System':
            return 'rgb(5, 134, 5)'
        elif system == 'State-CRDT':
            return 'rgb(134,5,5)'
        else:
            return 'rgb(134, 4, 134)'

    def getFileTypeForPrinting(self, testType):
        if testType == BYTES:
            return "-bytes"
        elif testType == MERGE:
            return "-mergelatency"
        elif testType == LATENCY:
            return "-messagelatency"
        else:
            return "-messagesize"

    def getYaxisForPrinting(self, testType):
        if testType == BYTES:
            return "<B>Size of messages sent across the network in bytes</B>"
        elif testType == MERGE:
            return "<B>Time to complete a merge action in ms</B>"
        elif testType == LATENCY:
            return "<B>Time to send a message between nodes in ms</B>"
        else:
            return "<B>Size of messages sent in bytes</B>"

    def addToArray(self, folder, data):
        if folder == "centralized":
            self.centralized.extend(data)
        elif folder == "delta":
            self.delta.extend(data)
        elif folder == "perfect":
            self.perfect.extend(data)
        else:
            self.state.extend(data)

    def writeBoxPlots(self, testType):
        print(px.data.iris())
        path = os.path.dirname(os.path.abspath(__file__))
        folders = os.listdir(path)
        bytes = []
        folders = filter(lambda x: ".py" not in x, folders)
        size = 0
        for folder in folders:
            files = glob.glob(folder + self.getFileType(testType) + "*")
            size = len(files)
            for i in range(1, size + 1):
                file = open(folder + self.getFileType(testType) + str(i), "r")
                line = file.read()
                file.close()
                try:
                    bytes.append(json.loads(line))
                    self.addToArray(folder, json.loads(line))
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
                        self.addToArray(folder, newList)
            self.data.append(bytes)
            bytes = []
        self.state.sort()
        print("**************")
        print(self.centralized)
        print(self.state)
        print("***************")
        print("Centralized max: %f min: %f", max(self.centralized), min(self.centralized))
        print("State max: %f min: %f", max(self.state), min(self.state))
        print("delta max: %f min: %f", max(self.delta), min(self.delta))
        print("perfect max: %f min: %f", max(self.perfect), min(self.perfect))

        systems = ['Reference System', 'Centrally Managed', 'State-CRDT', 'Delta-CRDT']
        testDict = {
            "Centrally Managed": self.centralized,
            "Reference System": self.perfect,
            "State-CRDT": self.state,
            "Delta-CRDT": self.delta
        }



        for system in systems:
            name = system+self.getFileTypeForPrinting(testType)
            lista = sorted(testDict.get(system))
            f = open(name, "w")
            f.write(json.dumps(lista))
            f.close()



        fig = go.Figure()

        for system in systems:
           fig.add_trace(
                go.Box(
                   y=testDict.get(system),
                    name=system,
                    boxpoints=False,
                    marker=dict(color=self.getColor(system)),
                    boxmean=True

                )
            )
            # fig.add_trace(
            #     go.Box(
            #         y=testDict.get(system),
            #         boxpoints='all',
            #         name=system,
            #         pointpos=2,
            #         jitter=0.8,
            #         marker=dict(color=self.getColor(system), opacity=0.7),
            #         line=dict(color='rgba(0,0,0,0)'),
            #         fillcolor='rgba(0,0,0,0)'
            #          ))
        fig.update_traces(quartilemethod="inclusive")
        fig.update_layout(
            yaxis_type="log",
            boxgap=0.01,
            yaxis_title=self.getYaxisForPrinting(testType),
            xaxis_title="<B>Name Of System tested</B>",
            font=dict(
                family="Raleway, Balto",
                size=36,
                color="#000000"
            )
        )
        fig.update_xaxes(tickfont=dict(color='black', size=32))
        fig.update_yaxes(gridwidth=0.5, gridcolor='rgba(155,155,155,1)', tickfont=dict(color='black', size=32))
        #fig.update_yaxes(gridwidth=0.5, gridcolor='rgba(155,155,155,1)', tickvals=[100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000], tickfont=dict(color='black', size=32))
        fig.show()
        plot(fig, filename=(path + "/" + self.getFileTypeForPrinting(testType) + ".html"), auto_open=False)
        os.chmod((path + "/" + self.getFileTypeForPrinting(testType) + ".html"), 0o777)

        # fig = px.box(dataDict, x="Bytes Sent", y="Bytes Sent")
        # fig.update_traces(quartilemethod="inclusive")
        # fig.show()





if __name__ == '__main__':
    data = Draw()
    data.writeBoxPlots(LATENCY)


#BYTES = 1
#MERGE = 2
#LATENCY = 3
#SIZE = 4