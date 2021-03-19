import json
import requests as req
key = open('key.txt','r').read()
USER_ID = 59504
print(f"Running check on playerID {USER_ID}")

#List of server route starters
serversList = [
    'http://server.tycoon.community:30120/status', 'http://server.tycoon.community:30122/status',
    'http://server.tycoon.community:30123/status','http://server.tycoon.community:30124/status',
    'http://na.tycoon.community:30120/status','http://na.tycoon.community:30122/status','http://na.tycoon.community:30123/status',
    'http://na.tycoon.community:30124/status','http://na.tycoon.community:30125/status']


def onlineServer():
    server = ""
    for i in range(len(serversList)):
        data = req.get(f'{serversList[i]}/players.json')
        if data.status_code != 200:
            print(f'Request to {serversList[i]} for online players failed!')
            continue
        if str(USER_ID) in data.text:
            server = serversList[i]
            break
    return server

def saveFile(largeList):
    with open('test.json', 'w') as outfile:
        json.dump(largeList, outfile)


def localRunner(server):
    if server:
        playerLocData = req.get(f'{server}/map/positions2.json', headers={"X-Tycoon-Key":key}).json()['players']
    else:
        print(f"PlayerID {USER_ID} not found on any servers!")
        return
    for i in range(len(playerLocData)):
        if USER_ID != playerLocData[i][2]:
            continue
        else:
            allCords = playerLocData[i][6]
            currentCords = allCords[1]
            print(currentCords, "Is the current player cords")
            location = input("Enter the boost location -->  ").lower()
            if "y" in input(f"Is boost location of {location} at x={currentCords[1]} and y={currentCords[2]} correct? Y or N -->   ").lower():
                with open('test.json') as json_file:
                    largeList = json.load(json_file)
                try:
                    largeList[location]
                except KeyError:
                    largeList.update({location: [[currentCords[1],currentCords[2],currentCords[3]]]})
                    saveFile(largeList)
                    print("New location saved!")
                    return
                for saved_local in largeList[location]:
                    passes = 0
                    for player_cord in allCords:
                        xIncD = saved_local[0] + 10
                        xIncU = saved_local[0] - 10
                        yIncD = saved_local[1] + 10
                        yIncU = saved_local[1] - 10
                        if player_cord[1] <= xIncD and player_cord[1] >= xIncU and player_cord[2] <= yIncD and player_cord[2] >= yIncU:
                            print("Location already logged")
                            passes += 1
                            break

                if passes == 0:
                    print(largeList)
                    newList = [currentCords[1],currentCords[2],currentCords[3]]
                    largeList[location].append(newList)
                    print(newList, "added!")
                    break

            else:
                print("ya messed up")
        break

localRunner(onlineServer())
