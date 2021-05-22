from utils import *
from tqdm import tqdm
import math

def analyseCity(city: dict, doTransport: bool = True, doMixedUse: bool = True, doInfrastructureComparison: bool = True):
    """Generates and returns an accessibility score for a given parsed city file"""
    print("Analysing city...\n")    

    if (doTransport):
        print(f"\n\n===== METRO / TRAIN NETWORK REPORT =====")
        
        stationLineCounts = []
        totalStations = 0
        numWithNoLines = 0

        for i in tqdm(range(len(city["points"])), desc="Analysing transport network"):
            struct = city["points"].loc[i]

            [name, railway, usage, line] = findTags(struct, ["name", "railway", "usage", "line"])

            if (railway == "station" and name != None and usage != "tourism"):
                totalStations += 1
                num_lines = 1

                if (line != None):
                    num_lines = line.count(";") + 1
                
                else:
                    numWithNoLines += 1

                #stations[name] = num_lines
                stationLineCounts.append(num_lines)
        
        
        # based on https://blog.finxter.com/how-to-get-the-standard-deviation-of-a-python-list/
        averageNumLines = sum(stationLineCounts) / len(stationLineCounts)
        variance = sum([(n - averageNumLines)**2 for n in stationLineCounts]) / len(stationLineCounts)
        std = variance**0.5

        print()

        percentWithNoLines = numWithNoLines*100/totalStations
        qualityStatement = ""
        skipSection = False
        if (percentWithNoLines == 0):
            qualityStatement = f"\nAll stations had line information. This value is very reliable."
        elif(percentWithNoLines > 90):
            print(f"\nAn extremely small proportion ({100-percentWithNoLines:.1f}%) of stations had line data. For this reason, data is not reliable.")
            skipSection = True
        elif (percentWithNoLines > 50):
            qualityStatement = "\nThis is over 50%: treat the returned standard deviation value with caution as there are a significant number of lines that have gone unaccounted for!"
        elif (percentWithNoLines < 20):
            qualityStatement = "\nThis is less than 20%, so this value is reasonably reliable."

        if (not skipSection):
            print(f"Standard deviation in number of lines per station is {std}.")
            print(f"{percentWithNoLines:.1f}% of stations had no line information.{qualityStatement}")

    if (doMixedUse):
        dwellings = []

        schools = []
        retail = []
        supermarkets = []
        busStops = []
        playgrounds = []
        doctors = []
        
        # POINTS
        for i in tqdm(range(len(city["points"])), desc="Getting point data"):
            struct = city["points"].loc[i]
            coordinate = struct["coordinates"]
            
            [building, amenity, shop, highway, railway, leisure] = findTags(struct, ["building", "amenity", "shop", "highway", "railway", "leisure"])

            if (amenity == "doctors"):
                doctors.append(coordinate)

            """if (highway == "bus_stop" or railway == "tram_stop"):
                busStops.append(coordinate)

            elif (building == "retail"):
                retail.append(coordinate)
            
                if (shop == "supermarket"):
                    supermarkets.append(coordinate)
            
            elif (amenity == "school"):
                schools.append(coordinate)
            
            elif (leisure == "playground"):
                playgrounds.append(coordinate)
            
            elif (amenity == "doctors"):
                doctors.append(coordinate)"""

        # AREAS
        for i in tqdm(range(len(city["multipolygons"])), desc="Getting building data"):
            struct = city["multipolygons"].loc[i]
            coordinate = getCoord(struct["coordinates"])

            [building, buildingFlats, amenity, shop, leisure] = findTags(struct, ["building", "building:flats", "amenity", "shop", "leisure"])
            
            if (buildingFlats != None):
                dwellings.append((buildingFlats, coordinate))
            
            elif (building == "house"):
                dwellings.append((1, coordinate))
            
            elif (building == "apartments"):
                dwellings.append((30, coordinate))
            
            elif (building == "residential"):
                dwellings.append((3, coordinate))
            
            elif (amenity == "doctors"):
                doctors.append(coordinate)
            
            """elif (building == "retail"):
                retail.append(coordinate)

                if (shop == "supermarket"):
                    supermarkets.append(coordinate)
            
            elif (amenity == "school"):
                schools.append(coordinate)
            
            elif (leisure == "playground"):
                playgrounds.append(coordinate)
            
            elif (amenity == "doctors"):
                doctors.append(coordinate)"""
        

        [schools, retail, supermarkets, busStops, playgrounds, doctors] = sortByLongitude([schools, retail, supermarkets, busStops, playgrounds, doctors])
        
        totalHouseholds = 0
        totalDistance_Schools = 0
        totalDistance_Shops = 0
        totalDistance_Supermarkets = 0
        totalDistance_BusStops = 0
        totalDistance_Playgrounds = 0
        totalDistance_Doctors = 0
        for h in tqdm(dwellings, desc="Analysing zoning"):
            coords = h[1]
            numHouseholds = h[0]
            if (type(numHouseholds) != int):
                try:
                    numHouseholds = int(numHouseholds)
                except:
                    numHouseholds = 5
            
            if (len(schools) != 0):
                totalDistance_Schools += numHouseholds * findMinDistance(coords, schools)
            
            if (len(retail) != 0):
                totalDistance_Shops += numHouseholds * findMinDistance(coords, retail)
            
            if (len(supermarkets) != 0):
                totalDistance_Supermarkets += numHouseholds * findMinDistance(coords, supermarkets)
            
            if (len(busStops) != 0):
                totalDistance_BusStops += numHouseholds * findMinDistance(coords, busStops)
            
            if (len(playgrounds) != 0):
                totalDistance_Playgrounds += numHouseholds * findMinDistance(coords, playgrounds)
            
            if (len(doctors) != 0):
                totalDistance_Doctors += numHouseholds * findMinDistance(coords, doctors)
                
            totalHouseholds += numHouseholds
        
        print()

        if (totalDistance_Schools != 0):
            avgDistanceToSchool = totalDistance_Schools / totalHouseholds
            print(f"Average distance to school: {avgDistanceToSchool*1000:.0f}m")
        
        if (totalDistance_Shops != 0):
            avgDistanceToShops = totalDistance_Shops / totalHouseholds
            print(f"Average distance to shop: {avgDistanceToShops*1000:.0f}m")
        
        if (totalDistance_Supermarkets != 0):
            avgDistanceToSupermarkets = totalDistance_Supermarkets / totalHouseholds
            print(f"Average distance to supermarket: {avgDistanceToSupermarkets*1000:.0f}m")
        
        if (totalDistance_BusStops != 0):
            avgDistanceToBusStops = totalDistance_BusStops / totalHouseholds
            print(f"Average distance to bus (or tram) stop: {avgDistanceToBusStops*1000:.0f}m")
        
        if (totalDistance_Playgrounds != 0):
            avgDistanceToPlaygrounds = totalDistance_Playgrounds / totalHouseholds
            print(f"Average distance to playground: {avgDistanceToPlaygrounds*1000:.0f}m")
        
        if (totalDistance_Doctors != 0):
            avgDistanceToDoctors = totalDistance_Doctors / totalHouseholds
            print(f"Average distance to doctor: {avgDistanceToDoctors*1000:.0f}m")
    


    if (doInfrastructureComparison):
        parkingSpaces = 0
        busStops = 0
        stations = 0
        
        for i in tqdm(range(len(city["points"])), desc="Getting point data"):
            struct = city["points"].loc[i]
            coordinate = struct["coordinates"]
            
            [amenity, capacity, highway, railway] = findTags(struct, ["amenity", "capacity", "highway", "railway"])

            if (highway == "bus_stop" or railway == "tram_stop"):
                busStops += 1
            
            elif (railway == "station" or railway == "halt"):
                stations += 1
            
            elif (amenity == "parking"):
                if (type(capacity) != int):
                    try:
                        capacity = int(capacity)
                    except:
                        capacity = 100
                
                parkingSpaces += capacity
        

        for i in tqdm(range(len(city["multipolygons"])), desc="Getting building data"):
            struct = city["multipolygons"].loc[i]
            coordinate = getCoord(struct["coordinates"])
            
            [amenity, capacity] = findTags(struct, ["amenity", "capacity"])
            
            if (amenity == "parking"):
                if (type(capacity) != int):
                    try:
                        capacity = int(capacity)
                    except:
                        capacity = 200
                
                parkingSpaces += capacity
        
        print()
        
        if (parkingSpaces > 0):
            if (busStops > 0):
                parkingSpacesPerBusStop = parkingSpaces / busStops
                print(f"Parking spaces per bus (or tram) stop: {parkingSpacesPerBusStop}")
            
            if (stations > 0):
                parkingSpacesPerStation = parkingSpaces / stations
                print(f"Parking spaces per train station: {parkingSpacesPerStation}")
            
            if (busStops > 0 and stations > 0):
                weightedRatio = parkingSpaces / (stations * 20 + busStops)
                print(f"Parking spaces divided by (train stations x 20 + bus stops): {weightedRatio}")


    """
    print("\n\n===== LINES =====\n")
    for i in range(len(city["lines"])):
        struct = city["lines"].loc[i]

        name = tagSearch(struct, "name")
        railway = tagSearch(struct, "railway")

        if (railway == "station" and name != None):
            print(name)
    

    print("\n\n===== MULTILINESTRINGS =====\n")
    for i in range(len(city["multilinestrings"])):
        struct = city["multilinestrings"].loc[i]

        [name, route, fr0m, t0, via] = findTags(struct, ["name", "route", "from", "to", "via"])

        if (route == "train"):
            print(f"\n{name}:\nFrom {fr0m} to {t0}\nVia {via}")
    

    print("\n\n===== OTHER RELATIONS =====\n")
    for i in range(len(city["other_relations"])):
        struct = city["other_relations"].loc[i]

        name = tagSearch(struct, "name")
        railway = tagSearch(struct, "railway")

        if (railway == "station" and name != None):
            print(name)
    """
