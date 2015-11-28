import shapefile
from geopy.distance import vincenty
from toGPS import addressToGPS
import csv

def calculateMinDistanceFromRecreation(data):
    with open('Recreation/Recreation___Park_Department_Park_Info_Dataset.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        raw_data = dict()
        attr_names = spamreader.next() #['Date, 'Category', ...]
        for attr in attr_names:
            raw_data[attr] = [] # raw_data['Date'] = []
                                # raw_data['Category'] = []

        for row in spamreader:
            for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                raw_data[attr_names[i]].append(attr)

        data_recreation = []
        for location in raw_data['Location 1']:
            if len(location) >0 :
                index_begin = location.index("(3")
                index_coma = location.index(",",index_begin)
                index_end = location.index(")")
                lat = float(location[index_begin+1:index_coma])
                lon = float(location[index_coma+2:index_end])
                data_recreation.append((lat,lon))
        distances = []
        for d in data:
            distances.append(min(map(lambda x : vincenty(d, x).miles, data_recreation)))
        return distances

def test_calculateMinDistanceFromPdDistricts():
    test_data = [(37.7986593, -122.4099628), (37.7754356, -122.403939), (37.7297506, -122.3979034), (37.762849, -122.422005), (37.78019, -122.4324452), (37.767797, -122.455287), (37.7799276, -122.4644668), (37.7246756, -122.4462154), (37.7438321, -122.4811658), (37.783665, -122.412904), (38, -122)]
    distances = calculateMinDistanceFromRecreation(test_data)
    print distances

if __name__ == "__main__":
    test_calculateMinDistanceFromPdDistricts()