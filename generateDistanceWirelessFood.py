from math import sqrt, pow
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

            count = 0
            dataToWrite = []
            maxInvDistanceWireless = 0
            maxInvDistanceFood = 0
            # Write to CSV
            if featureFilename:
                with open(featureFilename, 'wb') as f:
                    writerFeature = csv.writer(f)

                    # Read more CSV
                    for row in spamreader:
                        for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                            if attr_names[i] == 'Y':
                                lat = float(attr)
                            if attr_names[i] == 'X':
                                lon = float(attr)

                        count += 1
                        if count % 1000 == 0:
                            print count

                        d = [lat, lon]
                        distanceWireless = min(map(lambda x: sqrt(pow(d[0]-x[0], 2)+pow(d[1]-x[1], 2)), data_wireless))
                        distanceFood = min(map(lambda x: sqrt(pow(d[0]-x[0], 2)+pow(d[1]-x[1], 2)), data_food))
                        maxInvDistanceWireless = max(maxInvDistanceWireless, 1/distanceWireless)
                        maxInvDistanceFood = max(maxInvDistanceFood, 1/distanceFood)
                        dataToWrite.append([distanceWireless, distanceFood])

                    for row in dataToWrite:
                        distanceWireless = row[0]
                        distanceFood = row[1]
                        writerFeature.writerow([distanceWireless, distanceFood, 1/distanceWireless/maxInvDistanceWireless, 1/distanceFood/maxInvDistanceFood])


def main():
    print "prepareData"
    prepareData('Recreation/Wireless_Service_Facility_Permits.csv','Recreation/Mobile_Food_Facility_Permit.csv')
    print "generateFeature train"
    generateFeature('train.csv', 'trainDistanceWirelessFood.csv')
    print "generateFeature test"
    generateFeature('test.csv', 'testFeatureWirelessFood.csv')

if __name__ == "__main__":
    # execute only if run as a script
    main()