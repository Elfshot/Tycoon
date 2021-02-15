import re
rawText = open('CleanIn.txt','r', encoding='utf8').readlines()
open('CleanOut.txt','w', encoding='utf8').write("")
for line in rawText:
    newLine = re.sub(r"`|\*","",line)
    print(newLine)
    open('CleanOut.txt','a', encoding='utf8').write(newLine)
