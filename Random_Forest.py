from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from numpy import genfromtxt
from numpy import savetxt
from numpy import insert

def main():

  trainFeature = genfromtxt('trainFeature.csv', delimiter=',')
  trainLabel = genfromtxt('trainLabel_multi.csv', delimiter=',')
  testFeature = genfromtxt('testFeature.csv', delimiter=',')
  # trainFeature = genfromtxt('trainFeature1000.csv', delimiter=',')
  # trainLabel = genfromtxt('trainLabel1000_multi.csv', delimiter=',')
  # testFeature = genfromtxt('test2Feature.csv', delimiter=',')
  clf =OneVsRestClassifier(RandomForestClassifier(n_jobs=2))
  clf.fit(trainFeature, trainLabel)
  dec = clf.predict_proba(testFeature)

  header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

  fmt=['%d'] + ['%1.4f'] * dec.shape[1]

  # normalized to [0,1] by Henry
  dec = asarray([[(i - min(j)) / (max(j) - min(j)) for i in j] for j in dec])

  ind = [i for i in xrange(0,len(dec))]
  dec = insert(dec, 0, ind, axis=1)

  savetxt("predict_Random_Forest.csv", dec, delimiter=",", header=header, fmt=fmt, comments="")



if __name__ == "__main__":
  # execute only if run as a script
  main()

