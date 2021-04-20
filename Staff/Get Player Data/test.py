import requests as req
import math
key = "KbOykLziDIJSFzIial5LcaYE4ukGeHE2BV58Y"
data = req.get('http://server.tycoon.community:30120/status/data/59504', headers={"X-Tycoon-Key":key})
dict = data.json()
skilsName = {
    'bus': 'Bus',
    'train': "Train Conman",
    'garbage': 'Garbage',
    'postop': 'Postop Employee',
    'mechanic': 'Mechanic',
    'trucking': 'Trucking',
    'casino': "Gambling",
    'business': "Bidniz",
    'mining': 'Miner',
    'farming': 'Farmer',
    'fishing': 'Fisherman',
    'strength': 'Stronk',
    'skill': 'Hunter',
    'cargos': 'Cargo Pilot',
    'heli': 'Heli Pilot',
    'piloting': 'Airline Pilot',
    'player': 'Player Skills',
    'racing': 'Racer',
    'fire': 'Fire Fighter',
    'ems': 'EMS'
}
list = [
    'train',
    'trucking',
    'casino',
    'business',
    'farming',
    'physical',
    'hunting', 
    'piloting',
    'player',  
    'ems'
]

def function(cate):
    print(f"\n----------{cate}-------------")
    for item in dict['data']['gaptitudes_v'][cate].keys():
        value = round(int(dict['data']['gaptitudes_v'][cate][item]),3)
        difference = 1000000 - value
        if value <= 1000000:
            differenceLevel = math.floor((math.sqrt(1 + 8 * difference / 5) - 1) / 2)
            print(f"{differenceLevel} to {skilsName[item]}")
        else:
            print(f"One mill in {skilsName[item]} achieved")




for item in list:
    function(item)









#input()