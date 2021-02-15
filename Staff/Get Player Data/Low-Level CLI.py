import requests as req
import re
from bs4  import BeautifulSoup, Comment
import json
userID = []
userID = input("IDs to look for - seperated by commas and only numbers      ---->").replace(' ','').split(',')
serversList = [
    'http://server.tycoon.community:30120/status', 'http://server.tycoon.community:30122/status',
    'http://server.tycoon.community:30123/status','http://server.tycoon.community:30124/status',
    'http://server.tycoon.community:30125/status','http://na.tycoon.community:30120/status',
    'http://na.tycoon.community:30122/status','http://na.tycoon.community:30123/status',
    'http://na.tycoon.community:30124/status','http://na.tycoon.community:30125/status']
def getOnlineServer():
    onlineServers = []
    for userNum in range(len(userID)):
        for i in range(len(serversList)):
            data = req.get(f'{serversList[i]}/players.json')
            if data.status_code != 200:
                print(f'Request to {serversList[i]} for online players failed!')
                continue
            if userID[userNum] in data.text:
                onlineServers.append(serversList[i])
                break
    return onlineServers

def getUserWealth(server):
    usersWealth = []
    for userNum in range(len(userID)):
        htmlContent = req.get(f'{server[userNum]}/advanced/')
        bs = BeautifulSoup(htmlContent.content,'html.parser')
        tr = bs.find_all('tr')
        for i in range(len(tr)):
            if userID[userNum] in tr[i].text:
                temp = re.search(r'(\">\$(.*).{1}</td>)',str(tr[i].find_all('td')[4]))
                usersWealth.append(temp.group().strip('"></td'))
                break
    return usersWealth
#366391, 391984 
print(getUserWealth(getOnlineServer()))