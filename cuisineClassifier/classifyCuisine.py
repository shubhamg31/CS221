import collections
import mlpy
import numpy as np
import scipy as sp
import csv
import string
from sklearn import linear_model

recipesPath = '../mealplan/recipeData.txt'

cuisineMap = {}
cuisineMap['NorthernEuropean'] =250
cuisineMap['WesternEuropean'] =2659
cuisineMap['SouthernEuropean'] =4180
cuisineMap['MiddleEastern'] =645
cuisineMap['SouthAsian'] =621
cuisineMap['LatinAmerican'] =2917
cuisineMap['NorthAmerican'] =41524
cuisineMap['EasternEuropean'] =381
cuisineMap['SoutheastAsian'] =457
cuisineMap['African'] =352
cuisineMap['EastAsian'] =2512

oppMap = {}
for k,v in cuisineMap.iteritems():
	oppMap[v] = k

def process(filename):
	ingredientSet = getIngreds()
	X = []
	Y = []
	ingredientsList = []
	countCuisine = 0
	with open(filename, 'rb') as dataset:
		datareader = csv.reader(dataset)
		tempX = []
		for row in datareader:
			cuisine = row[0]
			orig = row[1:]
			ingredients = collections.Counter(orig)
			ingredientsList.append(orig)
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
		return X, Y, ingredientSet, cuisineMap, ingredientsList

def readIngredients(predictor, ingredientSet):
	ingredientsList = collections.OrderedDict()
	with open(recipesPath, 'rb') as dataset, open('./recipeWithCuisines.txt', 'wb') as output:
		for line in dataset:
			orig = line.strip()
			ingredients = []
			line = line.split("<>")
			ingredString = line[6]
			ingredList = ingredString.split(',')
			for ingred in ingredList:
				ingred = ingred.split(';')
				ingredients.append(ingred[0])
			testX = constructFeatureVector(ingredients, ingredientSet)
			cuisine = predictor.predict([testX])
			output.write(orig + "<>" + oppMap[cuisine[0]] + '\n')
	return ingredientsList

def constructFeatureVector(ingredients, ingredientSet):
	featureVector = [0] * len(ingredientSet)
	for index, ingredient in enumerate(ingredientSet):
		if ingredient in ingredients:
			featureVector[index] = 1
		else:
			featureVector[index] = 0
	return featureVector

def getIngreds(file1='ingredients_stats'):
	ingredientSet = set()
	with open(file1, 'rb') as f:
		for line in f:
			ingredientSet.add(line.split()[0])
	return ingredientSet

def predictCuisine(trainX, trainY):
	logreg = linear_model.LogisticRegression()
	logreg.fit(trainX, trainY)
	return logreg


trainX, trainY, ingredientSet, cuisineMap, trainIngredientsList = process("./data.csv")
predictor = predictCuisine(trainX, trainY)
recipeIngredientsList = readIngredients(predictor, ingredientSet)
