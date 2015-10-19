#!/usr/bin/python

import sklearn
import mlpy
import numpy as np
import scipy as sp
import csv
import string
from collections import * 
import processDataset
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

# X, Y, ingredientSet, cuisineMap = processDataset.process()
X = np.random.rand(10000,2)
Y = np.random.rand(10000,1)
Y = [1 if label > 0.5 else 0 for label in Y]
predictions = doLogisticRegression(X, Y)
