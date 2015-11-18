import csv
import numpy

i = 0

with open('train.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    raw_data = dict()
    attr_names = spamreader.next() #['Date, 'Category', ...]
    for attr in attr_names:
        raw_data[attr] = [] # raw_data['Date'] = []
                            # raw_data['Category'] = []

    for row in spamreader:
        for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
            raw_data[attr_names[i]].append(attr)
            

    # Dates -> split into year, month, date, hour (24hr), minute, second (may be all 0)

    # Category -> label them from 0-38

    # Descript -> ???

    # DayOfWeek -> Convert to 7 binary features (Monday, …, Sunday)

    # PdDistrict -> Convert to # binary features

    # Resolution -> ???

    # Address -> ???

    # X -> will use raw data, as well as features incorporated from SF OpenData

    # Y -> same as above
            
