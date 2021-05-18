import pydriosm.reader
import time
import json
from shapely.geometry import shape

def generateScore(cityFile: str):
    start = time.time()
    city = pydriosm.reader.parse_osm_pbf(cityFile)
    end = time.time()

    print(f"Loaded data from {cityFile} in {end-start} seconds.\nAnalysing...\n")

    for i in cityFile["points"]["points"]:
        geometry = i["geometry"]
        tags = i["properties"]