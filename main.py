from utils import *
from tqdm import tqdm

def analyseCity(city: dict, doTransitNetwork: bool = True, doMixedUse: bool = True, doInfrastructureComparison: bool = True):
    """Generates and returns accessibility for a given parsed city file.
        - city: an OSM PBF file, after being parsed by utils.parsePBF()
        - doTransitNetwork: Boolean deciding whether to find standard deviation in line connectedness across stations
        - doMixedUse: Boolean deciding whether to measure average distances between houses and facilities
        - doInfratructureComparison: Boolean deciding whether to find ratios of parking spaces vs other transit infrastructure
    """

    print("Beginning analysis...\n\n")


    # FINDING STANDARD DEVIATION OF STATION CONNECTEDNESS
    if doTransitNetwork:
        print(f"===== TRANSPORT NETWORK DESIGN =====")
        
        stationLineCounts = []
        totalStations = 0
        numWithNoLines = 0

        # Enumerate stations, collecting the numbers of lines into stationLineCounts
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

                stationLineCounts.append(num_lines)
        
        # Find standard deviation
        averageNumLines = sum(stationLineCounts) / len(stationLineCounts)
        variance = sum([(count - averageNumLines)**2 for count in stationLineCounts]) / len(stationLineCounts)
        std = variance**0.5

        print()

        # Output results, with a message decided by the proportion of stations with line information
        percentWithNoLines = numWithNoLines*100/totalStations
        qualityStatement = ""
        skipOutput = False
        if (percentWithNoLines == 0):
            qualityStatement = f"\n Since all stations had line information, this value is very reliable."
        elif (percentWithNoLines < 20):
            qualityStatement = "\nThis is less than 20%, so this value is reasonably reliable."
        elif (percentWithNoLines > 95):
            print(f"An extremely small proportion ({100-percentWithNoLines:.1f}%) of stations had line data. For this reason, data is not reliable.")
            skipOutput = True
        elif (percentWithNoLines > 50):
            qualityStatement = "\nThis is over 50%: treat the returned standard deviation value with caution as there are a significant number of lines that have gone unaccounted for!"

        # If the value is useless, don't print it
        if (not skipOutput):
            print(f"Standard deviation in number of lines per station is {std:.3f}.")
            print(f"{percentWithNoLines:.1f}% of stations had no line information.{qualityStatement}")

        print("\n")


    # FINDING AVERAGE DISTANCE FROM A HOUSE TO FACILITIES
    if (doMixedUse):
        print(f"===== MIXED-USE ZONING =====")

        dwellings = []

        schools = []
        retail = []
        supermarkets = []
        busStops = []
        playgrounds = []
        doctors = []
        
        # COLLECTING RELEVANT POINT FEATURES
        for i in tqdm(range(len(city["points"])), desc="Getting point data"):
            struct = city["points"].loc[i]
            coordinate = struct["coordinates"]
            
            [building, amenity, shop, highway, railway, leisure] = findTags(struct, ["building", "amenity", "shop", "highway", "railway", "leisure"])

            # Considering bus stops and tram stops to be equivalent
            if (highway == "bus_stop" or railway == "tram_stop"):
                busStops.append(coordinate)

            elif (building == "retail"):
                retail.append(coordinate)
            
                if (shop == "supermarket"):
                    supermarkets.append(coordinate)
            
            elif (amenity == "school"):
                schools.append(coordinate)
            
            elif (leisure == "playground"):
                playgrounds.append(coordinate)
            
            elif (amenity == "doctors"):
                doctors.append(coordinate)

        # COLLECTING RELEVANT POLYGON FEATURES
        for i in tqdm(range(len(city["multipolygons"])), desc="Getting building data"):
            struct = city["multipolygons"].loc[i]
            coordinate = getCoord(struct["coordinates"])

            [building, buildingFlats, amenity, shop, leisure] = findTags(struct, ["building", "building:flats", "amenity", "shop", "leisure"])
            
            # If the building specifies how many households are inside it, use that
            if (buildingFlats != None):
                dwellings.append((buildingFlats, coordinate))
            
            # Otherwise, use reasonable estimates
            elif (building == "house"):
                dwellings.append((1, coordinate))
            
            elif (building == "apartments"):
                dwellings.append((30, coordinate))
            
            elif (building == "residential"):
                dwellings.append((3, coordinate))
            
            # Also collect other relevant area types            
            elif (amenity == "doctors"):
                doctors.append(coordinate)
            
            elif (building == "retail"):
                retail.append(coordinate)

                if (shop == "supermarket"):
                    supermarkets.append(coordinate)
            
            elif (amenity == "school"):
                schools.append(coordinate)
            
            elif (leisure == "playground"):
                playgrounds.append(coordinate)
            
            elif (amenity == "doctors"):
                doctors.append(coordinate)
        

        # FINDING AVERAGE DISTANCES

        # Sort lists by longitude for findMinDistance()
        [schools, retail, supermarkets, busStops, playgrounds, doctors] = sortByLongitude([schools, retail, supermarkets, busStops, playgrounds, doctors])
        
        totalHouseholds = 0
        totalDistance_Schools = 0
        totalDistance_Shops = 0
        totalDistance_Supermarkets = 0
        totalDistance_BusStops = 0
        totalDistance_Playgrounds = 0
        totalDistance_Doctors = 0

        # For each house, find minimum distances to relevant facilities
        for h in tqdm(dwellings, desc="Analysing zoning"):
            coords = h[1]
            numHouseholds = h[0]
            if (type(numHouseholds) != int):
                try:
                    numHouseholds = int(numHouseholds)
                except:
                    numHouseholds = 5
            
            if (len(schools) != 0):
                totalDistance_Schools += numHouseholds * findMinDistance(coords, schools)
            
            if (len(retail) != 0):
                totalDistance_Shops += numHouseholds * findMinDistance(coords, retail)
            
            if (len(supermarkets) != 0):
                totalDistance_Supermarkets += numHouseholds * findMinDistance(coords, supermarkets)
            
            if (len(busStops) != 0):
                totalDistance_BusStops += numHouseholds * findMinDistance(coords, busStops)
            
            if (len(playgrounds) != 0):
                totalDistance_Playgrounds += numHouseholds * findMinDistance(coords, playgrounds)
            
            if (len(doctors) != 0):
                totalDistance_Doctors += numHouseholds * findMinDistance(coords, doctors)
                
            totalHouseholds += numHouseholds
        
        print()

        # Print all items that we have data for
        if (totalDistance_Schools != 0):
            avgDistanceToSchool = totalDistance_Schools / totalHouseholds
            print(f"Average distance to school: {avgDistanceToSchool*1000:.0f}m")
        
        if (totalDistance_Shops != 0):
            avgDistanceToShops = totalDistance_Shops / totalHouseholds
            print(f"Average distance to shop: {avgDistanceToShops*1000:.0f}m")
        
        if (totalDistance_Supermarkets != 0):
            avgDistanceToSupermarkets = totalDistance_Supermarkets / totalHouseholds
            print(f"Average distance to supermarket: {avgDistanceToSupermarkets*1000:.0f}m")
        
        if (totalDistance_BusStops != 0):
            avgDistanceToBusStops = totalDistance_BusStops / totalHouseholds
            print(f"Average distance to bus (or tram) stop: {avgDistanceToBusStops*1000:.0f}m")
        
        if (totalDistance_Playgrounds != 0):
            avgDistanceToPlaygrounds = totalDistance_Playgrounds / totalHouseholds
            print(f"Average distance to playground: {avgDistanceToPlaygrounds*1000:.0f}m")
        
        if (totalDistance_Doctors != 0):
            avgDistanceToDoctors = totalDistance_Doctors / totalHouseholds
            print(f"Average distance to doctor: {avgDistanceToDoctors*1000:.0f}m")
    
        print("\n")


    # FINDING RATIOS OF PARKING SPACES TO TRANSIT INFRASTRUCTURE
    if (doInfrastructureComparison):
        print(f"===== INFRASTRUCTURE RATIOS =====")

        parkingSpaces = 0
        busStops = 0
        stations = 0
        
        # COLLECT RELEVANT POINT FEATURES
        for i in tqdm(range(len(city["points"])), desc="Getting point data"):
            struct = city["points"].loc[i]
            coordinate = struct["coordinates"]
            
            [amenity, capacity, highway, railway] = findTags(struct, ["amenity", "capacity", "highway", "railway"])

            if (highway == "bus_stop" or railway == "tram_stop"):
                busStops += 1
            
            elif (railway == "station" or railway == "halt"):
                stations += 1
            
            elif (amenity == "parking"):
                if (type(capacity) != int):
                    try:
                        capacity = int(capacity)
                    except:
                        # Use a reasonable estimate
                        capacity = 100
                
                parkingSpaces += capacity
        
        # COLLECT RELEVANT POLYGON FEATURES
        for i in tqdm(range(len(city["multipolygons"])), desc="Getting building data"):
            struct = city["multipolygons"].loc[i]
            coordinate = getCoord(struct["coordinates"])
            
            [amenity, capacity] = findTags(struct, ["amenity", "capacity"])
            
            if (amenity == "parking"):
                if (type(capacity) != int):
                    try:
                        capacity = int(capacity)
                    except:
                        # Use a reasonable estimate
                        #   (larger than above as larger car parks are more likely to be represented by areas)
                        capacity = 200
                
                parkingSpaces += capacity
        
        print()
        
        # Print results if we have data for them
        if (parkingSpaces > 0):
            if (busStops > 0):
                parkingSpacesPerBusStop = parkingSpaces / busStops
                print(f"Parking spaces per bus (or tram) stop: {parkingSpacesPerBusStop:.2f}")
            
            if (stations > 0):
                parkingSpacesPerStation = parkingSpaces / stations
                print(f"Parking spaces per train station: {parkingSpacesPerStation:.2f}")
            
            if (busStops > 0 and stations > 0):
                weightedRatio = parkingSpaces / (stations * 20 + busStops)
                print(f"Parking spaces divided by (train stations x 20 + bus stops): {weightedRatio:.2f}")
        
        print("\n")