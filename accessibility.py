import pydriosm.reader
import time
import json
from shapely.geometry import shape
import re
import pickle

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
            print(f"No cache found. Reading in city file '{cityName}'...")

    if (not useCache):
        start = time.time()
        city = pydriosm.reader.parse_osm_pbf(cityFile)
        end = time.time()

        print(f"Loaded {cityFile} in {(end-start):.2f} seconds. Writing to cache...")

        with open(cacheName, 'wb') as file:
            pickle.dump(city, file)

    return city

def generateScore(city: dict):
    print("Analysing city...\n")

    for i in city["points"]["points"]:
        struct = json.loads(i)
        geometry = struct["geometry"]
        tags = struct["properties"]
        
        if (tags.get("railway") == "station" or tags.get("railway") == "halt" or tags.get("public_transport" == "station")):
            print(tags.get("name"))

if (__name__ == "__main__"):
    parsePBF("data/Durham.osm.pbf")
    parsePBF("data/Edinburgh.osm.pbf")
    parsePBF("data/Southfields.osm.pbf")
