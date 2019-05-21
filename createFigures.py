import plotly.plotly as py
from plotly.offline import plot
import plotly.io as pio
import plotly.graph_objs as go
import glob
import os
import json

class Draw:

    path = ""
    CENTRALIZED = 1
    STATE = 2
    DELTA = 3


    def perform_writes(self, type):
        ### Create a directory for all the graphs
        if type == self.CENTRALIZED:
            files = os.listdir("results/")
            count = 0
            for file in files:
                if "centralized" in file:
                    count += 1
            self.path = "results/centralized" + str(count+1)
            os.mkdir(self.path)
            os.chmod(self.path, 0o777)

        elif type == self.STATE:
            files = os.listdir("results/")
            count = 0
            for file in files:
                if "state" in file:
                    count += 1
            self.path = "results/state" + str(count + 1)
            os.mkdir(self.path)
            os.chmod(self.path, 0o777)

        elif type == DELTA:
            files = os.listdir("results/")
            count = 0
            for file in files:
                if "delta" in file:
                    count += 1
            self.path = "results/delta" + str(count + 1)
            os.mkdir(self.path)
            os.chmod(self.path, 0o777)

        ### Create the right graphs for the solutions that has been used ###
        if type == self.CENTRALIZED:
            self.write_master_mergelatency()
            self.write_slave_messagelatency()
            self.write_master_messagesize()
            self.write_master_messagelatency()
            self.write_slave_mergelatency()
            self.write_slave_messagesize()
        self.write_bytes()
        self.write_messagesize()
        self.write_messagelatency()
        self.write_mergelatency()





    def write_bytes(self):
        sum1 = 0
        sum2 = 0
        bytes = []

        files = glob.glob("testdata/bytes*")
        data = []
        for i in range(1, len(files)+1):
            file = open("testdata/bytes"+str(i), "r")
            line = file.read()
            bytes.append(json.loads(line))
            file.close()
            data.append(go.Bar(x=["Bytes actually sent", "Total bytes attempted to send"], y=bytes[i-1], name=("Node"+str(i)),
                               text=bytes[i-1], textposition='auto'))

        for input in bytes:
            sum1 += input[0]
            sum2 += input[1]
        average1 = sum1/len(bytes)
        average2 = sum2/len(bytes)
        data.append(go.Bar(x=["Bytes actually sent", "Total bytes attempted to send"], y=[average1, average2],
                           name="Average across all nodes", text=[average1, average2], textposition='auto'))

        layout = go.Layout(barmode='group', title='Number of bytes sent during test')
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path+"/bytes*")
        print(self.path)
        plot(figure, filename=(self.path+"/bytes%s.html" % str(len(files) + 1)), auto_open=False)


    def write_messagesize(self):
        files = glob.glob("testdata/messagesize*")
        data = []
        bytes = []
        for i in range(1, len(files)+1):
            file = open("testdata/messagesize"+str(i), "r")
            line = file.read()
            bytes.append(json.loads(line))
            file.close()
            xrange = list(range(1, len(bytes[i-1])+1))
            data.append(go.Scatter(x=xrange, y=bytes[i-1], mode='lines', name=("Node"+str(i))))

        layout = dict(title='Size of messages sent by nodes',
                      xaxis=dict(title='Number of sent messages'),
                      yaxis=dict(title='Message size (bytes)'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/messagesize*")
        plot(figure, filename=(self.path + "/messagesize%s.html" % str(len(files) + 1)), auto_open=False)


    def write_messagelatency(self):
        files = glob.glob("testdata/messagelatency*")
        data = []
        bytes = []
        for i in range(1, len(files) + 1):
            file = open("testdata/messagelatency" + str(i), "r")
            line = file.read()
            bytes.append(json.loads(line)[1])
            file.close()
            xrange = list(range(1, len(bytes[i - 1]) + 1))
            data.append(go.Scatter(x=xrange, y=bytes[i - 1], mode='lines', name=("Node" + str(i))))

        layout = dict(title='Time for an entire message to be received by the receiver',
                      yaxis=dict(title='Time for message to be received (milliseconds)'),
                      xaxis=dict(title='Received message number'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/messagelatency*")
        plot(figure, filename=(self.path + "/messagelatency%s.html" % str(len(files) + 1)), auto_open=False)


    def write_mergelatency(self):
        files = glob.glob("testdata/mergelatency*")
        data = []
        bytes = []
        for i in range(1, len(files) + 1):
            file = open("testdata/mergelatency" + str(i), "r")
            line = file.read()
            bytes.append(json.loads(line))
            file.close()
            xrange = list(range(1, len(bytes[i - 1]) + 1))
            data.append(go.Scatter(x=xrange, y=bytes[i - 1], mode='lines', name=("Node" + str(i))))

        layout = dict(title='Time for a node to perform an action/merge',
                      yaxis=dict(title='Time for action/merge(milliseconds)'),
                      xaxis=dict(title='Action/merge sequence'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mergelatency*")
        plot(figure, filename=(self.path + "/mergelatency%s.html" % str(len(files) + 1)), auto_open=False)


    def write_slave_mergelatency(self):
        files = glob.glob("testdata/mergelatency*")
        data = []
        bytes = []
        print(files)
        for i in range(2, len(files) + 1):
            file = open("testdata/mergelatency" + str(i), "r")
            line = file.read()
            bytes.append(json.loads(line))
            file.close()
            xrange = list(range(1, len(bytes[i - 2]) + 1))
            data.append(go.Scatter(x=xrange, y=bytes[i - 2], mode='lines', name=("Node" + str(i))))

        layout = dict(title='Time for slave-nodes to perform an action/merge in centralized configuration',
                      yaxis=dict(title='Time for action/merge(milliseconds)'),
                      xaxis=dict(title='Action/merge sequence number'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/slavemergelatency*")
        plot(figure, filename=(self.path + "/slavemergelatency%s.html" % str(len(files)+1)), auto_open=False)


    def write_master_mergelatency(self):
        data = []
        bytes = []
        file = open("testdata/mergelatency1", "r")
        line = file.read()
        bytes.append(json.loads(line))
        file.close()
        xrange = list(range(1, len(bytes[0]) + 1))
        data.append(go.Scatter(x=xrange, y=bytes[0], mode='lines', name="Node1"))

        layout = dict(title='Time for the master-node to perform an action/merge in centralized configuration',
                      yaxis=dict(title='Time for action/merge(milliseconds)'),
                      xaxis=dict(title='Action/merge sequence number'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mastermergelatency*")
        plot(figure, filename=(self.path + "/mastermergelatency%s.html" % str(len(files)+1)), auto_open=False)


    def write_slave_messagelatency(self):
        files = glob.glob("testdata/messagelatency*")
        data = []
        bytes = []
        for i in range(2, len(files) + 1):
            file = open("testdata/messagelatency" + str(i), "r")
            line = file.read()
            bytes.append(json.loads(line))
            file.close()
            xrange = list(range(1, len(bytes[i - 2][1]) + 1))
            data.append(go.Scatter(x=xrange, y=bytes[i - 2][1], mode='lines', name=("Node" + str(i))))

        layout = dict(title='Time for an entire message to be received by the receiver which are slave-nodes',
                      yaxis=dict(title='Time for message to be received (milliseconds)'),
                      xaxis=dict(title='Received message number'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/slavemessagelatency*")
        plot(figure, filename=(self.path + "/slavemessagelatency%s.html" % str(len(files)+1)), auto_open=False)


    def write_master_messagelatency(self):
        data = []
        bytes = []
        file = open("testdata/messagelatency1", "r")
        line = file.read()
        bytes.append(json.loads(line))
        file.close()
        xrange = list(range(1, len(bytes[0][1]) + 1))
        data.append(go.Scatter(x=xrange, y=bytes[0][1], mode='lines', name="Node1"))

        layout = dict(title='Time for an entire message to be received by the receiver which is the master-node',
                      yaxis=dict(title='Time for message to be received (milliseconds)'),
                      xaxis=dict(title='Received message number'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mastermessagelatency*")
        plot(figure, filename=(self.path + "/mastermessagelatency%s.html" % str(len(files)+1)), auto_open=False)


    def write_slave_messagesize(self):
        files = glob.glob("testdata/messagesize*")
        data = []
        bytes = []
        for i in range(2, len(files) + 1):
            file = open("testdata/messagesize" + str(i), "r")
            line = file.read()
            bytes.append(json.loads(line))
            file.close()
            xrange = list(range(1, len(bytes[i - 2]) + 1))
            data.append(go.Scatter(x=xrange, y=bytes[i - 2], mode='lines', name=("Node" + str(i))))

        layout = dict(title='Size of messages sent by slave-nodes',
                      yaxis=dict(title='Message size (bytes)'),
                      xaxis=dict(title='Number of sent messages'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/slavemessagesize*")
        plot(figure, filename=(self.path + "/slavemessagesize%s.html" % str(len(files)+1)), auto_open=False)


    def write_master_messagesize(self):
        data = []
        bytes = []
        file = open("testdata/messagesize1", "r")
        line = file.read()
        bytes.append(json.loads(line))
        file.close()
        xrange = list(range(1, len(bytes[0]) + 1))
        data.append(go.Scatter(x=xrange, y=bytes[0], mode='lines', name="Node1"))

        layout = dict(title='Size of messages sent by slave-nodes',
                      yaxis=dict(title='Message size (bytes)'),
                      xaxis=dict(title='Number of sent messages'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mastermessagesize*")
        plot(figure, filename=(self.path + "/mastermessagesize%s.html" % str(len(files)+1)), auto_open=False)


if __name__ == '__main__':
    #write_bytes()
    data = Draw()
    data.perform_writes(1)

