from utils import *
from tqdm import tqdm
import math

def generateScore(city: dict, doTransport = True, doMixedUse = True):
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

        for i in tqdm(range(len(city["multipolygons"])), desc="Getting building data"):
            struct = city["multipolygons"].loc[i]
            coordinate = getCoord(struct["coordinates"])

            [building, buildingFlats, amenity] = findTags(struct, ["building", "building:flats", "amenity"])
            
            if (buildingFlats != None):
                dwellings.append((buildingFlats, coordinate))
            
            elif (building == "house"):
                dwellings.append((1, coordinate))
            
            elif (building == "apartments"):
                dwellings.append((30, coordinate))
            
            elif (building == "residential"):
                dwellings.append((3, coordinate))
            
            elif (amenity == "school"):
                schools.append(coordinate)
        
        schools = sorted(schools, key=lambda x: x[0])

        totalHouseholds = 0
        totalDistance = 0
        for h in tqdm(dwellings, desc="Analysing zoning"):
            coords = h[1]
            numHouseholds = h[0]

            nearest = findMinDistance(coords, schools)

            if (type(numHouseholds) != int):
                try:
                    numHouseholds = int(numHouseholds)
                
                except:
                    numHouseholds = 5
                
            totalHouseholds += numHouseholds
            totalDistance += numHouseholds * nearest

        avgDistanceToSchool = totalDistance / totalHouseholds
        
        print(f"Average distance to school: {avgDistanceToSchool*1000:.0f}m")

    
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
    """
    parsePBF("data/Southfields.osm.pbf")
    parsePBF("data/Durham.osm.pbf")
    parsePBF("data/Newcastle.osm.pbf")
    parsePBF("data/Seoul.osm.pbf")
    parsePBF("data/Vienna.osm.pbf")
    parsePBF("data/Edinburgh.osm.pbf")
    parsePBF("data/London.osm.pbf")
    parsePBF("data/NewYork.osm.pbf")
    parsePBF("data/England.osm.pbf")
    """

    #"""
    generateScore(parsePBF("data/NewYork.osm.pbf"), doTransport=False, doMixedUse=True)
    #"""
