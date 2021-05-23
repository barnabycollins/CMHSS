from main import analyseCity
from utils import parsePBF

all = [
    "data/Southfields.osm.pbf",
    "data/Durham.osm.pbf",
    "data/Oxford.osm.pbf",
    "data/Cardiff.osm.pbf",
    "data/Manchester.osm.pbf",
    "data/Southampton.osm.pbf",
    "data/Newcastle.osm.pbf",
    "data/Liverpool.osm.pbf",
    "data/SouthLondon.osm.pbf",
    "data/Glasgow.osm.pbf",
    "data/Edinburgh.osm.pbf",
    "data/NorthLondon.osm.pbf",
    "data/Dublin.osm.pbf",
    "data/Seoul.osm.pbf",
    "data/Vienna.osm.pbf",
    "data/Birmingham.osm.pbf",
    "data/CentralLondon.osm.pbf",
    "data/London.osm.pbf",
    "data/NewYork.osm.pbf",
    #"data/England.osm.pbf"
]

new = [
    "data/Southampton.osm.pbf"
]

parseAll = False
analyseAll = True
citiesToUse = new

if (parseAll):
    for city in citiesToUse:
        parsePBF(city)
        print()

if (analyseAll):
    for city in citiesToUse:
        analyseCity(parsePBF(city), doTransport=True, doMixedUse=False, doInfrastructureComparison=False)
        print()

"""
analyseCity(parsePBF("data/Seoul.osm.pbf"), doTransport=False, doMixedUse=True)
"""
