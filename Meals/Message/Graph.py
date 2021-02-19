import pandas as pd
import plotly.express as px
import json 
oldDict = open('mealDataDump.txt','r').read()
oldDict = json.loads(oldDict)
serverNames = ['OS - 1','EU - 2','EU - 3','EU - 4','EU - 6','EU - 7','EU - 8','EU - 9','EU - A']

#print(type(oldDict),oldDict)
data = {}
for iMain in range(len(oldDict)):
    key = list(oldDict.keys())[iMain]
    
    dataTemp ={}
    for i in range(9):
        templist = oldDict[key].split(",")
        dataTemp.update({serverNames[i]: int(templist[i])}) 

    #print(dataTemp)
    data.update({key: dataTemp})


df = pd.DataFrame.from_dict(data=data, orient='index')
print(df)
fig = px.line(df)
fig.update_layout(title="Meals Remaining In A Given Server Over Time", 
yaxis_title = "Meals Remaining", xaxis_title = "Time & Date", legend_title="Server")
fig.show()
