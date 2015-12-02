# install package elm
# pip install elm

import elm
import numpy as np

def main():

  trainFeature = np.genfromtxt('trainFeature.csv', delimiter=',')[0::5]
  trainLabel = np.genfromtxt('trainLabel.csv', delimiter='\n')[0::5]
  testFeature = np.genfromtxt('testFeature.csv', delimiter=',')

  #trainFeature = np.genfromtxt('mytrain.csv', delimiter=',')
  #trainLabel = np.genfromtxt('mylabel.csv', delimiter='\n')
  #testFeature = np.genfromtxt('mytest.csv', delimiter=',')   
  testLabel = np.asarray([0]*testFeature.shape[0])

  train = np.concatenate((np.asarray([trainLabel]).T, trainFeature), axis=1)
  test = np.concatenate((np.asarray([testLabel]).T, testFeature), axis=1)
 
  elmk = elm.ELMKernel()
  elmk.search_param(train, cv="kfold", of="accuracy", eval=10)

  tr_result = elmk.train(train)
  te_result = elmk.test(test)

  predicted = te_result.predicted_targets
  predicted_class = np.round(predicted).astype(int)

  dec = [[0] * 39 for i in xrange(testFeature.shape[0])]
  for i in xrange(testFeature.shape[0]):
    dec[i][predicted_class[i]] = 1
 
  header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

  #dec = np.asarray([[(i - min(j)) / (max(j) - min(j)) for i in j] for j in dec])
  dec = np.asarray(dec)
  fmt=['%d'] + ['%1.3f'] * dec.shape[1]
  dec = np.insert(dec, 0, range(len(dec)), axis=1)
  np.savetxt("predict.csv", dec, delimiter=",", header=header, fmt=fmt, comments="")


if __name__ == "__main__":
  # execute only if run as a script
  main()
