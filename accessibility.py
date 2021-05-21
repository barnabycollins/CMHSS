import pydriosm.reader
import time
import json
from shapely.geometry import shape
import re
import pickle
import pandas

def parsePBF(cityFile: str, useCache: bool = True):
    cityName = re.search(r'^(?:.*\/)?([a-zA-Z]+)\.osm\.pbf$', cityFile).group(1)
    cacheName = f"./cache/{cityName}.pickle"

    if useCache:
        try:
            with open(cacheName, 'rb') as file:
                print(f"Loading data from '{cacheName}'...")
                city = pickle.load(file)
            
            print(f"Data loaded.")

        except IOError:
            useCache = False
            print(f"No cache found for '{cityName}'. Reading in city file...")

    if (not useCache):
        start = time.time()
        city = pydriosm.reader.parse_osm_pbf(cityFile, transform_other_tags=True)
        end = time.time()

        print(f"Loaded {cityFile} in {(end-start):.2f} seconds. Writing to cache...")

        with open(cacheName, 'wb') as file:
            pickle.dump(city, file)

    return city

def tagSearch(tags, item):
    
    if (isinstance(tags, pandas.Series)):
        tags = tags.to_dict()
    
    elif (tags == None):
        return None

    if (item not in tags):
        if ("other_tags" in tags):
            return tagSearch(tags["other_tags"], item)
        
        return None
    
    return tags[item]

def findTags(struct, tags):
    out = []
    for i in tags:
        out.append(tagSearch(struct, i))
    
    return out

def generateScore(city: dict):
    print("Analysing city...\n")
    

    #print("\n\n===== POINTS =====\n")

        
    stations = {}
    stationLineCounts = []
    totalStations = 0
    numWithNoLines = 0

    for i in range(len(city["points"])):
        struct = city["points"].loc[i]

        [name, railway, usage, line] = findTags(struct, ["name", "railway", "usage", "line"])

        if (railway == "station" and name != None and usage != "tourism"):
            totalStations += 1
            num_lines = 1

            if (line != None):
                print(line)
                num_lines = line.count(";") + 1
            
            else:
                numWithNoLines += 1

            #stations[name] = num_lines
            stationLineCounts.append(num_lines)
    


    print(f"\n\n===== METRO / TRAIN NETWORK REPORT =====")
    # based on https://blog.finxter.com/how-to-get-the-standard-deviation-of-a-python-list/
    averageNumLines = sum(stationLineCounts) / len(stationLineCounts)
    variance = sum([(n - averageNumLines)**2 for n in stationLineCounts]) / len(stationLineCounts)
    std = variance**0.5

    percentWithNoLines = numWithNoLines*100/totalStations
    qualityStatement = ""
    skipSection = False
    if (percentWithNoLines > 90):
        print(f"\nAn extremely small proportion ({100-percentWithNoLines:.1f}%) of stations had line data. For this reason, data is not reliable.")
        skipSection = True
    elif (percentWithNoLines > 50):
        qualityStatement = "\nThis is over 50%: treat the returned standard deviation value with caution as there are a significant number of lines that have gone unaccounted for!"
    elif (percentWithNoLines < 20):
        qualityStatement = "\nThis is less than 80%, so this value is reasonably reliable."

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

    dwellings = {
        "houses": [],
        "flats": []
    }

    schools = []

    for i in range(len(city["multipolygons"])):
        struct = city["multipolygons"].loc[i]

        [building, buildingFlats, amenity] = findTags(struct, ["building", "building:flats", "amenity"])

        if (building == "house"):
            dwellings["houses"].append(struct)
        
        elif (buildingFlats != None):
            dwellings["flats"].append(struct)
        
        elif (amenity == "school"):
            print(struct, "geometry")
            schools.append(struct)
    
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
    parsePBF("data/Seoul.osm.pbf")
    parsePBF("data/Vienna.osm.pbf")
    parsePBF("data/Edinburgh.osm.pbf")
    parsePBF("data/London.osm.pbf")
    parsePBF("data/NewYork.osm.pbf")
    parsePBF("data/England.osm.pbf")
    """

    #"""
    generateScore(parsePBF("data/Newcastle.osm.pbf"))
    #"""
