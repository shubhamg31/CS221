#!/usr/bin/python

import sklearn
import mlpy
import numpy as np
import scipy as sp
import csv
import string
from collections import * 
import processDataSet
from sklearn import linear_model

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

def doLogisticRegression(X, Y):
	logreg = linear_model.LogisticRegression(C=1e5)
	logreg.fit(X, Y)
	predictions = logreg.predict(X)

	count = 0
	for idx in range(len(predictions)):
		if predictions[idx] == Y[idx]:
			count+=1
	print count*1.0/len(Y)
	return predictions

X, Y, ingredientSet, cuisineMap = processDataSet.process("../project/data/recipe_data.csv")
predictions = doLogisticRegression(X, Y)
Y = Counter(Y)
predictions = Counter(predictions)
for k, v in cuisineMap.iteritems():
	print 'cuisine: ', k, ' original:', Y[v], ' predicted: ', predictions[v]
