import pydriosm.reader
import time
import re
import pickle
import pandas
import math

def parsePBF(cityFile: str, useCache: bool = True, writeCache: bool = True):
    """Parses a named .osm.pbf file into a Python structure and returns it.
        Writes loaded files to a cache directory to save time in future, and
        reads any matching cache file back if it exists (both by default)
        - cityFile: should be relative to the working directory or otherwise absolute
        - useCache: set false to force reading from the PBF instead of cache
        - writeCache: set false to stop the function writing to cache
    """

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

        if (writeCache):
            with open(cacheName, 'wb') as file:
                pickle.dump(city, file)
            print(f"Wrote pickle file to '{cacheName}'.")

    return city


def tagSearch(tags: dict, item: str):
    """Searches for a tag with the name 'item' in the given structure.
        Returns the value of that tag, or otherwise None if not present.
        - tags: the structure to search
        - item: the tag name to search for
    """
    
    if (isinstance(tags, pandas.Series)):
        tags = tags.to_dict()
    
    elif (tags == None):
        return None

    if (item not in tags):
        if ("other_tags" in tags):
            return tagSearch(tags["other_tags"], item)
        
        return None
    
    return tags[item]


def findTags(struct: dict, tags: list):
    """Bulk searches for tags in a structure, and returns them in the same order as given.
        - struct: the structure to be searched
        - tags: an ordered list of tag names to be returned in a list with the same order
    """
    out = []
    for i in tags:
        out.append(tagSearch(struct, i))
    
    return out


def getCoord(coordinates: list):
    """Returns a single co-ordinate pair from the given arbitrary set of co-ordinates
        Recursively traverses down the layers of a nested list until a pair of floats is located.
        Useful as a metric for roughly where an object is.
        - coordinates: an arbitrarily structured nested list of co-ordinates
    """
    if (type(coordinates[0]) != float):
        return getCoord(coordinates[0])
    
    else:
        if (len(coordinates) == 2):
            return coordinates
        
        else:
            return None


def findDistance(coord1: list, coord2: list):
    """Calculates the rough surface distance between two lat/long co-ordinate pairs
        Adapted from https://stackoverflow.com/a/19412565
        - coord1: the first co-ordinate
        - coord2: the second co-ordinate
    """

    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(coord1[1])
    lon1 = radians(coord1[0])
    lat2 = radians(coord2[1])
    lon2 = radians(coord2[0])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def findMinDistance_Naive(centre: list, locations: list):
    """Exhaustively enumerates locations to find the nearest one to the centre point,
        and returns the distance between these two points.
        - centre: the reference point to search for nearest neighbours to
        - locations: the list of co-ordinates to search for the neighbours/
    """
    distances = []

    for s in locations:
        distances.append(findDistance(centre, s))
    
    return min(distances)


def findLongitudeRange(centre: list, distance: list):
    """Given a distance and a centre point, find the two longitudes
        at that distance east and west of that point.
        - centre: the point to compute the range either side of
        - distance: the distance in kilometres to cover either side of the centre point
    """
    # approximate circumference of earth in km
    C = 40042.0

    dL = (distance / C) * 360 + 0.05

    return (centre - dL, centre + dL)


def sortByLongitude(lists: list):
    """Sorts the given list of co-ordinate lists by longitude and returns them (in order)."""

    sortedLists = []
    for item in lists:
        sortedLists.append(sorted(item, key=lambda x: x[0]))
    
    return sortedLists


def findMinDistance(centre: list, locations: list):
    """Finds the distance from 'centre' to the nearest co-ordinate in 'locations'.
        First samples a few locations, then takes the distance to the nearest and
        ignores any co-ordinates that are further in longitude than that distance.
        - centre: a pair of co-ordinates in the format [longitude, latitude]
        - locations: a list of co-ordinates in the above format, SORTED BY LONGITUDE!
    """
    
    distances = []

    n_locations = len(locations)
    n_samples = min(n_locations, 100)

    for s in range(n_samples):
        sampleLoc = locations[math.floor(s * (n_locations / n_samples))]
        distances.append(findDistance(centre, sampleLoc))

    if (n_locations > n_samples):

        nearest = min(distances)
        rangeToSearch = findLongitudeRange(centre[0], nearest)
        distances = [nearest]

        for l in locations:
            if (l[0] < rangeToSearch[0]):
                continue

            elif (l[0] > rangeToSearch[1]):
                break

            distances.append(findDistance(centre, l))

    nearest = min(distances)

    return nearest
        