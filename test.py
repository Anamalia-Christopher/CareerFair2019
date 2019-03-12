#########---CHRISTOPHER ANAMALIA-------###########
#########---EMMANUEL ANTWI ------------###########

from os import getcwd, system
import csv
from random import randrange

cwd = getcwd()
with open(cwd + '/data/airports.csv', 'r') as data:


    airport = []
    for row in csv.reader(data):
        # 2-city 3- country 4- IATA code 6-latitude 7-longitude
        if not (row[4] == '\\N'):
            airport.append([row[2], row[3]])
l = len(airport)
for i in range(10):
    s = randrange(0, l)
    d = randrange(0, l)
    while s==d:
        d = randrange(0, l)


    a = airport[s][0]
    s_city = a.replace(' ', '')
    a = airport[d][0]
    d_city = a.replace(' ', '')
    if '/' in d_city or '/' in s_city:
        continue

    with open(cwd + '/tests/' + s_city + '-'+d_city + '.txt', 'w+') as sol:
        sol.write(airport[s][0] + ', '+airport[s][1] +'\n')
        sol.write(airport[d][0] + ', '+airport[d][1])

    t = 'tests/'+s_city + '-'+d_city + '.txt'
    # print(t)
    system('python run.py '+ t)