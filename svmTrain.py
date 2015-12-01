from sklearn import svm
from numpy import genfromtxt
from numpy import savetxt
from numpy import insert
from numpy import asarray

def main():

  trainFeature = genfromtxt('trainFeature.csv', delimiter=',')[0::5]
  trainLabel = genfromtxt('trainLabel.csv', delimiter='\n')[0::5]
  testFeature = genfromtxt('testFeature.csv', delimiter=',')   

  clf = svm.SVC(decision_function_shape='ovr')
  clf.fit(trainFeature, trainLabel)
  dec = clf.decision_function(testFeature)
  
  header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

  dec = asarray([[(i - min(j)) / (max(j) - min(j)) for i in j] for j in dec])
  fmt=['%d'] + ['%1.3f'] * dec.shape[1]
  dec = insert(dec, 0, range(len(dec)), axis=1)
  savetxt("predict.csv", dec, delimiter=",", header=header, fmt=fmt, comments="")


if __name__ == "__main__":
  # execute only if run as a script
  main()
