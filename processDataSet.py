#!/usr/bin/python

import random
import collections
import math
import sys
import csv
from collections import Counter

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
			Y.append(cuisineMap.get(cuisine))
	return X, Y, ingredientSet, cuisineMap


x, y, i, c = process('data.csv')
print x