from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt
from numpy import savetxt
from numpy import insert
from sklearn.neighbors import KNeighborsClassifier
import time

def main():


  # trainFeature = genfromtxt('trainF2.csv', delimiter=',')
  # trainLabel = genfromtxt('trainLabel100.csv', delimiter='\n')
  # testFeature = genfromtxt('test2Feature.csv', delimiter=',')
  trainFeature = genfromtxt('trainFeature.csv', delimiter=',')[0::5]
  trainLabel = genfromtxt('trainLabel.csv', delimiter='\n')[0::5]
  testFeature = genfromtxt('testFeature.csv', delimiter=',')

  time_start = time.clock()
  clf = KNeighborsClassifier(n_jobs=2)
  clf.fit(trainFeature, trainLabel)

  time_elapsed = (time.clock() - time_start)
  print "build model time = "+str(time_elapsed)
  time_start = time.clock()

  dec = clf.predict_proba(testFeature)

  time_elapsed = (time.clock() - time_start)
  print "predict time = "+str(time_elapsed)

  header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

  print dec.shape[1]
  fmt=['%d'] + ['%1.4f'] * dec.shape[1]

  ind = [i for i in xrange(0,len(dec))]
  dec = insert(dec, 0, ind, axis=1)

  savetxt("predict_KNN.csv", dec, delimiter=",", header=header, fmt=fmt, comments="")
  #

if __name__ == "__main__":
  # execute only if run as a script
  main()

