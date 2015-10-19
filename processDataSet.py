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
		for row in datareader:
			cuisine = row[0]
			if cuisine not in cuisineMap:
				cuisineMap[cuisine] = countCuisine
				countCuisine = countCuisine + 1
			ingredients = collections.Counter(row[1:])
			X.append(ingredients)
			Y.append(cuisineMap.get(cuisine))
			ingredientSet.update(ingredients)
	return X, Y, ingredientSet, cuisineMap