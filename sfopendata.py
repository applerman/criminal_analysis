import shapefile
from geopy.distance import vincenty

from toGPS import addressToGPS

def calculateMinDistanceFromPdDistricts(data):
    sf = shapefile.Reader("sfpd_stations/sfpd_stations")
    pd_locations = map(lambda x: addressToGPS(x[2] + "San Francisco, CA"), sf.records())
    distances = []
    for d in data:
        distances.append(min(map(lambda x : vincenty(d, x).miles, pd_locations)))

    return distances

def test_calculateMinDistanceFromPdDistricts():
    test_data = [(37.7986593, -122.4099628), (37.7754356, -122.403939), (37.7297506, -122.3979034), (37.762849, -122.422005), (37.78019, -122.4324452), (37.767797, -122.455287), (37.7799276, -122.4644668), (37.7246756, -122.4462154), (37.7438321, -122.4811658), (37.783665, -122.412904), (38, -122)]
    distances = calculateMinDistanceFromPdDistricts(test_data)

    print distances

if __name__ == "__main__":
    test_calculateMinDistanceFromPdDistricts()
