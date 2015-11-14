import random
import collections
import math
import sys
import csv
import bisect
from collections import Counter
import time
from sklearn import svm

def process(filename):
	ingredientSet = set()
	cuisineMap = {}
	X = []
	Y = []
	countCuisine = 0
	with open(filename, 'rb') as dataset:
		datareader = csv.reader(dataset)
		tempX = []
		for row in datareader:
			cuisine = row[0]
			if cuisine not in cuisineMap:
				cuisineMap[cuisine] = countCuisine
				countCuisine = countCuisine + 1
			ingredients = collections.Counter(row[1:])
			ingredientSet.update(ingredients)
			tempX.append((ingredients, cuisineMap.get(cuisine)))
		for ingredients, cuisine in tempX:
			featureVector = [0] * len(ingredientSet)
			for index, ingredient in enumerate(ingredientSet):
				if ingredient in ingredients:
					featureVector[index] = 1
				else:
					featureVector[index] = 0
			X.append(featureVector)
			Y.append(cuisine)
	return X, Y, ingredientSet, cuisineMap


file1 = "data.csv"
X, Y, _, _ = process(file1)
print 1
nExamples = len(Y)
shuffleIdx = range(nExamples)
random.shuffle(shuffleIdx)
X = [X[i] for i in shuffleIdx]
Y = [Y[i] for i in shuffleIdx]
nTrain = 7*nExamples/10
XTrain = X[:nTrain]
YTrain = Y[:nTrain]
XTest = X[nTrain:]
YTest = Y[nTrain:]
print 2
clf = svm.SVC(kernel='poly', tol=0.1, verbose=True)
clf.fit(XTrain, YTrain)
print 3
YPred = clf.predict(XTest)
print 4
correct = 0
for i in xrange(len(YPred)):
    if YPred[i] != YTest[i]:
        correct+=1
        print correct, i
predSet = set(YPred)
classSet = set(YTrain)
print len(predSet), predSet
print len(classSet), classSet
print "Fraction of correct classifications:", str(correct*1.0/len(YPred))
