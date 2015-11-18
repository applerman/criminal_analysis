import csv
import numpy

i = 0
with open('train.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if i < 2:
            for field in row:
                print field
        i = i + 1
