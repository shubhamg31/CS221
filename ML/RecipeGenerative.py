import random
import collections
import math
import sys
import csv
import operator
from collections import Counter


def readFile(filename):
    cuisineIngrDict = collections.defaultdict(list)
    countOfCuisine = collections.Counter()
    testSet = []
    with open(filename, 'rb') as dataset:
        datareader = csv.reader(dataset)
        for row in datareader:
            if random.random() < 0.9:
                cuisineIngrDict[row[0]].append(row[1:])
                countOfCuisine[row[0]]+=1
            else:
                testSet.append(row)
    return cuisineIngrDict, testSet, countOfCuisine

def generateModels(cuisineIngrDict):
    ingrCount = {}
    for k, v in cuisineIngrDict.iteritems():
        for ingrList in v:
            for ingr in ingrList:
                if ingr not in ingrCount.keys():
                    ingrCount[ingr] = collections.Counter()
                ingrCount[ingr][k]+=1
    return ingrCount

def predictCuisine(listOfIngreds, ingrCount, countOfCuisine):
    probOfCuisine = {}
    for ingred in listOfIngreds:
        if ingred in ingrCount:
            cuisine, count = ingrCount[ingred].most_common(1)[0]
            totalOccur = sum([counts for _,counts in ingrCount[ingred].most_common()])
            if cuisine not in probOfCuisine:
                probOfCuisine[cuisine] = 0.0
            probOfCuisine[cuisine] += (count*1.0/totalOccur)
    return max(probOfCuisine.iteritems(), key=lambda x: x[1]*countOfCuisine[x[0]])[0]

cuisineIngrDict, testSet, countOfCuisine = readFile("data.csv")
ingrCount = generateModels(cuisineIngrDict)
wrong = 0
for row in testSet:
    prediction = predictCuisine(row[1:], ingrCount, countOfCuisine)
    if prediction != row[0]:
        wrong+=1
print "Fraction of wrong classifications:", str(wrong*1.0/len(testSet))
