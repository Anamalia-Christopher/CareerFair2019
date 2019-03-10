import csv
from os import  getcwd
from sys import argv
from datetime import datetime
from math import asin, radians, cos, sqrt, sin


class Main:

    def __init__(self):
        self.journey_to = []
        self.journey_from = []
        self.between= []
        self.inter = {}
        self.to_dict = {}
        self.to_dict = {}
        self.least_distance = [10000000000,0]
        self.cum_distance =0
        self.more = False

    def openFiles(self):
        cwd = getcwd()
        with open(cwd + '/data/airlines.csv', 'r') as data:
            self.airline = []
            for row in csv.reader(data):
                # 3 - IATA code 7- active
                if row[3] and row[7] == 'Y':
                    self.airline.append(row[3])

        with open(cwd + '/data/airports.csv', 'r') as data:
            self.airport = []
            self.IATA_airport = []
            for row in csv.reader(data):
                # 2-city 3- country 4- IATA code 6-latitude 7-longitude
                if not (row[4] == '\\N'):
                    self.airport.append([row[2],row[3], row[4], row[6],row[7]])
                    self.IATA_airport.append(row[4])

        with open(cwd + '/data/routes.csv', 'r') as data:
            self.routes = []
            for row in csv.reader(data):
                # 0 - airline code 2- source airport code 4 - destination airport code 7- stops
                if row[1] != '\\N':
                    self.routes.append([row[0],row[2], row[4], row[7]])


        with open(cwd +'/'+ argv[-1],  'r') as data:
            self.input = [ i.strip().split(', ') for i in data.readlines()]


        return

    def inputCodes(self):
        self.input_codes = {}
        half_length = int(len(self.airport)/2)
        for i in range(half_length):

            if self.input[0][1]==self.airport[i][1] and self.input[0][0]==self.airport[i][0]:
                self.input_codes['source']= self.airport[i][2]
                if len(self.input_codes) == 2:
                    break

            if self.input[1][1]==self.airport[i][1] and self.input[1][0]==self.airport[i][0]:
                self.input_codes['destination'] = self.airport[i][2]
                if len(self.input_codes) == 2:
                    break
            if self.input[0][1]==self.airport[half_length+i][1] and self.input[0][0]==self.airport[half_length+i][0]:
                self.input_codes['source']= self.airport[half_length+i][2]
                if len(self.input_codes) == 2:
                    break

            if self.input[1][1]==self.airport[half_length+i][1] and self.input[1][0]==self.airport[half_length+i][0]:
                self.input_codes['destination'] = self.airport[half_length+i][2]
                if len(self.input_codes) == 2:
                    break

        print(self.input_codes)


    # todo: do for direct flight
    def directFlight(self, source, destination):
        quarter_length = int(len(self.routes)/4)
        self.direct_l = []

        cor1 = self.coor(source)
        cor2 = self.coor(destination)


        distance = self.Harversine_f(lat1=cor1[0], lon1=cor1[1], lat2=cor2[0], lon2=cor2[1])

        for i in range(quarter_length):

            if self.routes[i][1] == source and self.routes[i][2] == destination and (self.routes[i][0] in self.airline):
                self.routes[i].append(distance)
                self.direct_l = self.routes[i]
                return

            if self.routes[quarter_length + i][1] == source and self.routes[quarter_length + i][2] == destination and (self.routes[quarter_length + i][0] in self.airline):

                self.routes[quarter_length+i].append(distance)
                self.direct_l = self.routes[quarter_length + i]
                return

            if self.routes[2 * quarter_length + i][1] == source and self.routes[2 * quarter_length + i][2] == destination and (
                    self.routes[2 * quarter_length + i][0] in self.airline):

                self.routes[2*quarter_length+i].append(distance)
                self.direct_l = self.routes[2 * quarter_length + i]
                return

            if self.routes[3 * quarter_length + i][1] == source and self.routes[3 * quarter_length + i][2] == destination and (
                    self.routes[3 * quarter_length + i][0] in self.airline):

                self.routes[3*quarter_length+i].append(distance)
                self.direct_l = self.routes[3 * quarter_length + i]
                return


        return

    def dRFlight(self, source_set, destination_set):
        quarter_length = round(len(self.routes)/4)
        l_s = len(source_set)
        l_d = len(destination_set)
        check =[]
        for i in range(quarter_length):
            if l_s>= l_d:
                for source in source_set:

                    if self.routes[i][1] == source and self.routes[i][2] in destination_set and (self.routes[i][0] in self.airline) and [self.routes[i][1],self.routes[i][2]] not in  check:

                        cor1 = self.coor(source)
                        cor2 = self.coor(self.routes[i][2])

                        self.routes[i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[i])
                        check.append([self.routes[i][1],self.routes[i][2]])
                        break

                    if self.routes[quarter_length + i][1] == source and self.routes[quarter_length + i][2] in destination_set and (self.routes[quarter_length + i][0] in self.airline) and [self.routes[quarter_length + i][1],self.routes[quarter_length + i][2]] not in check:


                        cor1 = self.coor(source)
                        cor2 = self.coor(self.routes[quarter_length+i][2])

                        self.routes[quarter_length+i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[quarter_length + i])

                        check.append([self.routes[quarter_length + i][1],self.routes[quarter_length + i][2]])
                        break

                    if self.routes[2 * quarter_length + i][1] == source and self.routes[2 * quarter_length + i][2] in destination_set and (self.routes[2 * quarter_length + i][0] in self.airline) and [self.routes[2 * quarter_length + i][1],self.routes[2 * quarter_length + i][2]] not in check:

                        cor1 = self.coor(source)
                        cor2 = self.coor(self.routes[2*quarter_length+i][2])

                        self.routes[2*quarter_length+i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[2 * quarter_length + i])
                        check.append([self.routes[2 * quarter_length + i][1],self.routes[2 * quarter_length + i][2]])
                        break

                    if self.routes[3 * quarter_length + i][1] == source and self.routes[3 * quarter_length + i][2] in destination_set and (
                            self.routes[3 * quarter_length + i][0] in self.airline) and [self.routes[3 * quarter_length + i][1], self.routes[3 * quarter_length + i][2]] not in check:

                        cor1 = self.coor(source)
                        cor2 = self.coor(self.routes[3*quarter_length+i][2])

                        self.routes[3*quarter_length+i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[3 * quarter_length + i])

                        check.append([self.routes[3 * quarter_length + i][1], self.routes[3 * quarter_length + i][2]])

                        break

            else:
                for destination in destination_set:

                    if self.routes[i][2] == destination and self.routes[i][1] in source_set and (
                            self.routes[i][0] in self.airline) and [self.routes[i][1],self.routes[i][2]] not in  check:

                        cor1 = self.coor(self.routes[i][1])
                        cor2 = self.coor(destination)

                        self.routes[i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[i])

                        check.append([self.routes[i][1], self.routes[i][2]])

                        break
                    if self.routes[quarter_length + i][2] == destination and self.routes[quarter_length + i][1] in source_set and (self.routes[quarter_length + i][0] in self.airline) and [self.routes[quarter_length + i][1],self.routes[quarter_length + i][2]] not in check:

                        cor1 = self.coor(self.routes[quarter_length + i][1])
                        cor2 = self.coor(destination)

                        self.routes[quarter_length+i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[quarter_length + i])
                        check.append([self.routes[quarter_length + i][1],self.routes[quarter_length + i][2]])

                        break

                    if self.routes[2 * quarter_length + i][2] == destination and self.routes[2 * quarter_length + i][1] in source_set and (
                            self.routes[2 * quarter_length + i][0] in self.airline) and [self.routes[2 * quarter_length + i][1],self.routes[2 * quarter_length + i][2]] not in check:

                        cor1 = self.coor(self.routes[2*quarter_length + i][1])
                        cor2 = self.coor(destination)

                        self.routes[2*quarter_length+i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[2 * quarter_length + i])
                        check.append([self.routes[2 * quarter_length + i][1],self.routes[2 * quarter_length + i][2]])

                        break

                    if self.routes[3 * quarter_length + i][2] == destination and self.routes[3 * quarter_length + i][1] in source_set and (
                            self.routes[3 * quarter_length + i][0] in self.airline)  and [self.routes[3 * quarter_length + i][1], self.routes[3 * quarter_length + i][2]] not in check:
                        cor1 = self.coor(self.routes[3 * quarter_length + i][1])
                        cor2 = self.coor(destination)

                        self.routes[3*quarter_length+i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[3 * quarter_length + i])
                        check.append([self.routes[3 * quarter_length + i][1], self.routes[3 * quarter_length + i][2]])

                        break


        return


    def routing(self, source, destination):

        self.journey_to.append(source)
        self.journey_from.insert(0, destination)
        self.to_dict.setdefault(source, {})
        self.to_dict.setdefault(destination, {})
        s_to = set()
        d_from = set()
        quarter_length = int(len(self.routes)/4)
        cor1 = self.coor(source)
        cor3 = self.coor(destination)

        for i in range(quarter_length):

            if self.routes[i][1] == source and (self.routes[i][0] in self.airline):
                s_to.add(self.routes[i][2])

                cor2 = self.coor(self.routes[i][2])

                self.routes[i].append(self.Harversine_f(lat1=cor1[0], lon1=cor1[1], lat2=cor2[0], lon2=cor2[1]))


                self.to_dict[source][self.routes[i][2]]= self.routes[i]

            if self.routes[quarter_length+i][1] == source and (self.routes[quarter_length+i][0] in self.airline):
                s_to.add(self.routes[quarter_length+i][2])

                cor2 = self.coor(self.routes[quarter_length+i][2])


                self.routes[quarter_length+i].append(self.Harversine_f(lat1=cor1[0], lon1=cor1[1], lat2=cor2[0], lon2=cor2[1]))

                self.to_dict[source][self.routes[quarter_length+i][2]] = self.routes[quarter_length+i]

            if self.routes[2*quarter_length+i][1] == source and (self.routes[2*quarter_length+i][0] in self.airline):
                s_to.add(self.routes[2*quarter_length+i][2])

                cor2 = self.coor(self.routes[2*quarter_length + i][2])

                self.routes[2*quarter_length + i].append(self.Harversine_f(lat1=cor1[0], lon1=cor1[1], lat2=cor2[0], lon2=cor2[1]))

                self.to_dict[source][self.routes[2*quarter_length+i][2]] = self.routes[2*quarter_length+i]

            if self.routes[3*quarter_length+i][1] == source and (self.routes[3*quarter_length+i][0] in self.airline):
                s_to.add(self.routes[3*quarter_length+i][2])

                cor2 = self.coor(self.routes[3*quarter_length + i][2])

                self.routes[3*quarter_length + i].append(self.Harversine_f(lat1=cor1[0], lon1=cor1[1], lat2=cor2[0], lon2=cor2[1]))

                self.to_dict[source][self.routes[3*quarter_length+i][2]] = self.routes[3*quarter_length+i]



            if self.routes[i][2] == destination and (self.routes[i][0] in self.airline):
                d_from.add(self.routes[i][1])

                cor2 = self.coor(self.routes[i][1])

                self.routes[i].append(self.Harversine_f(lat1=cor3[0], lon1=cor3[1], lat2=cor2[0], lon2=cor2[1]))

                self.to_dict[destination][self.routes[i][1]] = self.routes[i]


            if self.routes[quarter_length+i][2] == destination and (self.routes[quarter_length+i][0] in self.airline):
                d_from.add(self.routes[quarter_length+i][1])

                cor2 = self.coor(self.routes[quarter_length+i][1])

                self.routes[quarter_length+i].append(self.Harversine_f(lat1=cor3[0], lon1=cor3[1], lat2=cor2[0], lon2=cor2[1]))


                self.to_dict[destination][self.routes[quarter_length+i][1]] = self.routes[quarter_length+i]


            if self.routes[2*quarter_length+i][2] == destination and (self.routes[2*quarter_length+i][0] in self.airline):
                d_from.add(self.routes[2*quarter_length+i][1])

                cor2 = self.coor(self.routes[2*quarter_length+i][1])

                self.routes[2* quarter_length+i].append(self.Harversine_f(lat1=cor3[0], lon1=cor3[1], lat2=cor2[0], lon2=cor2[1]))


                self.to_dict[destination][self.routes[2*quarter_length+i][1]] = self.routes[2*quarter_length+i]


            if self.routes[3*quarter_length+i][2] == destination and (self.routes[3*quarter_length+i][0] in self.airline):
                d_from.add(self.routes[3*quarter_length+i][1])

                cor2 = self.coor(self.routes[3*quarter_length+i][1])


                self.routes[3 * quarter_length+i].append(self.Harversine_f(lat1=cor3[0], lon1=cor3[1], lat2=cor2[0], lon2=cor2[1]))


                self.to_dict[destination][self.routes[3*quarter_length+i][1]] = self.routes[3*quarter_length+i]



        inter = s_to.intersection(d_from)
        if inter:
            self.inter = inter
            return

        self.dRFlight(source_set=s_to, destination_set=d_from)

        del inter
        if self.between:
            return

        else:
            self.more = True
            self.s_to = s_to
            self.d_from = d_from
            self.More()
            return

    def More(self):
        if len(self.s_to)>= len(self.d_from):
            for i in self.s_to:
                for j in self.d_from:
                    if len(self.journey_to)>1 and len(self.journey_from)>1:
                        self.journey_to.pop()
                        self.journey_from.pop(0)
                    self.routing(source=i, destination=j)

        else:
            for i in self.d_from:
                for j in self.s_to:
                    if len(self.journey_to)>1 and len(self.journey_from)>1:
                        self.journey_to.pop()
                        self.journey_from.pop(0)
                    self.routing(source=j, destination=i)

        return

    def Optimizer(self):

        if self.more :

            if len(self.inter) > 1:
                for i in self.inter:
                    before = self.to_dict[self.journey_to[-1]][i][1]
                    after = self.to_dict[self.journey_from[0]][i][2]
                    self.cum_distance = self.to_dict[self.journey_to[0]][before][4]+self.to_dict[self.journey_to[-1]][i][4] + \
                                        self.to_dict[self.journey_from[0]][i][4] +self.to_dict[self.journey_to[-1]][after][4]

                    self.comparator(i)

            elif len(self.between) > 1:
                for i in self.between:
                    before = self.to_dict[self.journey_to[-1]][i[1]][1]
                    after = self.to_dict[self.journey_from[0]][i[2]][2]
                    self.cum_distance = self.to_dict[self.journey_to[0]][before][4]+ self.to_dict[self.journey_to[-1]][i[1]][4] + i[4] + \
                                        self.to_dict[self.journey_from[0]][i[2]][4] + self.to_dict[self.journey_from[0]][after][4]

                    self.comparator(i)
            return

        elif len(self.inter)>1:

            for i in self.inter:

                self.cum_distance = self.to_dict[self.journey_to[0]][i][4] +self.to_dict[self.journey_from[-1]][i][4]

                self.comparator(i)

        elif len(self.between)>1:
            for i in self.between:

                self.cum_distance = self.to_dict[self.journey_to[0]][i[1]][4] + i[4] + self.to_dict[self.journey_from[-1]][i[2]][4]
                self.comparator(i)

        return



    def Writing(self):
        with open(getcwd() + '/' + argv[-1][:-4:] + '_output.txt', 'w+') as sol:
            if self.direct_l:

                self.WriteLine(file=sol, info=self.direct_l)
                sol.write('Total flights: 1\n')
                sol.write('Total additional stops: ' + str(self.direct_l[3]) + '\n')
                sol.write('Total distance: ' + str(self.direct_l[4]) + 'km\n')
                sol.write('Optimality criteria: flights')
                return

            if self.more:

                if self.inter:

                    if len(self.inter)==1:


                        i = list(self.inter)[0]
                        before = self.to_dict[self.journey_to[-1]][i][1]
                        after = self.to_dict[self.journey_from[0]][i][2]

                        self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][before])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_to[-1]][i])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_from[0]][i])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_to[-1]][after])

                        stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                                            int(self.to_dict[self.journey_to[-1]][i][3]) + \
                                            int(self.to_dict[self.journey_from[0]][i][3]) + \
                                            int(self.to_dict[self.journey_to[-1]][after][3])

                        self.cum_distance = self.cum_distance = self.to_dict[self.journey_to[0]][before][4] + \
                                            self.to_dict[self.journey_to[-1]][i][4] + \
                                            self.to_dict[self.journey_from[0]][i][4] + \
                                            self.to_dict[self.journey_to[-1]][after][4]


                        sol.write('Total flights: 4\n')
                        sol.write('Total additional stops: ' + str(stops) + '\n')
                        sol.write('Total distance: ' + str(self.cum_distance) + 'km\n')
                        sol.write('Optimality criteria: flights')

                        return

                    i = self.least_distance[1]
                    before = self.to_dict[self.journey_to[-1]][i][1]
                    after = self.to_dict[self.journey_from[0]][i][2]

                    self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][before])
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_to[-1]][i])
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_from[0]][i])
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_to[-1]][after])

                    stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                            int(self.to_dict[self.journey_to[-1]][i][3]) + \
                            int(self.to_dict[self.journey_from[0]][i][3]) + \
                            int(self.to_dict[self.journey_to[-1]][after][3])

                    sol.write('Total flights: 4\n')
                    sol.write('Total additional stops: ' + str(stops) + '\n')
                    sol.write('Total distance: ' + str(self.least_distance[0]) + 'km\n')
                    sol.write('Optimality criteria: distance')

                    return

                elif self.between:

                    if len(self.between) == 1:
                        i = self.between[0]

                        before = self.to_dict[self.journey_to[-1]][i[1]][1]
                        after = self.to_dict[self.journey_from[0]][i[2]][2]


                        self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][before])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_to[-1]][i[1]])

                        self.WriteLine(file=sol, info=i)

                        self.WriteLine(file=sol, info=self.to_dict[self.journey_from[0]][i[2]])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_from[0]][after])

                        stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                                            int(self.to_dict[self.journey_to[-1]][i[1]][3]) + int(i[3]) + \
                                            int(self.to_dict[self.journey_from[0]][i[2]][3]) + \
                                            int(self.to_dict[self.journey_from[0]][after][3])

                        self.cum_distance = self.to_dict[self.journey_to[0]][before][4] + \
                                            self.to_dict[self.journey_to[-1]][i[1]][4] + i[4] + \
                                            self.to_dict[self.journey_from[0]][i[2]][4] + \
                                            self.to_dict[self.journey_from[0]][after][4]

                        sol.write('Total flights: 5\n')
                        sol.write('Total additional stops: ' + str(stops) + '\n')
                        sol.write('Total distance: ' + str(self.cum_distance) + 'km\n')
                        sol.write('Optimality criteria: flights')

                        return

                    i = self.least_distance[1]

                    before = self.to_dict[self.journey_to[-1]][i[1]][1]
                    after = self.to_dict[self.journey_from[0]][i[2]][2]

                    self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][before])
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_to[-1]][i[1]])

                    self.WriteLine(file=sol, info=i)

                    self.WriteLine(file=sol, info=self.to_dict[self.journey_from[0]][i[2]])
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_from[0]][after])

                    stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                            int(self.to_dict[self.journey_to[-1]][i[1]][3]) + int(i[3]) + \
                            int(self.to_dict[self.journey_from[0]][i[2]][3]) + \
                            int(self.to_dict[self.journey_from[0]][after][3])


                    sol.write('Total flights: 5\n')
                    sol.write('Total additional stops: ' + str(stops) + '\n')
                    sol.write('Total distance: ' + str(self.least_distance[0]) + 'km\n')
                    sol.write('Optimality criteria: flights')

                    return


            elif self.inter:

                if len(self.inter) == 1:
                    i = list(self.inter)[0]
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][i])

                    self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][i])
                    stops = int(self.to_dict[self.journey_to[0]][i][3]) + int(self.to_dict[self.journey_from[-1]][i][3])

                    self.cum_distance = self.to_dict[self.journey_to[0]][i][4]+self.to_dict[self.journey_from[-1]][i][4]


                    sol.write('Total flights: 2\n')
                    sol.write('Total additional stops: ' + str(stops) + '\n')
                    sol.write('Total distance: ' + str(self.cum_distance) + 'km\n')
                    sol.write('Optimality criteria: flights')

                    return

                i=self.least_distance[1]
                self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][i])

                self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][i])
                stops = int(self.to_dict[self.journey_to[0]][i][3]) + int(self.to_dict[self.journey_from[-1]][i][3])

                sol.write('Total flights: 2\n')
                sol.write('Total additional stops: ' + str(stops) + '\n\n')
                sol.write('Total distance: ' + str(self.least_distance[0]) + 'km\n')
                sol.write('Optimality criteria: distance')

                return


            elif self.between:

                if len(self.between)==1:
                    i=self.between[0]
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][i[1]])

                    self.WriteLine(file=sol, info=i)

                    self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][i[2]])
                    stops =int(self.to_dict[self.journey_to[0]][i[1]][3])+ int(i[3]) +int(self.to_dict[self.journey_from[-1]][i[2]][3])

                    self.cum_distance =self.to_dict[self.journey_to[0]][i[1]][4]+ i[4] + self.to_dict[self.journey_from[-1]][i[2]][4]


                    sol.write('Total flights: 3\n')
                    sol.write('Total additional stops: ' + str(stops) + '\n')
                    sol.write('Total distance: ' + str(self.cum_distance) + 'km\n')
                    sol.write('Optimality criteria: flights')

                    return

                i = self.least_distance[1]

                self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][i[1]])

                self.WriteLine(file=sol, info=i)

                self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][i[2]])

                stops = int(self.to_dict[self.journey_to[0]][i[1]][3])+ int(i[3]) +int(self.to_dict[self.journey_from[-1]][i[2]][3])


                sol.write('Total flights: 3\n')
                sol.write('Total additional stops: ' + str(stops) + '\n\n')
                sol.write('Total distance: ' + str(self.least_distance[0]) + 'km\n')
                sol.write('Optimality criteria: distance')
                return

            else:
                sol.write("Unsupported request")


    def WriteLine(self, file, info):
        return file.write(info[0] + ' from ' + info[1] + ' to ' + info[2] + ' ' + info[3] + ' stops\n')

    def Final(self):
        self.openFiles()
        self.inputCodes()
        self.directFlight(source=self.input_codes['source'], destination=self.input_codes['destination'])

        if self.direct_l:
            self.Writing()
            return

        self.routing(source=self.input_codes['source'], destination=self.input_codes['destination'])
        self.Optimizer()
        self.Writing()
        return

    def coor(self, IATA):
        return float(self.airport[self.IATA_airport.index(IATA)][3]), float(self.airport[self.IATA_airport.index(IATA)][4])


    def Harversine_f(self, lat1, lon1,lat2, lon2):
        lon1, lat1, lon2, lat2 = radians(lon1), radians(lat1), radians(lon2), radians(lat2)
        d = int(2* 6371 * asin(sqrt(sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2)))

        return d

    def comparator(self, keyword):

        if self.cum_distance<self.least_distance[0]:
            self.least_distance[0] = self.cum_distance
            self.least_distance[1] = keyword

        return

    def BinarySearch(self, data, search):
        data = sorted(data)
        start = 0
        end = len(data) - 1
        while start <= end:
            middle = (start + end) // 2
            midpoint = data[middle]
            if midpoint > search:
                end = middle - 1
            elif midpoint < search:
                start = middle + 1
            else:
                return midpoint


start = datetime.now()
a = Main()


a.Final()
end = datetime.now()

print(((start-end).microseconds)/1000000)

