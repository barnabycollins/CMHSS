import pydriosm.reader
import time
import json

print("k cool")

start = time.time()
southfields = pydriosm.reader.parse_osm_pbf("data/Southfields.osm.pbf")
end = time.time()

# 6 seconds
print(f"bam... all done. Loaded Southfields ({sum([len(southfields[i]) for i in southfields])} things) in {end-start} seconds.")

for i in ["points", "lines", "multilinestrings"]:

    feature = json.loads(southfields[i][i][0])
    print(f"\n{i} - {feature['properties']['name']} ({feature['properties']['osm_id']}):")

    for j in feature["geometry"]["coordinates"]:
        print(j)


"""
start = time.time()
durham = pydriosm.reader.parse_osm_pbf("data/Durham.osm.pbf")
end = time.time()

# 32 seconds
print(f"bam... all done. Loaded Durham ({sum([len(durham[i]) for i in durham])} things) in {end-start} seconds.")

for i in durham:
    print(durham[i][0])
"""

"""
start = time.time()
edinburgh = pydriosm.reader.parse_osm_pbf("data/Edinburgh.osm.pbf")
end = time.time()

# 6.5 mins
print(f"bam... all done. Loaded Edinburgh ({sum([len(edinburgh[i]) for i in edinburgh])} things) in {end-start} seconds.")

start = time.time()
england = pydriosm.reader.parse_osm_pbf("data/england-latest.osm.pbf")
end = time.time()

# 51 mins
print(f"bam... all done. Loaded Engerland ({sum([len(england[i]) for i in england])} things) in {end-start} seconds. 😳")
"""