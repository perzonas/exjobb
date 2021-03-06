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
    max_avg = []
    min_avg = []
    xrange = []



    def perform_writes(self, type):
        self.path = os.path.dirname(os.path.abspath(__file__))
        folders = os.listdir(self.path)
        folders = filter(lambda x: ".py" not in x, folders)
        for folder in folders:
            print(folder)
        ### Create the right graphs for the solutions that has been used ###
        for folder in folders:
            print(folder)
            print("### CREATING GRAPHS FROM RESULTS ###")
            self.clear()
            self.write_bytes(folder)
            self.clear()
            self.write_messagesize(folder)
            self.clear()
            self.write_messagelatency(folder)
            self.clear()
            self.write_mergelatency(folder)
            self.clear()
            if type == self.CENTRALIZED:
                self.write_master_mergelatency()
                self.write_slave_messagelatency()
                self.write_master_messagesize()
                self.write_master_messagelatency()
                self.write_slave_mergelatency()
                self.write_slave_messagesize()
            print("### FINISHED MAKING GRAPHS ###")
            print("### TEST FINISHED -> CLOSING DOWN ###")


    def write_bytes(self, folder):
        sum1 = 0
        sum2 = 0
        bytes = []
        print(folder+"111")
        files = glob.glob(folder+"/rawdata/bytes*")
        data = []
        for i in range(1, len(files)+1):
            file = open(folder+"/rawdata/bytes"+str(i), "r")
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

        layout = go.Layout(barmode='group', font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                           yaxis=dict(type='log'))
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(folder+"/bytes*")
        plot(figure, filename=(folder+"/bytes%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(folder+"/bytes%s.html" % str(len(files) + 1), 0o777)


    def write_messagesize(self, folder):
        files = glob.glob(folder+"/rawdata/messagesize*")
        data = []
        bytes = []
        for i in range(1, len(files)+1):
            file = open(folder+"/rawdata/messagesize"+str(i), "r")
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

        self.xrange = list(range(1, max_length + 1))
        total = 0
        sent_messages = 0
        for i in range(max_length):
            min = 999999999999999999
            max = 0
            
            for j in range(len(bytes)):
                try:
                    if bytes[j][i] < min:
                        min = bytes[j][i]
                    if bytes[j][i] > max:
                        max = bytes[j][i]
                    total += bytes[j][i]
                    sent_messages += 1
                except:
                    pass
            self.messagesize_average.append(total/sent_messages)
            self.messagesize_max.append(max)
            self.messagesize_min.append(min)
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_average, name="Avg", mode='lines', line=dict(color='blue', width=6)))
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_max, name="Max", mode='lines', line=dict(color='black', width=4, dash='dot')))
        data.append(go.Scatter(x=self.xrange, y=self.messagesize_min, name="Min", mode='lines', line=dict(color='firebrick', width=4, dash='dash')))


        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      xaxis=dict(title='Sequence number of message'),
                      yaxis=dict(title='Message Size (bytes)', type='log'))
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(folder+ "/messagesize*")
        plot(figure, filename=(folder+"/messagesize%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(folder+"/messagesize%s.html" % str(len(files) + 1), 0o777)


    def write_messagelatency(self, folder):
        files = glob.glob(folder+"/rawdata/messagelatency*")
        data = []
        bytes = []
        for i in range(1, len(files) + 1):
            file = open(folder+"/rawdata/messagelatency" + str(i), "r")
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
        self.xrange = list(range(1, max_length + 1))
        total = 0
        messages_sent = 0
        max_total = 0
        min_total = 0
        for i in range(max_length):

            max = 0
            min = 999999999999999
            for j in range(len(bytes)):
                try:
                    if bytes[j][i] < min:
                        min = bytes[j][i]
                    if bytes[j][i] > max:
                        max = bytes[j][i]
                    total += bytes[j][i]
                    messages_sent += 1
                except:
                    pass
            max_total += max
            min_total += min
            self.max_avg.append(max_total / (i + 1))
            self.min_avg.append(min_total / (i + 1))
            self.messagelatency_average.append(total / messages_sent)
            self.messagelatency_max.append(max)
            self.messagelatency_min.append(min)
        data.append(go.Scatter(x=self.xrange, y=self.max_avg, name="Max_Avg", mode='lines', line=dict(color='black', width=5, dash='dot')))
        data.append(go.Scatter(x=self.xrange, y=self.min_avg, name="Min_Avg", mode='lines', line=dict(color='firebrick', width=5, dash='dash')))
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_average, name="Avg", mode='lines', line=dict(color='blue', width=4)))
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_max, name="Max", opacity=0.3, mode='lines', line=dict(color='black', width=3, dash='dot')))
        data.append(go.Scatter(x=self.xrange, y=self.messagelatency_min, name="Min", opacity=0.4, mode='lines', line=dict(color='firebrick', width=3, dash='dash')))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time to receive message in ms', type='log'),
                      xaxis=dict(title='Sequence number of message'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(folder+ "/messagelatency*")
        plot(figure, filename=(folder+ "/messagelatency%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(folder+ "/messagelatency%s.html" % str(len(files) + 1), 0o777)


    def write_mergelatency(self, folder):
        files = glob.glob(folder+"/rawdata/mergelatency*")
        data = []
        bytes = []
        for i in range(1, len(files) + 1):
            file = open(folder+"/rawdata/mergelatency" + str(i), "r")
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

        self.xrange = list(range(1, max_length+1))
        total = 0
        messages_sent = 0
        max_total = 0
        min_total = 0
        for i in range(max_length):
            min = 999999999999999
            max = 0
            for j in range(len(bytes)):
                try:
                    if bytes[j][i] < min:
                        min = bytes[j][i]
                    if bytes[j][i] > max:
                        max = bytes[j][i]
                    total += bytes[j][i]
                    messages_sent += 1
                except:
                    pass
            max_total += max
            min_total += min
            self.max_avg.append(max_total / (i + 1))
            self.min_avg.append(min_total / (i + 1))
            self.mergelatency_average.append(total / messages_sent)
            self.mergelatency_max.append(max)
            self.mergelatency_min.append(min)
        data.append(go.Scatter(x=self.xrange, y=self.max_avg, name="Max_Avg", mode='lines',
                               line=dict(color='black', width=5, dash='dot')))
        data.append(go.Scatter(x=self.xrange, y=self.min_avg, name="Min_Avg", mode='lines',
                               line=dict(color='firebrick', width=5, dash='dash')))
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_average, name="Avg", mode='lines', line=dict(color='blue', width=6)))
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_max, name="Max", opacity=0.3, mode='lines', line=dict(color='black', width=4, dash='dot')))
        data.append(go.Scatter(x=self.xrange, y=self.mergelatency_min, name="Min", opacity=0.4, mode='lines', line=dict(color='firebrick', width=4, dash='dash')))

        layout = dict(font=dict(family='Courier New, monospace', size=22, color='#2f2f2f'),
                      yaxis=dict(title='Time to perform operation in ms', type='log'),
                      xaxis=dict(title='Sequence number of performed operation'),
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(folder+ "/mergelatency*")
        plot(figure, filename=(folder+"/mergelatency%s.html" % str(len(files) + 1)), auto_open=False)
        os.chmod(folder+ "/mergelatency%s.html" % str(len(files) + 1), 0o777)


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
                      yaxis=dict(title='Time to perform operation in ms', type='log'),
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
                      yaxis=dict(title='Time to perform operation in ms', type='log'),
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
                      yaxis=dict(title='Time to receive message in ms', type='log'),
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
                      yaxis=dict(title='Time to receive message in ms', type='log'),
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
                      yaxis=dict(title='Size of message in bytes'),
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
                      yaxis=dict(title='Size of message in bytes'),
                      xaxis=dict(title='Sequence number of sent message')
                      )
        figure = go.Figure(data=data, layout=layout)
        files = glob.glob(self.path + "/mastermessagesize*")
        plot(figure, filename=(self.path + "/mastermessagesize%s.html" % str(len(files)+1)), auto_open=False)
        os.chmod(self.path + "/mastermessagesize%s.html" % str(len(files) + 1), 0o777)

    def clear(self):
        self.min_avg = []
        self.max_avg = []
        self.bytes_average = []
        self.messagesize_average = []
        self.messagesize_min = []
        self.messagesize_max = []
        self.messagelatency_average = []
        self.messagelatency_min = []
        self.messagelatency_max = []
        self.mergelatency_average = []
        self.mergelatency_min = []
        self.mergelatency_max = []
        self.xrange = []


if __name__ == '__main__':
    #write_bytes()
    data = Draw()
    data.perform_writes(3)

