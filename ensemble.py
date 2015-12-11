import csv
import sys
from numpy import savetxt
from numpy import genfromtxt
from numpy import insert
from numpy import asarray

header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

def ensembleBySum(outputFilename, inputFiles):
    readers = []
    for inputFile in inputFiles:
        readers.append(csv.reader(open(inputFile, 'rb'), delimiter=','))
        readers[-1].next()

    dec = []
    for ii, reader in enumerate(readers):
        for i, row in enumerate(reader):
            values = map(lambda x: float(x), row[1:])
            values = map(lambda x: x/sum(values), values)
            if ii == 0:
                dec.append(values)
            else:
                dec[i] = [sum(x) for x in zip(dec[i], values)]

    fmt=['%d'] + ['%1.4f'] * len(dec[0])
    dec = asarray([[(i - min(j)) / (max(j) - min(j)) for i in j] for j in dec])
    dec = insert(dec, 0, range(len(dec)), axis=1)
    savetxt(outputFilename, dec, delimiter=",", header=header, fmt=fmt, comments="")
        
def main():
    inputFiles = sys.argv[1:]
    ensembleBySum("predict_ensemble.csv", inputFiles)

if __name__ == "__main__":
    main() 
