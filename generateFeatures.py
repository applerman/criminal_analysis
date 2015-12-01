# Some reference:
# https://www.kaggle.com/smerity/sf-crime/fighting-crime-with-keras/code
# https://www.kaggle.com/petercooman/sf-crime/odds-based-on-pddistrict

import csv

days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
districts = ['BAYVIEW', 'CENTRAL', 'INGLESIDE', 'MISSION', 'NORTHERN', 'PARK', 'RICHMOND', 'SOUTHERN', 'TARAVAL', 'TENDERLOIN']
labels = 'ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS'.split(',')
daysDict = {}
districtsDict = {}
labelsDict = {}
statMatrix = [[0.0 for x in range(len(labels))] for x in range(len(districts))]


def generateFeatureLabel(inputFilename, featureFilename, lableFilename):
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

                        # Read more CSV
                        for row in spamreader:
                            currFeature = [0.0 for i in range(17)] # 7 dim binary for DayOfWeek + 10 dim binary for PdDistrict
                            for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "

                                if attr_names[i] == 'Category':
                                    writerLable.writerow([labelsDict[attr]])

                                if attr_names[i] == 'DayOfWeek':
                                    indexDay = daysDict[attr]
                                    currFeature[indexDay] = 1.0

                                if attr_names[i] == 'PdDistrict':
                                    indexPd = districtsDict[attr]
                                    currFeature[7 + indexPd] = 1.0

                            writerFeature.writerow(currFeature + statMatrix[indexPd]) # + 39 dim continuous PdDistrictStats


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
                        currFeature = [0.0 for i in range(17)] # 7 dim binary for DayOfWeek + 10 dim binary for PdDistrict
                        for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "

                            if attr_names[i] == 'DayOfWeek':
                                indexDay = daysDict[attr]
                                currFeature[indexDay] = 1.0

                            if attr_names[i] == 'PdDistrict':
                                indexPd = districtsDict[attr]
                                currFeature[7 + indexPd] = 1.0

                        writerFeature.writerow(currFeature + statMatrix[indexPd]) # + 39 dim continuous PdDistrictStats


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

    generateFeatureLabel('train.csv', 'trainFeature.csv', 'trainLabel.csv')
    generateFeature('test.csv', 'testFeature.csv')

if __name__ == "__main__":
    # execute only if run as a script
    main()
