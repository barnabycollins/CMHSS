from utils import *
from tqdm import tqdm
import math

def generateScore(city: dict, doTransport: bool = True, doMixedUse: bool = True):
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

    """
    print("\n\n===== LINES =====\n")

    
    for i in range(len(city["lines"])):
        struct = city["lines"].loc[i]

        name = tagSearch(struct, "name")
        railway = tagSearch(struct, "railway")

        if (railway == "station" and name != None):
            print(name)
    """
    
    """
    print("\n\n===== MULTILINESTRINGS =====\n")


    for i in range(len(city["multilinestrings"])):
        struct = city["multilinestrings"].loc[i]

        [name, route, fr0m, t0, via] = findTags(struct, ["name", "route", "from", "to", "via"])

        if (route == "train"):
            print(f"\n{name}:\nFrom {fr0m} to {t0}\nVia {via}")

    print("\n\n===== MULTIPOLYGONS =====\n")
    """

    if (doMixedUse):
        dwellings = []

        schools = []
        retail = []
        supermarkets = []

        for i in tqdm(range(len(city["multipolygons"])), desc="Getting building data"):
            struct = city["multipolygons"].loc[i]
            coordinate = getCoord(struct["coordinates"])

            [building, buildingFlats, amenity, shop] = findTags(struct, ["building", "building:flats", "amenity", "shop"])
            
            if (buildingFlats != None):
                dwellings.append((buildingFlats, coordinate))
            
            elif (building == "house"):
                dwellings.append((1, coordinate))
            
            elif (building == "apartments"):
                dwellings.append((30, coordinate))
            
            elif (building == "residential"):
                dwellings.append((3, coordinate))
            
            elif (building == "retail"):
                retail.append(coordinate)

                if (shop == "supermarket"):
                    supermarkets.append(coordinate)
            
            elif (amenity == "school"):
                schools.append(coordinate)
        
        [schools, retail, supermarkets] = sortByLongitude([schools, retail, supermarkets])
        
        totalHouseholds = 0
        totalDistance_Schools = 0
        totalDistance_Shops = 0
        totalDistance_Supermarkets = 0
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
                
            totalHouseholds += numHouseholds

        if (totalDistance_Schools != 0):
            avgDistanceToSchool = totalDistance_Schools / totalHouseholds
            print(f"Average distance to school: {avgDistanceToSchool*1000:.0f}m")
        
        if (totalDistance_Shops != 0):
            avgDistanceToShops = totalDistance_Shops / totalHouseholds
            print(f"Average distance to shop: {avgDistanceToShops*1000:.0f}m")
        
        if (totalDistance_Supermarkets != 0):
            avgDistanceToSupermarkets = totalDistance_Supermarkets / totalHouseholds
            print(f"Average distance to supermarket: {avgDistanceToSupermarkets*1000:.0f}m")

    
    """
    print("\n\n===== OTHER RELATIONS =====\n")


    for i in range(len(city["other_relations"])):
        struct = city["other_relations"].loc[i]

        name = tagSearch(struct, "name")
        railway = tagSearch(struct, "railway")

        if (railway == "station" and name != None):
            print(name)
    """


if (__name__ == "__main__"):
    parseAll = False
    analyseAll = True
    all = [
        "data/Southfields.osm.pbf",
        "data/Durham.osm.pbf",
        "data/Newcastle.osm.pbf",
        "data/SouthLondon.osm.pbf",
        "data/Glasgow.osm.pbf",
        "data/Edinburgh.osm.pbf",
        "data/NorthLondon.osm.pbf",
        "data/Seoul.osm.pbf",
        "data/Vienna.osm.pbf",
        "data/CentralLondon.osm.pbf",
        "data/London.osm.pbf",
        "data/NewYork.osm.pbf",
        #"data/England.osm.pbf"
    ]

    new = [
        "data/SouthLondon.osm.pbf",
        "data/NorthLondon.osm.pbf",
        "data/CentralLondon.osm.pbf"
    ]

    citiesToUse = all

    if (parseAll):
        for city in citiesToUse:
            parsePBF(city)

    if (analyseAll):
        for city in citiesToUse:
            generateScore(parsePBF(city), doTransport=True, doMixedUse=False)
    """
    generateScore(parsePBF("data/Seoul.osm.pbf"), doTransport=False, doMixedUse=True)
    """
