import plotly.plotly as py
from plotly.offline import plot
import plotly.io as pio
import plotly.graph_objs as go
import glob
import os
import json


class Draw:

    path = ""
    temp_path = ""
    CENTRALIZED = 1
    STATE = 2
    DELTA = 3
    bytes_average = []
    messagesize_average = []
    messagesize_min = []
    messagesize_max = []
    messagelatency_average = []
    messagelatency_min = []
    messagelatency_max = []
    mergelatency_average = []
    mergelatency_min = []
    mergelatency_max = []
    xrange = []



    def perform_writes(self, type):
        self.path = os.path.dirname(os.path.abspath(__file__))
        folders = glob.glob(self.path+"/*")
        ### Create the right graphs for the solutions that has been used ###

        print("### CREATING GRAPHS FROM RESULTS ###")
        self.write_bytes()
        self.write_messagesize()
        self.write_messagelatency()
        self.write_mergelatency()
        if type == self.CENTRALIZED:
            self.write_master_mergelatency()
            self.write_slave_messagelatency()
            self.write_master_messagesize()
            self.write_master_messagelatency()
            self.write_slave_mergelatency()
            self.write_slave_messagesize()
        print("### FINISHED MAKING GRAPHS ###")
        print("### TEST FINISHED -> CLOSING DOWN ###")


    def write_bytes(self):
        sum1 = 0
        sum2 = 0
        bytes = []

        files = glob.glob("rawdata/bytes*")
        data = []
        for i in range(1, len(files)+1):
            file = open("rawdata/bytes"+str(i), "r")
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
                        print("###############")
                        print(element)
                        print("###############")
                if not newList == []:
                    bytes.append(newList)


        for i in range(len(bytes)):
            data.append(go.Bar(x=["Bytes actually sent", "Total bytes attempted to send"], y=bytes[i], name=("Node"+str(i)),
                               text=bytes[i], textposition='auto'))

        for input in bytes:
            sum1 += input[0]
            sum2 += input[1]
        average1 = sum1/len(bytes)
        average2 = sum2/len(bytes)
        data.append(go.Bar(x=["Bytes actually sent", "Total bytes attempted to send"], y=[average1, average2],
                           name="Average across all nodes", text=[average1, average2], textposition='auto'))

        layout = go.Layout(barmode='group', font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'))
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path+"/bytes*")
        plot(figure, filename=(self.path+"/bytes%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(self.path+"/bytes%s.html" % str(len(files) + 1), 0o777)


    def write_messagesize(self):
        files = glob.glob("rawdata/messagesize*")
        data = []
        bytes = []
        for i in range(1, len(files)+1):
            file = open("rawdata/messagesize"+str(i), "r")
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
                bytes.append(newList)

            self.xrange = list(range(1, len(bytes[i-1])+1))
            #data.append(go.Scatter(x=self.xrange, y=bytes[i-1], mode='lines', name=("Node"+str(i))))

        max_length = 0
        for input in bytes:
            if len(input)>max_length:
                max_length = len(input)

        for i in range(max_length):
            total = 0
            min = 999999999999999999
            max = 0
            for j in range(len(bytes)):
                try:
                    if bytes[j][i] < min:
                        min = bytes[j][i]
                    if bytes[j][i] > max:
                        max = bytes[j][i]
                    total += bytes[j][i]
                except:
                    pass
            self.messagesize_average.append(total/len(bytes))
            self.messagesize_max.append(max)
            self.messagesize_min.append(min)
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_average, name="Average", mode='lines'))
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_max, name="Maximum", mode='lines'))
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_min, name="Minimum", mode='lines'))


        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      xaxis=dict(title='Sequence number of sent message'),
                      yaxis=dict(title='Size of messages in bytes', type='log'))
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/messagesize*")
        plot(figure, filename=(self.path + "/messagesize%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(self.path + "/messagesize%s.html" % str(len(files) + 1), 0o777)


    def write_messagelatency(self):
        files = glob.glob("rawdata/messagelatency*")
        data = []
        bytes = []
        for i in range(1, len(files) + 1):
            file = open("rawdata/messagelatency" + str(i), "r")
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
                bytes.append(newList)

            self.xrange = list(range(1, len(bytes[i - 1]) + 1))
            #data.append(go.Scatter(x=self.xrange, y=bytes[i - 1], mode='lines', name=("Node" + str(i))))

        max_length = 0
        for input in bytes:
            if len(input) > max_length:
                max_length = len(input)
        for i in range(max_length):
            total = 0
            max = 0
            min = 999999999999999
            for j in range(len(bytes)):
                try:
                    if bytes[j][i] < min:
                        min = bytes[j][i]
                    if bytes[j][i] > max:
                        max = bytes[j][i]
                    total += bytes[j][i]
                except:
                    pass
            self.messagelatency_average.append(total/len(bytes))
            self.messagelatency_max.append(max)
            self.messagelatency_min.append(min)
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_average, name="Average", mode='lines'))
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_max, name="Maximum", mode='lines'))
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_min, name="Minimum", mode='lines'))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time for message to be received in ms', type='log'),
                      xaxis=dict(title='Sequence number of received message'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/messagelatency*")
        plot(figure, filename=(self.path + "/messagelatency%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(self.path + "/messagelatency%s.html" % str(len(files) + 1), 0o777)


    def write_mergelatency(self):
        files = glob.glob("rawdata/mergelatency*")
        data = []
        bytes = []
        for i in range(1, len(files) + 1):
            file = open("rawdata/mergelatency" + str(i), "r")
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
                bytes.append(newList)
            self.xrange = list(range(1, len(bytes[i - 1]) + 1))
            #data.append(go.Scatter(x=self.xrange, y=bytes[i - 1], mode='lines', name=("Node" + str(i))))

        max_length = 0
        for input in bytes:
            if len(input)>max_length:
                max_length = len(input)
        for i in range(max_length):
            total = 0
            min = 999999999999999
            max = 0
            for j in range(len(bytes)):
                try:
                    if bytes[j][i] < min:
                        min = bytes[j][i]
                    if bytes[j][i] > max:
                        max = bytes[j][i]
                    total += bytes[j][i]
                except:
                    pass
            self.mergelatency_average.append(total/len(bytes))
            self.mergelatency_max.append(max)
            self.mergelatency_min.append(min)
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_average, name="Average", mode='lines'))
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_max, name="Maximum", mode='lines'))
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_min, name="Minimum", mode='lines'))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time to perform an operation in ms', type='log'),
                      xaxis=dict(title='Sequence number of performed operation'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mergelatency*")
        plot(figure, filename=(self.path + "/mergelatency%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(self.path + "/mergelatency%s.html" % str(len(files) + 1), 0o777)


    def write_slave_mergelatency(self):
        files = glob.glob("testdata/mergelatency*")
        data = []
        bytes = []
        for i in range(2, len(files) + 1):
            file = open("testdata/mergelatency" + str(i), "r")
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
                bytes.append(newList)
            self.xrange = list(range(1, len(bytes[i - 2]) + 1))
            data.append(go.Scatter(x=self.xrange, y=bytes[i - 2], mode='lines', name=("Node" + str(i))))
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_average, mode='lines'))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time to perform an operation in ms', type='log'),
                      xaxis=dict(title='Sequence number of performed operation'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/slavemergelatency*")
        plot(figure, filename=(self.path + "/slavemergelatency%s.html" % str(len(files)+1)), auto_open=False)
        os.chmod(self.path + "/slavemergelatency%s.html" % str(len(files) + 1), 0o777)


    def write_master_mergelatency(self):
        data = []
        bytes = []
        file = open("testdata/mergelatency1", "r")
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
            bytes.append(newList)
        self.xrange = list(range(1, len(bytes[0]) + 1))
        data.append(go.Scatter(x=self.xrange, y=bytes[0], mode='lines', name="Node1"))
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_average, mode='lines', name="Average message size"))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time to perform an operation in ms', type='log'),
                      xaxis=dict(title='Sequence number of performed operation'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mastermergelatency*")
        plot(figure, filename=(self.path + "/mastermergelatency%s.html" % str(len(files)+1)), auto_open=False)
        os.chmod(self.path + "/mastermergelatency%s.html" % str(len(files) + 1), 0o777)


    def write_slave_messagelatency(self):
        files = glob.glob("testdata/messagelatency*")
        data = []
        bytes = []
        for i in range(2, len(files) + 1):
            file = open("testdata/messagelatency" + str(i), "r")
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
                bytes.append(newList)
            self.xrange = list(range(1, len(bytes[i - 2]) + 1))
            data.append(go.Scatter(x=self.xrange, y=bytes[i - 2], mode='lines', name=("Node" + str(i))))
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_average, mode='lines'))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time for a message to be received in ms', type='log'),
                      xaxis=dict(title='Sequence number of received message'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/slavemessagelatency*")
        plot(figure, filename=(self.path + "/slavemessagelatency%s.html" % str(len(files)+1)), auto_open=False)
        os.chmod(self.path + "/slavemessagelatency%s.html" % str(len(files) + 1), 0o777)


    def write_master_messagelatency(self):
        data = []
        bytes = []
        file = open("testdata/messagelatency1", "r")
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
            bytes.append(newList)
        self.xrange = list(range(1, len(bytes[0]) + 1))
        data.append(go.Scatter(x=self.xrange, y=bytes[0], mode='lines', name="Node1"))
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_average, mode='lines', name="Average message size"))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time for a message to be received in ms', type='log'),
                      xaxis=dict(title='Sequence number of received message'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mastermessagelatency*")
        plot(figure, filename=(self.path + "/mastermessagelatency%s.html" % str(len(files)+1)), auto_open=False)
        os.chmod(self.path + "/mastermessagelatency%s.html" % str(len(files) + 1), 0o777)


    def write_slave_messagesize(self):
        files = glob.glob("testdata/messagesize*")
        data = []
        bytes = []
        for i in range(2, len(files) + 1):
            file = open("testdata/messagesize" + str(i), "r")
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
                bytes.append(newList)
            self.xrange = list(range(1, len(bytes[i - 2]) + 1))
            data.append(go.Scatter(x=self.xrange, y=bytes[i - 2], mode='lines', name=("Node" + str(i))))
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_average, mode='lines'))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Size of messages in bytes'),
                      xaxis=dict(title='Sequence number of sent message'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/slavemessagesize*")
        plot(figure, filename=(self.path + "/slavemessagesize%s.html" % str(len(files)+1)), auto_open=False)
        os.chmod(self.path + "/slavemessagesize%s.html" % str(len(files) + 1), 0o777)


    def write_master_messagesize(self):
        data = []
        bytes = []
        file = open("testdata/messagesize1", "r")
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
            bytes.append(newList)
        self.xrange = list(range(1, len(bytes[0]) + 1))
        data.append(go.Scatter(x=self.xrange, y=bytes[0], mode='lines', name="Node1"))
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_average, mode='lines'))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Size of messages in bytes'),
                      xaxis=dict(title='Sequence number of sent message')
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mastermessagesize*")
        plot(figure, filename=(self.path + "/mastermessagesize%s.html" % str(len(files)+1)), auto_open=False)
        os.chmod(self.path + "/mastermessagesize%s.html" % str(len(files) + 1), 0o777)


if __name__ == '__main__':
    #write_bytes()
    data = Draw()
    data.perform_writes(3)

