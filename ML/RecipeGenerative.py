import random
import collections
import math
import sys
import csv
import operator
from collections import Counter


def readFile(filename):
    cuisineIngrDict = collections.defaultdict(list)
    testSet = []
    with open(filename, 'rb') as dataset:
        datareader = csv.reader(dataset)
        for row in datareader:
            if random.random() < 0.8:
    			cuisineIngrDict[row[0]].append(row[1:])
            else:
                testSet.append(row)
    return cuisineIngrDict, testSet

def generateModels(cuisineIngrDict):
    ingrCount = {}
    for k, v in cuisineIngrDict.iteritems():
        for ingrList in v:
            for ingr in ingrList:
                if ingr not in ingrCount.keys():
                    ingrCount[ingr] = collections.Counter()
                ingrCount[ingr][k]+=1
    return ingrCount

def predictCuisine(listOfIngreds, ingrCount):
    probOfCuisine = {}
    for ingred in listOfIngreds:
        if ingred in ingrCount:
            cuisine, count = ingrCount[ingred].most_common(1)[0]
            totalOccur = sum([counts for _,counts in ingrCount[ingred].most_common()])
            if cuisine not in probOfCuisine:
                probOfCuisine[cuisine] = 0.0
            probOfCuisine[cuisine] += (count*1.0/totalOccur)
    return max(probOfCuisine.iteritems(), key=operator.itemgetter(1))[0]

cuisineIngrDict, testSet = readFile("data.csv")
ingrCount = generateModels(cuisineIngrDict)
wrong = 0
for row in testSet:
    prediction = predictCuisine(row[1:], ingrCount)
    if prediction != row[0]:
        wrong+=1
print "Fraction of wrong classifications:", str(wrong*1.0/len(testSet))
