import pyperclip
import time
import json
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
def characterCleaner(something):
        something = str(something)
        something = re.sub("\[", "", something)
        something = re.sub("]", "", something)
        something = re.sub("\'", "", something)
        return something
def main():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVER_ACCOUNT_FILE = "creds.json"
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVER_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #get numbers
    numbersresult = sheet.values().get(spreadsheetId='1-JJlDjbO828b8jyvPMg9-fJKIGVkYGmBaFUG9ZsXbTo', 
                                                    range="IA MEALS!D5:D14").execute()
    global dataValue
    dataValue = numbersresult.get('values', [])
    dataValue.pop(4)
    #get names
    dataName = [
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
    #get time                                                
    timeresults = sheet.values().get(spreadsheetId='1-JJlDjbO828b8jyvPMg9-fJKIGVkYGmBaFUG9ZsXbTo', 
                                                    range="IA MEALS!E5:E14").execute()
    timeValue = timeresults.get('values', [])
    #get date                                                
    dateresults = sheet.values().get(spreadsheetId='1-JJlDjbO828b8jyvPMg9-fJKIGVkYGmBaFUG9ZsXbTo', 
                                                    range="IA MEALS!F5:F14").execute()
    dateValue = dateresults.get('values', [])
    #Take the time and format it
    maxTime = characterCleaner(max(timeValue))
    maxDate = characterCleaner(max(dateValue))
    global timeAndDate
    timeAndDate = maxTime + ' ' + maxDate
        #Creates the meal table used in final formating
    def createTablesMeal(dataValue):
        mealTable = f"""\
    ```
                                            OS - 1 | {dataValue[0]} Meals
                                            EU - 2 | {dataValue[1]} Meals
                                            EU - 3 | {dataValue[2]} Meals
                                            EU - 4 | {dataValue[3]} Meals
                                            EU - 6 | {dataValue[4]} Meals
                                            EU - 7 | {dataValue[5]} Meals 
                                            EU - 8 | {dataValue[6]} Meals
                                            EU - 9 | {dataValue[7]} Meals
                                            EU - A | {dataValue[8]} Meals
    ```
            """
            #Formatting the table to exclude charactes
        return characterCleaner(mealTable)
# Function to determine what servers need to be filled
    def reallyBadServers():
        badservsint = []
        #Goes over each server and if meals are less than 1000, they will be added to "badservers" and returned at the end
        for iter in range(9):
            mealsinserver = characterCleaner(str(dataValue[iter]))
            if int(mealsinserver) < 1000:
                badservsint.append(iter)
        badservers = []
        for iter in badservsint:
            badservers.append(dataName[iter])
        if len(badservers) > 1:
            badservers[-1] = f"and {badservers[-1]}"
        badservers = str(badservers)
        characterCleaner(badservers)
        if badservers: 
            return f"Please make sure to fill servers ||{badservers}|| urgently!"
        else:
            return ""
        return badservers 
    def prettyGoodServers():
        badservsint = []
        #Goes over each server and if meals are over 2000 & under 10000, they will be added to "badservers" and returned at the end
        for iter in range(9):
            mealsinserver = characterCleaner(str(dataValue[iter]))
            if int(mealsinserver) >= 2000 and int(mealsinserver) < 10000:
                badservsint.append(iter)
        badservers = []
        for iter in badservsint:
            badservers.append(dataName[iter])
        if len(badservers) > 1:
            badservers[-1] = f"and {badservers[-1]}"
        badservers = str(badservers)
        characterCleaner(badservers)
        if badservers: 
            return f"\n    Fill servers ||{badservers}|| as you see fit."
        else:
            return ""
    def reallyOkServers():
        badservsint = []
        #Goes over each server and if meals are less than 2000 but over 1000, they will be added to "badservers" and returned at the end
        for iter in range(9):
            mealsinserver = characterCleaner(str(dataValue[iter]))
            if int(mealsinserver) >= 1000 and int(mealsinserver) < 2000:
                badservsint.append(iter)
        badservers = []
        for iter in badservsint:
            badservers.append(dataName[iter])
        if len(badservers) > 1:
            badservers[-1] = f"and {badservers[-1]}"
        badservers = str(badservers)
        characterCleaner(badservers)
        if badservers: 
            return f" Fill servers ||{badservers}|| afterwards."
        else:
            return ""
    def fullServersCount():
        badservsint = 0
        #Goes over each server and if meals are 1000, they will be added to "badservers" and returned at the end
        for iter in range(9):
            mealsinserver = characterCleaner(str(dataValue[iter]))
            if int(mealsinserver) == 10000:
                badservsint += 1
        if badservsint == 1:
            return 8
        else:
            return badservsint * 8
    #Function to compile the final message
    def compileMessage():
        #Call all functions and files needed to fill variables in the final message
        meals = createTablesMeal(dataValue)
        needFilling = reallyBadServers()
        wantFilling = reallyOkServers()
        notReallFill = prettyGoodServers()
        fullChars = fullServersCount()
        #All servs full
        if not needFilling and not wantFilling and not notReallFill:
            needFilling = "Fucking amazing job, all the servers are filled to the brim!"
        #all servs empty
        elif len(needFilling) == 111:
           needFilling = "Piss poor performance, literally all the servers need filling! Smh my head"
        #all servers 1k - 2k
        elif len(wantFilling) - fullChars <= 83: 
            wantFilling = reallyOkServers().replace("afterwards", "whenever possible")
        elif len(wantFilling) - fullChars > 83:
           wantFilling = "Fill all the servers as you see fit, they're doing *ok* but most could use a bit more."
        #all servs 2k - 9999
        elif len(notReallFill) == 112 - fullChars:
           notReallFill = "All the servers are filled up pretty good, fill up the lesser stocked ones if you're in the mood."
        # no servs under 1k but at least one over 1k
        elif len(needFilling) == 0 and len(wantFilling) >= 5:
            wantFilling = wantFilling.replace(" as soon as possible followed by ", "Please fill the following servers as you see fit - ")
        motd = str(open("Motd.txt", "r").read())
        notes = str(open("Additional Notes.txt", "r").read())
        nameUser = "Elfshot"
        rankCompany = "Freight Manager"
    #Make final message; all variables are now but into one big chunk
        return f"""
        @ imp air

                                                                                        ----Imperial Airlines----
    {motd}
                                                                                        ==Server / Meal List==
    {meals}\
                                                                                        --Notes--
    {needFilling}{wantFilling}{notReallFill}
    {notes}
                    {nameUser}
    :empire: {rankCompany} :empire:"""

    finalMessage = compileMessage()
    print(finalMessage, f"\n\n P.S \nAccurate as of {timeAndDate} CET(UTC +1)", 
    "\n\nYes this was copied to the clipboard.")
    #Copy to clipboard
    pyperclip.copy(finalMessage)
    dataValue = characterCleaner(dataValue)

#Save a data dump to file every run cycle (except if old in new)
def dataDump():
#    delare some stuff used in the loop
    oldDict = open("mealDataDump.txt", "r").read()
    newDict = json.loads(oldDict)
    try:
        newDict[f'{timeAndDate}']
        print("already cached ez")
    except KeyError:
        newDict.update({timeAndDate: f"{dataValue}"})
        open("mealDataDump.txt", "w").write(json.dumps(newDict))
        print("Cached")


#{"21:31:07 26/01/21": [8802, 1975, 1944,10000, 7000, 0, 0, 0, 3745], "4:24:37 30/01/21": [0, 0, 1944, 0, 7000, 0, 0, 0, 0], "6:54:50 31/01/21": [9700, 3700, 1944, 9800, 7000, 0, 5976, 0, 100], "21:53:23 01/02/21": [0, 0, 0, 9597, 7000, 0, 5976, 0, 100], "2:09:41 03/02/21":  [0, 0, 0, 9597, 7000, 0, 5976, 0, 53], "17:58:55 04/02/21": [0, 0, 0, 9597, 0, 0, 5976, 0, 53], "1:55:38 06/02/21":  [0, 0, 0, 9575, 0, 0, 5913, 0, 0], "23:41:02 06/02/21":  [4000, 0, 0, 9575, 0, 0, 5895, 0, 0], "23:22:49 07/02/21": [5998, 0, 0, 0, 0, 0, 5895, 0, 2133], "8:21:10 08/02/21": [7641, 1900, 1900, 0, 0, 0, 5895, 0, 3933]}






#Call the primary functions - dataDump is both seperate to isolate its variables and for easy disabling of that code.
main()
dataDump()
#Small timeout for them slow boys to catch a peek
time.sleep(2)