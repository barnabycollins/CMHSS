from OSMPythonTools.api import Api

OSM = Api()

way = OSM.query('way/5887599')

print(way.tags())