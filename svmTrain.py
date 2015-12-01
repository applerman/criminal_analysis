from sklearn import svm
from numpy import genfromtxt
from numpy import savetxt
from numpy import insert

def main():

  trainFeature = genfromtxt('trainFeature.csv', delimiter=',')   
  trainLabel = genfromtxt('trainLabel.csv', delimiter='\n')   
  testFeature = genfromtxt('testFeature.csv', delimiter=',')   

  clf = svm.SVC(decision_function_shape='ovr')
  clf.fit(trainFeature, trainLabel)
  dec = clf.decision_function(testFeature)
  
  header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

  fmt=['%d'] + ['%1.3f'] * dec.shape[1]

  ind = [i for i in xrange(1,len(dec)+1)]
  dec = insert(dec, 0, ind, axis=1)

  savetxt("predict.csv", dec, delimiter=",", header=header, fmt=fmt, comments="")


if __name__ == "__main__":
  # execute only if run as a script
  main()
