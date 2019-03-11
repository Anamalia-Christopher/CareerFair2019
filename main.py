import csv
from os import  getcwd
from sys import argv
from datetime import datetime
from math import asin, radians, cos, sqrt, sin, ceil

# the logic used in this program is that airplanes leaving a source and airplanes arriving
# have something in common from intermediate flights if applicable
class Main:

    # initalizing the class variables
    # journey_to - keeps places left towards the destination from source
    # journey_from - keeps places left towards the source from destination
    # between - keep journey between source and destination
    # inter - keeps similar places in common between source and destination journeys
    # to_dict - all journeys leaving the source and destination
    # least_distance - [0]=least distance between source and destination(initialised with a really big value
    #                  [1] = information used to get what journey have the least distance
    # cum_distance - cumulative distance for different paths
    # more - Becomes true if more that 3 flights takes one to a destination
    def __init__(self):
        self.journey_to = []
        self.journey_from = []
        self.between= []
        self.inter = {}
        self.to_dict = {}
        self.least_distance = [10000000000,0]
        self.cum_distance =0
        self.more = False

    # Reads the necessary files and stores them in local variables
    def openFiles(self):

        # current working dir
        cwd = getcwd()

        # Reads airline data.
        # Excludes airlines with no airline ID since they are not used in routes
        # Excludes airlines that are not active
        with open(cwd + '/data/airlines.csv', 'r') as data:
            self.airline = []
            for row in csv.reader(data):
                # 3 - IATA code 7- active
                if row[3] and row[7] == 'Y':
                    self.airline.append(row[3])

        # Reads routes data and excludes all flights whose airlines do not exist,
        # whose airlines are defective, and with no Airline ID

        with open(cwd + '/data/routes.csv', 'r') as data:
            self.routes = []
            self.s_d = []
            source = set()
            destination = set()
            l = set(self.airline[:])

            for row in csv.reader(data):
                # 0 - airline code 2- source airport code 4 - destination airport code 7- stops

                if row[1] != '\\N' and l.intersection({row[0]}):
                    self.routes.append([row[0],row[2], row[4], row[7]])
                    self.s_d.append([row[2], row[4]])
                    source.add(row[2])
                    destination.add(row[4])

            routable = source.union(destination)


        # Reads airport data. Excludes airports with no IATA code
        # Excludes airports that are not routed to to reduce data length.
        with open(cwd + '/data/airports.csv', 'r') as data:
            self.airport = []
            self.IATA_airport = []
            self.city = []
            for row in csv.reader(data):
                # 2-city 3- country 4- IATA code 6-latitude 7-longitude
                if not (row[4] == '\\N') and routable.intersection({row[4]}):
                    self.airport.append([row[2],row[3], row[4], row[6],row[7]])
                    self.IATA_airport.append(row[4])
                    self.city.append(row[2])

        # Reads the input file into self.input list
        with open(cwd +'/'+ argv[-1],  'r') as data:
            self.input = [ i.strip().split(', ') for i in data.readlines()]


        return

    # Gets the IATA codes for the given location in the input.
    # Writes 'unsupported request' in file if it doesnt exist
    def inputCodes(self):
        self.input_codes = {}
        try:
            self.input_codes['source'] = self.IATA_airport[self.city.index(self.input[0][0])]
            self.input_codes['destination'] = self.IATA_airport[self.city.index(self.input[1][0])]
        except ValueError:
            self.Unsupported()
        del self.city

        print(self.input_codes)

        return

    # Checks if there is a direct flight to the destination
    def directFlight(self, source, destination):
        self.direct_l = []

        cor1 = self.coor(source)
        cor2 = self.coor(destination)


        distance = self.Harversine_f(lat1=cor1[0], lon1=cor1[1], lat2=cor2[0], lon2=cor2[1])

        try:
            i = self.s_d.index([source, destination])
            self.routes[i].append(distance)
            self.direct_l = self.routes[i]
            return
        except ValueError:return

    # checks if the is a direct flight between any of the flights leaving source and flying to destination
    # it uses data from self.routing method
    def dRFlight(self, source_set, destination_set):
        l=len(self.s_d)
        quarter_length = ceil(l/4)
        if 4*quarter_length>l:
            for i in range(l,4*quarter_length ):
                self.s_d.append(['something'])
        if len(source_set) >= len(destination_set):

            for source in source_set:

                for destination in destination_set:

                    try:

                        for n in range(4):

                            i = self.s_d.index( [source, destination], n*quarter_length,(n+1)*quarter_length)
                            break

                        cor1 = self.coor(source)
                        cor2 = self.coor(destination)

                        self.routes[i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[i])

                    except ValueError:pass


        elif len(source_set) <= len(destination_set):
            for destination in destination_set:
                for source in source_set:
                    try:

                        for n in range(4):

                            i = self.s_d.index( [source, destination], n*quarter_length,(n+1)*quarter_length)
                            break

                        cor1 = self.coor(source)
                        cor2 = self.coor(destination)

                        self.routes[i].append(self.Harversine_f(cor1[0], cor1[1], cor2[0], cor2[1]))

                        self.between.append(self.routes[i])

                    except ValueError:pass


        if 4*quarter_length>l:
            for i in range(l,4*quarter_length ):
                self.s_d.pop()

        return

    # checks for fights avaliable to a destination.
    # does this by first checking all flights leaving and arriving the source and destination
    # it then implements self.dRFlight,  self.More and set intersection to find the right flight.
    def routing(self, source, destination):

        self.journey_to.append(source)
        self.journey_from.insert(0, destination)
        self.to_dict.setdefault(source, {})
        self.to_dict.setdefault(destination, {})
        s_to = set()
        d_from = set()

        cor1 = self.coor(source)
        cor3 = self.coor(destination)
        inter = set()

        for i in range(len(self.s_d)):
            if self.s_d[i][0] == source and self.s_d[i][1] in self.IATA_airport:

                s_to.add(self.routes[i][2])
                cor2 = self.coor(self.routes[i][2])

                self.routes[i].append(self.Harversine_f(lat1=cor1[0], lon1=cor1[1], lat2=cor2[0], lon2=cor2[1]))


                self.to_dict[source][self.routes[i][2]] = self.routes[i]


            if self.s_d[i][1] == destination and self.s_d[i][0] in self.IATA_airport:
                d_from.add(self.routes[i][1])

                cor2 = self.coor(self.routes[i][1])

                self.routes[i].append(self.Harversine_f(lat1=cor3[0], lon1=cor3[1], lat2=cor2[0], lon2=cor2[1]))

                self.to_dict[destination][self.routes[i][1]] = self.routes[i]


        inter = s_to.intersection(d_from)

        if inter:
            self.inter = inter
            return

        self.dRFlight(source_set=s_to, destination_set=d_from)

        del inter

        if self.between:
            return


        else:

            if self.more:
                return
            self.more = True
            self.s_to = s_to
            self.d_from = d_from
            return self.More()


    # is implemented if one needs more than 3 flights to a destination.
    # for the sake of abnormal recursion, it caters to less than 6 flights
    def More(self):

        for i in self.s_to:
            for j in self.d_from:
                if self.between or self.inter:
                    return

                if len(self.journey_to)>1 and len(self.journey_from)>1:
                    del self.to_dict[self.journey_to[-1]]
                    del self.to_dict[self.journey_from[0]]

                    self.journey_to.pop()
                    self.journey_from.pop(0)

                self.routing(source=i, destination=j)


        return

    # the optimising function for distance
    def Optimizer(self):

        if self.more :

            if len(self.inter) > 1:
                for i in self.inter:
                    before = self.to_dict[self.journey_to[-1]][i][1]
                    after = self.to_dict[self.journey_from[0]][i][2]
                    self.cum_distance = self.to_dict[self.journey_to[0]][before][4]+self.to_dict[self.journey_to[-1]][i][4] + \
                                        self.to_dict[self.journey_from[0]][i][4] +self.to_dict[self.journey_from[-1]][after][4]

                    self.comparator(i)
                return

            elif len(self.between) > 1:
                for i in self.between:
                    before = self.to_dict[self.journey_to[-1]][i[1]][1]
                    after = self.to_dict[self.journey_from[0]][i[2]][2]

                    self.cum_distance = self.to_dict[self.journey_to[0]][before][4]+ self.to_dict[self.journey_to[-1]][i[1]][4] + i[4] + \
                                        self.to_dict[self.journey_from[0]][i[2]][4] + self.to_dict[self.journey_from[-1]][after][4]

                    self.comparator(i)
                return

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


    # for writing into file for the different options or modes
    # these modes are - 1) Direct flights 2) Two flights(inter) 3) Three flights(between) 4)More
    def Writing(self):
        with open(getcwd() + '/' + argv[-1][:-4:] + '_output.txt', 'w+') as sol:
            if self.direct_l:

                self.WriteLine(file=sol, info=self.direct_l)
                sol.write('Total flights: 1\n')
                sol.write('Total additional stops: ' + str(self.direct_l[3]) + '\n')
                sol.write('Total distance: ' + str(self.direct_l[4]) + 'km\n')
                sol.write('Optimality criteria: flights')
                return

            elif self.more:

                if self.inter:

                    if len(self.inter)==1:


                        i = list(self.inter)[0]
                        before = self.to_dict[self.journey_to[-1]][i][1]
                        after = self.to_dict[self.journey_from[0]][i][2]

                        self.WriteLine(file=sol, info=self.to_dict[self.journey_to[0]][before])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_to[-1]][i])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_from[0]][i])
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][after])

                        stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                                            int(self.to_dict[self.journey_to[-1]][i][3]) + \
                                            int(self.to_dict[self.journey_from[0]][i][3]) + \
                                            int(self.to_dict[self.journey_from[-1]][after][3])

                        self.cum_distance = self.cum_distance = self.to_dict[self.journey_to[0]][before][4] + \
                                            self.to_dict[self.journey_to[-1]][i][4] + \
                                            self.to_dict[self.journey_from[0]][i][4] + \
                                            self.to_dict[self.journey_from[-1]][after][4]


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
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][after])

                    stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                            int(self.to_dict[self.journey_to[-1]][i][3]) + \
                            int(self.to_dict[self.journey_from[0]][i][3]) + \
                            int(self.to_dict[self.journey_from[-1]][after][3])

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
                        self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][after])

                        stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                                            int(self.to_dict[self.journey_to[-1]][i[1]][3]) + int(i[3]) + \
                                            int(self.to_dict[self.journey_from[0]][i[2]][3]) + \
                                            int(self.to_dict[self.journey_from[-1]][after][3])

                        self.cum_distance = self.to_dict[self.journey_to[0]][before][4] + \
                                            self.to_dict[self.journey_to[-1]][i[1]][4] + i[4] + \
                                            self.to_dict[self.journey_from[0]][i[2]][4] + \
                                            self.to_dict[self.journey_from[-1]][after][4]

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
                    self.WriteLine(file=sol, info=self.to_dict[self.journey_from[-1]][after])

                    stops = int(self.to_dict[self.journey_to[0]][before][3]) + \
                            int(self.to_dict[self.journey_to[-1]][i[1]][3]) + int(i[3]) + \
                            int(self.to_dict[self.journey_from[0]][i[2]][3]) + \
                            int(self.to_dict[self.journey_from[-1]][after][3])


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
                sol.write('Total additional stops: ' + str(stops) + '\n')
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
                sol.write('Total additional stops: ' + str(stops) + '\n')
                sol.write('Total distance: ' + str(self.least_distance[0]) + 'km\n')
                sol.write('Optimality criteria: distance')
                return

            else:
                return sol.write("Unsupported request")
            return

    # For writing into file if request is unsupported
    def Unsupported(self):
        with open(getcwd() + '/' + argv[-1][:-4:] + '_output.txt', 'w+') as sol:
            sol.write("Unsupported request")

        exit()

    # Writing abstraction for wrinting a single line into a file
    def WriteLine(self, file, info):
        return file.write(info[0] + ' from ' + info[1] + ' to ' + info[2] + ' ' + info[3] + ' stops\n')

    # Implements or combines all the methods into single method that can be called for results
    def Final(self):
        self.openFiles()
        self.inputCodes()
        self.directFlight(source=self.input_codes['source'], destination=self.input_codes['destination'])

        if self.direct_l:
            self.Writing()
            return

        self.routing(source=self.input_codes['source'], destination=self.input_codes['destination'])
        if not(self.inter) and not(self.between):
            self.More()
        self.Optimizer()
        self.Writing()
        return


    # getting the coordinates of the place when given the IATA code
    def coor(self, IATA):
        return float(self.airport[self.IATA_airport.index(IATA)][3]), float(self.airport[self.IATA_airport.index(IATA)][4])


    # Using the Harversine to return the interger distance between 2 points. Radius of the earth is 6371km
    def Harversine_f(self, lat1, lon1,lat2, lon2):
        lon1, lat1, lon2, lat2 = radians(lon1), radians(lat1), radians(lon2), radians(lat2)
        d = int(2* 6371 * asin(sqrt(sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2)))

        return d

    # for getting the least distance form a source to a destination and storing the associated infomation for writing
    def comparator(self, keyword):
        if self.cum_distance<self.least_distance[0]:
            self.least_distance[0] = self.cum_distance
            self.least_distance[1] = keyword

        return

    # Implementation of binary search for faster searches
    # at the end, this method was not use because inbuilt search algorithms proved the same worth

    def BinarySearch(self, data, search):
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

# Function call
a.Final()
end = datetime.now()

# Supposed runtime
print(((start-end).microseconds)/1000000)

