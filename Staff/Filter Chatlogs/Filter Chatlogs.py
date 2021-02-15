import re
searchIds = []
searchIds = input("IDs to look for - seperated by commas and only numbers      ---->").replace(' ','').split(',')
rawText = open('raw.txt','r', encoding='utf8').readlines()
open('output.txt','w', encoding='utf8').write("")

def userOrder():
    for i in range(len(searchIds)):
        if len(searchIds[i]) < 6:
            spacerAmount = '-'* (6 - len(searchIds[i]))
            searchIds[i] = f'{spacerAmount}{searchIds[i]}'
        regex = f'(ID {searchIds[i]}'+'{1})'
        for line in rawText:
            if re.search(regex, line):
                #print(line)
                open('output.txt','a', encoding='utf8').write(line)
def timeOrder():
    regex = []
    for i in range(len(searchIds)):
        if len(searchIds[i]) < 6:
            spacerAmount = '-'* (6 - len(searchIds[i]))
            searchIds[i] = f'{spacerAmount}{searchIds[i]}'
        regex.append(f'(ID {searchIds[i]}'+'{1})')
    for line in rawText:
        for i in range(len(regex)):
            if re.search(regex[i], line):
                #print(line)
                open('output.txt','a', encoding='utf8').write(line)
opType = input('Chronological order Order(1) **or** by individual users\' messages(2)')
if opType != '1' and opType != '2':
    print("Welp, that was wrong, try again")
elif opType == '1':
    print(timeOrder())
elif opType == '2':
    print(userOrder())
else:
    print("You must've done something wrong here, idk man")