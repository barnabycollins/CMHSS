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
                city = pickle.load(file)
            
            print(f"Data loaded from cache file '{cacheName}'.")

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


def generateScore(city: dict):
    print("Analysing city...\n")

    for i in range(len(city["points"])):
        struct = city["points"].loc[i]

        dave = tagSearch(struct, "railway")

        if (dave != None):
            print(struct.to_dict())

    print("ho ho")

    for i in range(len(city["lines"])):
        struct = city["lines"].loc[i]

        dave = tagSearch(struct, "railway")

        if (dave != None):
            print(struct.to_dict())

if (__name__ == "__main__"):
    """
    parsePBF("data/Southfields.osm.pbf")
    parsePBF("data/Durham.osm.pbf")
    parsePBF("data/Edinburgh.osm.pbf")
    parsePBF("data/London.osm.pbf")
    parsePBF("data/England.osm.pbf")
    """

    #"""
    generateScore(parsePBF("data/Newcastle.osm.pbf"))
    #"""
