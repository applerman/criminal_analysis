# Some reference:
# https://msdn.microsoft.com/en-us/library/azure/dn913056.aspx
# https://www.kaggle.com/c/sf-crime/forums/t/15836/predicting-crime-categories-with-address-featurization-and-neural-nets

import csv
import pandas
from copy import deepcopy

# Build Dict of name to index
labels = 'ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS'.split(',')
labelsDict = {}
for (i, attr) in enumerate(labels):
    labelsDict[attr] = i

defaultFeature = [0.0 for x in range(len(labels))]
addrWeight = {}
addrFeature = {}
oldAddress = []
oldCountsAddress = {}
oldAddressSize = 0.0

def generateCountingFeatureAddr(inputFilename):

    trainData = pandas.read_csv(inputFilename)

    global oldAddressSize
    oldAddressSize = deepcopy(float(len(trainData)))

    addresses = sorted(trainData["Address"].unique())
    categories = sorted(trainData["Category"].unique())

    global oldAddress
    oldAddress = deepcopy(addresses)

    countsCategory = trainData.groupby(["Category"]).size()
    countsAddress = trainData.groupby(["Address"]).size()
    countsAddressCategory = trainData.groupby(["Address", "Category"]).size()

    global oldCountsAddress
    oldCountsAddress = deepcopy(countsAddress)

    for cat in categories:
        index = labelsDict[cat]
        defaultFeature[index] = float(countsCategory[cat])/float(len(trainData))

    for addr in addresses:
        currFeature = deepcopy(defaultFeature)
        weight = float(countsAddress[addr])/float(len(trainData))
        addrWeight[addr] = deepcopy(weight)

        for cate in countsAddressCategory[addr].keys():
            index = labelsDict[cate]
            if (countsAddress[addr] > countsAddressCategory[addr][cate]) and (countsAddressCategory[addr][cate] > 2): # Prevent Corner Case
                prob = float(countsAddressCategory[addr][cate])/float(countsAddress[addr])
                currFeature[index] = prob

        addrFeature[addr] = deepcopy(currFeature)


def generateFeatureFileForTrain(trainFilename, featureFilename):
    with open(trainFilename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        attr_names = spamreader.next()

        if featureFilename:
            with open(featureFilename, 'wb') as f:
                writer = csv.writer(f)

                for row in spamreader:
                    for (index, attribute) in enumerate(row):
                        if attr_names[index] == 'Address':
                            writer.writerow(addrFeature[attribute] + [addrWeight[attribute]])


def predictTestWithCountingFeatureAddr(testFilename, predictFilename):

    testData = pandas.read_csv(testFilename)

    newAddresses = sorted(testData["Address"].unique())
    newCountsAddress = testData.groupby("Address").size()

    addressOnlyInTest = set(newAddresses + oldAddress) - set(oldAddress)
    addressInBoth = set(newAddresses).intersection(oldAddress)

    for addr in addressOnlyInTest:
        weight = float(newCountsAddress[addr]) / float(oldAddressSize + len(testData))
        addrWeight[addr] = deepcopy(weight)

    for addr in addressInBoth:
        weight = float(oldCountsAddress[addr] + newCountsAddress[addr]) / float(oldAddressSize + len(testData))
        addrWeight[addr] = deepcopy(weight)

    with open(testFilename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        attr_names = spamreader.next()

        if predictFilename:
            with open(predictFilename, 'wb') as f:
                writer = csv.writer(f)
                writer.writerow(['Id'] + labels)

                for row in spamreader:
                    for (index, attribute) in enumerate(row):

                        if attr_names[index] == 'Id':
                                currId = attribute

                        if attr_names[index] == 'Address':
                            if attribute in addrFeature:
                                featureToWrite = deepcopy(addrFeature[attribute])
                                featureToWrite[:] = [int((float(x) * 10000) + 0.5) / 10000.0 for x in featureToWrite]
                                writer.writerow([currId] + featureToWrite)
                            else:
                                addrFeature[attribute] = deepcopy(defaultFeature)
                                featureToWrite = deepcopy(addrFeature[attribute])
                                featureToWrite[:] = [int((float(x) * 10000) + 0.5) / 10000.0 for x in featureToWrite]
                                writer.writerow([currId] + featureToWrite)


def generateFeatureFileForTest(testFilename, featureFilename):
    with open(testFilename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        attr_names = spamreader.next()

        if featureFilename:
            with open(featureFilename, 'wb') as f:
                writer = csv.writer(f)

                for row in spamreader:
                    for (index, attribute) in enumerate(row):
                        if attr_names[index] == 'Address':
                            writer.writerow(addrFeature[attribute] + [addrWeight[attribute]])


def main():

    trainFilename = 'train.csv'
    testFilename = 'test.csv'

    print "generateCountingFeatureAddr"
    generateCountingFeatureAddr(trainFilename)

    print "generateFeatureFileForTrain"
    generateFeatureFileForTrain(trainFilename, 'trainFeatureAddr.csv')

    print "predictTestWithCountingFeatureAddr"
    predictTestWithCountingFeatureAddr(testFilename, 'predictCountingFeatureAddr.csv')

    print "generateFeatureFileForTest"
    generateFeatureFileForTest(testFilename, 'testFeatureAddr.csv')

if __name__ == "__main__":
    main()
