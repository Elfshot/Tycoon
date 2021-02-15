import discord
from discord.ext import commands
import logging
import requests as req
import re
from bs4  import BeautifulSoup, Comment
import json
import time
APIkey = 'KbOykLziDIJSFzIial5LcaYE4ukGeHE2BV58Y'
serversList = [
    'http://server.tycoon.community:30120/status', 'http://server.tycoon.community:30122/status',
    'http://server.tycoon.community:30123/status','http://server.tycoon.community:30124/status',
    'http://server.tycoon.community:30125/status','http://na.tycoon.community:30120/status',
    'http://na.tycoon.community:30122/status','http://na.tycoon.community:30123/status',
    'http://na.tycoon.community:30124/status','http://na.tycoon.community:30125/status']
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Client start
client = commands.Bot(command_prefix = 's!')
#ready message
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="s!help"))
    print("Bot is ready for bannings!")
#ping commad
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
@client.command()
async def wealthloop(ctx, *, arg):
    def getOnlineServer(userID):
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
    def getUserWealth(userID, server):
        usersWealth = []
        for userNum in range(len(userID)):
            try:
                htmlContent = req.get(f'{server[userNum]}/advanced/')
            except IndexError:
                usersWealth.append("User Offline")
                continue
            bs = BeautifulSoup(htmlContent.content,'html.parser')
            tr = bs.find_all('tr')
            for i in range(len(tr)):
                if userID[userNum] in tr[i].text:
                    temp = re.search(r'(\">\$(.*).{1}</td>)',str(tr[i].find_all('td')[4]))
                    usersWealth.append(temp.group().strip('"></td'))
                    break
        return usersWealth
    users = arg.replace(' ','').split(',')
    for i in range(100):
        wealth = f'{getUserWealth(users, getOnlineServer(users))} \n loop {i}/100'
        embed = discord.Embed(
                title = f'Wealth of uID {arg}',
                description =  f'**{wealth}**'
            ) 
        await ctx.send(embed=embed)
        time.sleep(3)

@client.command()
async def userinv(ctx, *, arg):
    users = arg.replace(' ','').split(',')
    for user in users:
        htmlContent = req.get(f'http://server.tycoon.community:30120/status/dataadv/{user}', headers={"X-Tycoon-Key":APIkey})
        if htmlContent.status_code != 200:
            await ctx.send(f"Error fetching skills for uID {user}: {htmlContent.text}")
            return
        dict = htmlContent.json()
        embed = discord.Embed(
                    title = f'Inventory of uID {users}'
                ) 
        for key in dict['data']['inventory'].keys():
            objName = re.sub(r"(<.*?>)","",dict['data']['inventory'][key]['name'])
            print(objName)
            embed.add_field(name = objName, value = dict['data']['inventory'][key]['amount'], inline= True)
        await ctx.send(embed=embed)

@client.command()
async def userskills(ctx, *, arg):
    users = arg.replace(' ','').split(',')
    for user in users:
        htmlContent = req.get(f'http://server.tycoon.community:30120/status/dataadv/{user}', headers={"X-Tycoon-Key":APIkey})
        if htmlContent.status_code != 200:
            await ctx.send(f"Error fetching skills for uID {user}: {htmlContent.text}")
            return
        dict = htmlContent.json()
        embed = discord.Embed(title = f'Skills of uID {user}') 
        for key in dict['data']['gaptitudes_v'].keys():
            for item in dict['data']['gaptitudes_v'][key].keys():
                value = round(int(dict['data']['gaptitudes_v'][key][item]),3)
                embed.add_field(name = item.capitalize(), value = value, inline= True)
        await ctx.send(embed=embed)

#if file is not present or does not have token it will break
client.run(open('token.txt','r').read())