import pydriosm.reader
import time
import json
import mercantile # handles conversion from co-ords to tiles
import geotiler # allows you to get actual map tile images



""" yucky
def findExtentFromFeatures(data):
    def findExtentFromList(stuff):
        extent = [1e308, 1e308, -1e308, -1e308]

        if (type(stuff) != list):
            return extent 
        
        for i in stuff:
            result = recursiveCoordSearch(i)

            print(result)

            extent[0] = min(extent[0], result[0])
            extent[1] = min(extent[1], result[1])
            extent[2] = max(extent[2], result[2])
            extent[3] = max(extent[3], result[3])


    def recursiveCoordSearch(thing):
        extent = [1e308, 1e308, -1e308, -1e308]

        print(thing)
        
        if (type(thing) != list):
            return extent
        

        if (type(thing[0]) != float):
            extent = findExtentFromList(thing)
        
        elif (type(thing[0]) == float and type(thing[1]) == float):
            extent = [thing[0], thing[1], thing[0], thing[1]]

        return extent
    

    outerResults = []
    for i in ["points", "lines", "multilinestrings"]:
        results = []
        for j in data[i][i]:
            results.append(recursiveCoordSearch(json.loads(j)['geometry']['coordinates']))
        
        outerResults.append(findExtentFromList(results))
    
    return findExtentFromList(outerResults)
"""

print("k cool")

start = time.time()
southfields = pydriosm.reader.parse_osm_pbf("data/Southfields.osm.pbf")
end = time.time()

map = geotiler.Map(center=(-0.20649, 51.44475), zoom=14, size=(512, 512))

# 6 seconds
print(f"bam... all done. Loaded Southfields ({sum([len(southfields[i]) for i in southfields])} things) in {end-start} seconds.")

for i in southfields:

    print(southfields[i])

    """feature = json.loads(southfields[i][i][0])
    print(f"\n{i} - {feature['properties']['name']} ({feature['properties']['osm_id']}):")

    print(feature)"""

    #for j in feature["geometry"]["coordinates"]:
    #    print(j)


image = geotiler.render_map(map)

image.save('./maps/southfields.png')

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