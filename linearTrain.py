from sklearn import svm
from numpy import genfromtxt
from numpy import savetxt
from numpy import insert
from numpy import asarray

def main():

  trainFeature = genfromtxt('trainFeature.csv', delimiter=',')[0::5]
  trainLabel = genfromtxt('trainLabel.csv', delimiter='\n')[0::5]
  testFeature = genfromtxt('testFeature.csv', delimiter=',')   

  #trainFeature = genfromtxt('mytrain.csv', delimiter=',')
  #trainLabel = genfromtxt('mylabel.csv', delimiter='\n')
  #testFeature = genfromtxt('mytest.csv', delimiter=',')   

  lin_clf = svm.LinearSVC()
  lin_clf.fit(trainFeature, trainLabel)
  dec = lin_clf.decision_function(testFeature)
  
  header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

  #dec = [[(i + 1.0) / 2.0 for i in j] for j in dec]
  #mm = dec.min()
  #dec = asarray([[(i - mm) for i in j] for j in dec])

  dec = asarray([[(i - min(j)) for i in j] for j in dec])

  fmt=['%d'] + ['%1.3f'] * dec.shape[1]

  ind = [i for i in xrange(0,len(dec))]
  dec = insert(dec, 0, ind, axis=1)

  savetxt("predict.csv", dec, delimiter=",", header=header, fmt=fmt, comments="")


if __name__ == "__main__":
  # execute only if run as a script
  main()
