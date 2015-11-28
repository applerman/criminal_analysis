# Some reference:
# https://www.kaggle.com/smerity/sf-crime/fighting-crime-with-keras/code
# https://www.kaggle.com/petercooman/sf-crime/odds-based-on-pddistrict

import csv

def generatePdDistrictStats(infile, outfile):
    with open(infile, 'rb') as csvfile:

        # Read CSV
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        raw_data = dict()
        attr_names = spamreader.next() #['Date, 'Category', ...]
        for attr in attr_names:
            raw_data[attr] = [] # raw_data['Date'] = []
                                # raw_data['Category'] = []

        # Build Dict of name to index
        districts = ['BAYVIEW', 'CENTRAL', 'INGLESIDE', 'MISSION', 'NORTHERN', 'PARK', 'RICHMOND', 'SOUTHERN', 'TARAVAL', 'TENDERLOIN']
        labels = 'ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS'.split(',')
        districtsDict = {}
        labelsDict = {}
        for (i, attr) in enumerate(districts):
            districtsDict[attr] = i;
        for (i, attr) in enumerate(labels):
            labelsDict[attr] = i;

        # Declare arrays
        statMatrix = [[0.0 for x in range(len(labels))] for x in range(len(districts))] # Each row is the statistics for the district
        districtsCount = [0.0 for x in range(len(districts))] # Count the appearance of that district

        # Read more CSV, Count occurrence
        for row in spamreader:
            for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                raw_data[attr_names[i]].append(attr)

                if attr_names[i] == 'Category':
                    indexCate = labelsDict[attr]
                if attr_names[i] == 'PdDistrict':
                    indexPd = districtsDict[attr]
                    districtsCount[indexPd] += 1
                    statMatrix[indexPd][indexCate] += 1

        # Average
        for i in range(len(districts)):
            for j in range(len(labels)):
                statMatrix[i][j] /= districtsCount[i]

        # Write to CSV
        if outfile:
            with open(outfile, 'wb') as f:
                writer = csv.writer(f)
                for i in range(len(statMatrix)):
                    writer.writerow(statMatrix[i])

def predictTestWithPdDistrictStats(testFilename, PdDistrictStatsFilename, predictFilename):

    # Build Dict of name to index
    districts = ['BAYVIEW', 'CENTRAL', 'INGLESIDE', 'MISSION', 'NORTHERN', 'PARK', 'RICHMOND', 'SOUTHERN', 'TARAVAL', 'TENDERLOIN']
    labels = 'ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS'.split(',')
    districtsDict = {}
    labelsDict = {}
    for (i, attr) in enumerate(districts):
        districtsDict[attr] = i;
    for (i, attr) in enumerate(labels):
        labelsDict[attr] = i;

    # Declare arrays
    statMatrix = [[0.0 for x in range(len(labels))] for x in range(len(districts))]

    # Read PdDistrictStatsFilename and create the lookup table
    with open(PdDistrictStatsFilename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for (i,row) in enumerate(spamreader):
            for (j, attr) in enumerate(row):
                statMatrix[i][j] = int((float(attr) * 100) + 0.5) / 100.0

    with open(testFilename, 'rb') as csvfile:
        # Read CSV
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        raw_data = dict()
        attr_names = spamreader.next() #['Date, 'Category', ...]
        for attr in attr_names:
            raw_data[attr] = [] # raw_data['Date'] = []
                                # raw_data['Category'] = []

        # Write to CSV
        if predictFilename:
            with open(predictFilename, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(['Id'] + labels)

                # Read more CSV, Write predicts to predict file
                for row in spamreader:
                    for (i, attr) in enumerate(row): #"2011-01-12 17:05:00", "
                        raw_data[attr_names[i]].append(attr)

                        if attr_names[i] == 'Id':
                            currId = attr
                        if attr_names[i] == 'PdDistrict':
                            indexPd = districtsDict[attr]
                            writer.writerow([currId] + statMatrix[indexPd])

def main():
    generatePdDistrictStats('train.csv', 'PdDistrictStats.csv')
    predictTestWithPdDistrictStats('test.csv', 'PdDistrictStats.csv', 'predict.csv')

if __name__ == "__main__":
    main()
