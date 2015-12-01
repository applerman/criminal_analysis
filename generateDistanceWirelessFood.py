from geopy.distance import vincenty
import csv

data_wireless = []
data_food = []


def prepareData(wirelessFilename, foodFilename):
    with open(wirelessFilename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        raw_data = dict()
        attr_names = spamreader.next() #['Date, 'Category', ...]
        for attr in attr_names:
            raw_data[attr] = [] # raw_data['Date'] = []
                                # raw_data['Category'] = []

        for row in spamreader:
            for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                raw_data[attr_names[i]].append(attr)

        for location in raw_data['Location1']:
            if len(location) > 0:
                index_begin = location.index("(3")
                index_coma = location.index(",",index_begin)
                index_end = location.index(")")
                lat = float(location[index_begin+1:index_coma])
                lon = float(location[index_coma+2:index_end])
                data_wireless.append((lat, lon))

    with open(foodFilename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        raw_data = dict()
        attr_names = spamreader.next() #['Date, 'Category', ...]
        for attr in attr_names:
            raw_data[attr] = [] # raw_data['Date'] = []
                                # raw_data['Category'] = []

        for row in spamreader:
            for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                raw_data[attr_names[i]].append(attr)

        for location in raw_data['Location']:
            if len(location) > 0:
                index_begin = location.index("(3")
                index_coma = location.index(",",index_begin)
                index_end = location.index(")")
                lat = float(location[index_begin+1:index_coma])
                lon = float(location[index_coma+2:index_end])
                data_food.append((lat, lon))


def generateFeature(inputFilename, featureFilename):
    with open(inputFilename, 'rb') as csvfile:
            # Read CSV
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            raw_data = dict()
            attr_names = spamreader.next()  #['Date, 'Category', ...]
            for attr in attr_names:
                raw_data[attr] = []  # raw_data['Date'] = []
                                     # raw_data['Category'] = []

            # Write to CSV
            if featureFilename:
                with open(featureFilename, 'wb') as f:
                    writerFeature = csv.writer(f)

                    # Read more CSV
                    for row in spamreader:
                        for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                            if attr_names[i] == 'Y':
                                lat = attr
                            if attr_names[i] == 'X':
                                lon = attr

                        d = [lat, lon]
                        distanceWireless = min(map(lambda x: vincenty(d, x).miles, data_wireless))
                        distanceFood = min(map(lambda x: vincenty(d, x).miles, data_food))
                        writerFeature.writerow([distanceWireless,distanceFood,1/distanceWireless,1/distanceFood])


def main():
    prepareData('Recreation/Wireless_Service_Facility_Permits.csv','Recreation/Mobile_Food_Facility_Permit.csv')
    generateFeature('train.csv', 'trainDistanceWirelessFood.csv')
    generateFeature('test.csv', 'testFeatureWirelessFood.csv')

if __name__ == "__main__":
    # execute only if run as a script
    main()