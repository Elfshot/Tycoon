import threading
import requests as req
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re
key = open('key.txt','r').read()
#All members of IA
whitelistIA = ['7323','63573','323921','187701','15349','165288','122035','148383',
    '194505','125693','204132','344676','59504','120705','122372','68934','15148','71219',
    '325751','151866','316676','346325','150266','250036','360447','200750','165247','192643',
    '217725','318892','203580','174848','13762','438854','346931','336352','157396','199431',
    '354189','52806','461785','307590','402455']
#server names to ref
serverNames = [
    'OS - 1',
    'EU - 2',
    'EU - 3',
    'EU - 4',
    'EU - 6',
    'EU - 7',
    'EU - 8',
    'EU - 9',
    'EU - A'
]
#List of server route starters
serversList = [
    'http://server.tycoon.community:30120/status', 'http://server.tycoon.community:30122/status',
    'http://server.tycoon.community:30123/status','http://server.tycoon.community:30124/status',
    'http://na.tycoon.community:30120/status','http://na.tycoon.community:30122/status','http://na.tycoon.community:30123/status',
    'http://na.tycoon.community:30124/status','http://na.tycoon.community:30125/status']
#Get meals from meal sheet without s5 data
def mealsFromGoogle():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVER_ACCOUNT_FILE = "creds.json"
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVER_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #Data for the dump
    global dumpResults
    dumpResults = sheet.values().get(spreadsheetId='1-JJlDjbO828b8jyvPMg9-fJKIGVkYGmBaFUG9ZsXbTo', 
                                                    range="IA MEALS!C5:D14").execute()
    #get numbers
    numbersresult = sheet.values().get(spreadsheetId='1-JJlDjbO828b8jyvPMg9-fJKIGVkYGmBaFUG9ZsXbTo', 
                                                    range="IA MEALS!D5:D14").execute()
    dataValue = numbersresult.get('values', [])
    dataValue.pop(4)
    return dataValue
mealsFromGoogle = mealsFromGoogle()
#main function
def massScanning():
    #This will check to see if there are any people on the transformer
    def inMealLocation(server):
        try:
            playerLocData = req.get(f'{serversList[server]}/map/positions.json', headers={"X-Tycoon-Key":key}).json()['players']
        except:
            #If there is an error calling the api, print offline and return nothing to skip function
            print(f'!! ~\'{serversList[server]}\'~ is offline!!')
            return
        for iter in range(len(playerLocData)):
            if playerLocData[iter][4]:
                #print(playerLocData[iter])
                try:
                    playerLocal = [int(playerLocData[iter][3]['x']),int(playerLocData[iter][3]['y'])]
                except TypeError:
                    continue
                #Checks player's X and Y against +10 and -10 the X,Y of the transformer
                if  playerLocal[0] <= -1580 and playerLocal[0] >= -1600 and playerLocal[1] <= -3146 and playerLocal[1] >= -3166:
                    inTerminalID = str(playerLocData[iter][2])
                    print(f'ID - {playerLocData[iter][2]} is on the IA meal terminal in {serverNames[server]}')
                    #Checks if the player is in the preset IA list before adding them to the txt
                    if 'imperialtrailer' in str(playerLocData[iter][4]['owned_vehicles']):
                        print(f"Trailer found for {inTerminalID} in {serverNames[server]}")
                        return
                    elif inTerminalID in whitelistIA:
                        open("WhoInMeals.txt","a").write(f"\nID - {playerLocData[iter][2]} is on the IA meal terminal in {serverNames[server]}")
    #Goes over each of the nine servers to see if the server even has meals before the api calling function is envoked
    for iter in range(9): #9 servers
            #formatting >
            serverMeals = re.sub("\['", "", str(mealsFromGoogle[iter])) 
            serverMeals = int(re.sub("']", "", serverMeals))
            #formatting ^
            if serverMeals > 0:
                inMealLocation(iter)
    #Try and Except for getting API keys, if server down then print the thing
    try:
        print(req.get('http://na.tycoon.community:30125/status/charges.json', headers={"X-Tycoon-Key":key}).text)
    except:
        print("Keys Server Down!")
#Perma looping it
while True:
    massScanning()
    threading.Event().wait(300)
