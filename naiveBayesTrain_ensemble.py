from numpy import genfromtxt
from numpy import savetxt
from numpy import insert
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from numpy import genfromtxt
from numpy import savetxt
from numpy import insert
import time
import numpy as np

def main():

  # 3/5 train
  trainFeature1 = genfromtxt('trainFeatureWithCounting.csv', delimiter=',')[0::5]
  trainLabel1 = genfromtxt('trainLabel.csv', delimiter='\n')[0::5]
  trainFeature2 = genfromtxt('trainFeatureWithCounting.csv', delimiter=',')[2::5]
  trainLabel2 = genfromtxt('trainLabel.csv', delimiter='\n')[2::5]
  trainFeature3 = genfromtxt('trainFeatureWithCounting.csv', delimiter=',')[4::5]
  trainLabel3 = genfromtxt('trainLabel.csv', delimiter='\n')[4::5]
  trainFeature = np.concatenate((trainFeature1, trainFeature2,trainFeature3))
  trainLabel = np.concatenate((trainLabel1, trainLabel2,trainLabel3))

  # 2/5 in trainset to test
  trainFeature_test1 = genfromtxt('trainFeatureWithCounting.csv', delimiter=',')[1::5]
  trainLabel_test1 = genfromtxt('trainLabel.csv', delimiter='\n')[1::5]
  trainFeature_test2 = genfromtxt('trainFeatureWithCounting.csv', delimiter=',')[3::5]
  trainLabel_test2 = genfromtxt('trainLabel.csv', delimiter='\n')[3::5]
  trainFeature_test = np.concatenate((trainFeature_test1, trainFeature_test2))
  trainLabel_test = np.concatenate((trainLabel_test1, trainLabel_test2))

  #testset
  testFeature = genfromtxt('testFeatureWithCounting.csv', delimiter=',')


  clf = MultinomialNB()
  clf.fit(trainFeature, trainLabel)
  MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
  header = "Id,ARSON,ASSAULT,BAD CHECKS,BRIBERY,BURGLARY,DISORDERLY CONDUCT,DRIVING UNDER THE INFLUENCE,DRUG/NARCOTIC,DRUNKENNESS,EMBEZZLEMENT,EXTORTION,FAMILY OFFENSES,FORGERY/COUNTERFEITING,FRAUD,GAMBLING,KIDNAPPING,LARCENY/THEFT,LIQUOR LAWS,LOITERING,MISSING PERSON,NON-CRIMINAL,OTHER OFFENSES,PORNOGRAPHY/OBSCENE MAT,PROSTITUTION,RECOVERED VEHICLE,ROBBERY,RUNAWAY,SECONDARY CODES,SEX OFFENSES FORCIBLE,SEX OFFENSES NON FORCIBLE,STOLEN PROPERTY,SUICIDE,SUSPICIOUS OCC,TREA,TRESPASS,VANDALISM,VEHICLE THEFT,WARRANTS,WEAPON LAWS"

  #testset
  dec1 = clf.predict_proba(testFeature)
  #trainset to test
  dec2 = clf.predict_proba(trainFeature_test)


  fmt1=['%d'] + ['%1.4f'] * dec1.shape[1]
  fmt2=['%d'] + ['%1.4f'] * dec2.shape[1]

  # normalized to [0,1] by Henry
  # dec = asarray([[(i - min(j)) / (max(j) - min(j)) for i in j] for j in dec])

  #ind = [i for i in xrange(1,len(dec)+1)] by Henry
  dec1 = insert(dec1, 0, range(len(dec1)), axis=1)
  savetxt("predict_NaiveBayes_96_testset.csv", dec1, delimiter=",", header=header, fmt=fmt1, comments="")

  dec2 = insert(dec2, 0, range(len(dec2)), axis=1)
  savetxt("predict_NaiveBayes_96_trainset_to_test.csv", dec2, delimiter=",", header=header, fmt=fmt2, comments="")

if __name__ == "__main__":
  # execute only if run as a script
  main()
