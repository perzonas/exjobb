import plotly.plotly as py
from plotly.offline import plot
import plotly.io as pio
import plotly.graph_objs as go
import glob
import os
import json


sum1 = 0
sum2 = 0
bytes = []

files = glob.glob("testdata/bytes*")
data = []
for i in range(1, len(files)+1):
    file = open("testdata/bytes"+str(i), "r")
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

layout = go.Layout(barmode='group', title='Number of bytes sent during test')
figure = go.Figure(data=data, layout=layout)
files = glob.glob(self.path+"/bytes*")
plot(figure, filename=(self.path+"/bytes%s.html" % str(len(files) + 1)), auto_open=False)
os.chmod(self.path+"/bytes%s.html" % str(len(files) + 1), 0o777)