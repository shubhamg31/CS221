#!/usr/bin/python

import sklearn
import mlpy
import numpy as np
import scipy as sp
import csv
import string
from collections import * 
import processDataSet
import random
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier

# cuisine = Counter()
# ingredients = Counter()
# with open('../project/data/recipe_data.csv', 'rb') as csvfile:
# 	datareader = csv.reader(csvfile, delimiter=',')
# 	for row in datareader:
# 		if row[0].startswith("#"):
# 			continue
# 		else:
# 			cuisine[row[0]] += 1
# 			for ingredient in row[1:]:
# 				ingredients[ingredient] += 1

# # print len(ingredients)
# f = open("ingredients_stats", "w")
# for k, v in ingredients.iteritems():
# 	print >> f, k, v

def doLogisticRegression(train_X, train_Y, test_X, test_Y):
	logreg = linear_model.LogisticRegression(C=1e5)
	logreg.fit(train_X, train_Y)
	predictions = logreg.predict(test_X)

	count = 0
	for idx in range(len(predictions)):
		if predictions[idx] == test_Y[idx]:
			count+=1
	print count*1.0/len(test_Y)

	predictions = logreg.predict(train_X)
	count = 0
	for idx in range(len(predictions)):
		if predictions[idx] == train_Y[idx]:
			count+=1
	print count*1.0/len(train_Y)
	return predictions

X, Y, ingredientSet, cuisineMap = processDataSet.process("../project/data/recipe_data.csv")

def doNearestNeighborsClassification(train_X, train_Y, test_X, test_Y):
	neigh = KNeighborsClassifier()
	neigh.fit(train_X, train_Y) 
	predictions = neigh.predict(test_X)
	count = 0
	for idx in range(len(predictions)):
		if predictions[idx] == test_Y[idx]:
			count+=1
	print count*1.0/len(test_Y)
	return predictions


samples = range(len(Y))
random.shuffle(samples)
partition = int(0.8*len(samples))
train_x = [X[i] for i in samples[:partition]]
train_y = [Y[i] for i in samples[:partition]]
test_x = [X[i] for i in samples[partition+1:]]
test_y = [Y[i] for i in samples[partition+1:]]	

pred_logreg = doLogisticRegression(train_x, train_y, test_x, test_y)
## Takes a hell lot of time to run
# pred_knn = doNearestNeighborsClassification(train_x, train_y, test_x, test_y)


# Y = Counter(Y)
# predictions = Counter(predictions)
# for k, v in cuisineMap.iteritems():
# 	print 'cuisine: ', k, ' original:', Y[v], ' predicted: ', predictions[v]
