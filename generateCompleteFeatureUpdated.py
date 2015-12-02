# Some reference:
# https://www.kaggle.com/smerity/sf-crime/fighting-crime-with-keras/code
# https://www.kaggle.com/petercooman/sf-crime/odds-based-on-pddistrict
# https://www.kaggle.com/c/sf-crime/forums/t/15836/predicting-crime-categories-with-address-featurization-and-neural-nets

import csv
from datetime import datetime

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
districts = ['BAYVIEW', 'CENTRAL', 'INGLESIDE', 'MISSION', 'NORTHERN', 'PARK', 'RICHMOND', 'SOUTHERN', 'TARAVAL', 'TENDERLOIN']
labels = 'ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS'.split(',')
daysDict = {}
districtsDict = {}
labelsDict = {}
statMatrix = [[0.0 for x in range(len(labels))] for x in range(len(districts))]

def getTimeFeatures(attr):
    currTime = datetime.strptime(attr, "%Y-%m-%d %H:%M:%S")
    year = currTime.year / 2015.0
    month = currTime.month / 12.0
    day = currTime.day / 31.0
    time = currTime.hour / 24.0

    winter = 0
    spring = 0
    summer = 0
    fall = 0
    if month in [11, 0, 1]:
        winter = 1
    if month in [2, 3, 4]:
        spring = 1
    if month in [5, 6, 7]:
        summer = 1
    if month in [8, 9, 10]:
        fall = 1

    awake = 0
    if 9 <= time <= 23:
        awake = 1

    return [year, month, day, time, winter, spring, summer, fall, awake]

def generateFeatureLabel(inputFilename, featureFilename, lableFilename, countingFilename):
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
                if lableFilename:
                    with open(lableFilename, 'wb') as f2:
                        writerFeature = csv.writer(f)
                        writerLable = csv.writer(f2)

                        if countingFilename:
                            with open(countingFilename, 'rb') as countingFile:
                                countingReader = csv.reader(countingFile, delimiter=',', quotechar='"')

                                # Read more CSV
                                for row in spamreader:
                                    currFeature = [0.0 for i in range(19)] # 7 dim binary for DayOfWeek + 10 dim binary for PdDistrict + 2 dim XY
                                    countingFeature = countingReader.next()
                                    for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "

                                        if attr_names[i] == 'Category':
                                            writerLable.writerow([labelsDict[attr]])

                                        if attr_names[i] == 'DayOfWeek':
                                            indexDay = daysDict[attr]
                                            currFeature[indexDay] = 1.0

                                        if attr_names[i] == 'PdDistrict':
                                            indexPd = districtsDict[attr]
                                            currFeature[7 + indexPd] = 1.0

                                        if attr_names[i] == 'X':
                                            currFeature[17] = float(attr) / 123.0

                                        if attr_names[i] == 'Y':
                                            currFeature[18] = float(attr) / 38.0

                                        if attr_names[i] == 'Dates':
                                            timeFeatures = getTimeFeatures(attr)

                                    writerFeature.writerow(currFeature + timeFeatures + statMatrix[indexPd] + countingFeature) # + 4 dim year, month, date, hour + 4 dim seasons + 1 dim awake + 39 dim continuous PdDistrictStats + 40 dim counting features


def generateFeature(inputFilename, featureFilename, countingFilename):
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

                    if countingFilename:
                            with open(countingFilename, 'rb') as countignFile:
                                countingReader = csv.reader(countignFile, delimiter=',', quotechar='"')

                                # Read more CSV
                                for row in spamreader:
                                    currFeature = [0.0 for i in range(19)] # 7 dim binary for DayOfWeek + 10 dim binary for PdDistrict + 2 dim XY
                                    countingFeature = countingReader.next()

                                    for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "

                                        if attr_names[i] == 'DayOfWeek':
                                            indexDay = daysDict[attr]
                                            currFeature[indexDay] = 1.0

                                        if attr_names[i] == 'PdDistrict':
                                            indexPd = districtsDict[attr]
                                            currFeature[7 + indexPd] = 1.0

                                        if attr_names[i] == 'X':
                                            currFeature[17] = float(attr) / 123.0

                                        if attr_names[i] == 'Y':
                                            currFeature[18] = float(attr) / 38.0

                                        if attr_names[i] == 'Dates':
                                            timeFeatures = getTimeFeatures(attr)

                                    writerFeature.writerow(currFeature + timeFeatures + statMatrix[indexPd] + countingFeature) # + 4 dim year, month, date, hour + 4 dim seasons + 1 dim awake + 39 dim continuous PdDistrictStats + 40 dim counting features


def main():
    for (i, attr) in enumerate(days):
        daysDict[attr] = i
    for (i, attr) in enumerate(districts):
        districtsDict[attr] = i
    for (i, attr) in enumerate(labels):
        labelsDict[attr] = i

    with open('PdDistrictStats.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for (i,row) in enumerate(spamreader):
            for (j, attr) in enumerate(row):
                statMatrix[i][j] = int((float(attr) * 10000) + 0.5) / 10000.0

    generateFeatureLabel('train.csv', 'trainFeatureComplete.csv', 'trainLabel4.csv', 'trainFeatureAddr.csv')
    generateFeature('test.csv', 'testFeatureComplete.csv', 'testFeatureAddr.csv')

if __name__ == "__main__":
    # execute only if run as a script
    main()

