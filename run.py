from main import analyseCity
from utils import parsePBF

# ===== HELPER SCRIPT =====
# This program can be used as a starting point to run analysis on cities in batches!
# It was written for the datasets I used, but obviously can be trivially adjusted 
#   for other exported maps :)

# All cities used (in ascending order of file size)
# These exact files can be downloaded from the link in README.txt, but any file
#   extracted using the tool at extract.BBBike.org will work!
all = [
    "data/Durham.osm.pbf",
    "data/Oxford.osm.pbf",
    "data/York.osm.pbf",
    "data/Cardiff.osm.pbf",
    "data/Glasgow_Small.osm.pbf",
    "data/Manchester.osm.pbf",
    "data/Southampton.osm.pbf",
    "data/Newcastle.osm.pbf",
    "data/Liverpool.osm.pbf",
    "data/SouthLondon.osm.pbf",
    "data/Glasgow_Big.osm.pbf",
    "data/Edinburgh.osm.pbf",
    "data/NorthLondon.osm.pbf",
    "data/Dublin.osm.pbf",
    "data/Seoul.osm.pbf",
    "data/Vienna.osm.pbf",
    "data/Birmingham.osm.pbf",
    "data/CentralLondon.osm.pbf",
    "data/London.osm.pbf",
    "data/NewYork.osm.pbf"
]

# Some subset of cities (to be edited as desired)
subset = [
    "data/Durham.osm.pbf",
]

# Use this to decide whether to run for all cities or for a subset as defined above
citiesToUse = subset

# Enable to generate cache files for all cities in citiesToUse
parse = False

# Enable to analyse all cities in citiesToUse
analyse = True

if (parse):
    for city in citiesToUse:
        parsePBF(city)
        print("\n")

if (analyse):
    for city in citiesToUse:
        analyseCity(
            parsePBF(city),
            doTransitNetwork = True,
            doMixedUse = True,
            doInfrastructureComparison = True
        )
        print("\n")
