import random
import collections
import math
import sys
import copy
import csv
from collections import Counter
import time

def process(filename, currSetOfIngreds):
    possAdds = Counter()
    with open(filename, 'rb') as dataset:
        datareader = csv.reader(dataset)
        for row in datareader:
            recipeIngredients = set(row[1:])
            if currSetOfIngreds.issubset(recipeIngredients):
                otherIngreds = recipeIngredients - currSetOfIngreds
                for otherIngred in otherIngreds:
                    possAdds[otherIngred] += 1
    return possAdds

def calcProbs(listOfRecipes, listOfIngreds):
    dictOfProbs = collections.Counter()
    ingredSetN = [[]]
    for nIngreds in xrange(1, 3):
        print nIngreds
        ingredSetN1 = []
        for ingred in listOfIngreds:
            for set1 in ingredSetN:
                setNew = copy.deepcopy(set1)
                if ingred not in setNew:
                    setNew.append(ingred)
                    ingredSetN1.append(setNew)
                    for recipe in listOfRecipes:
                        if set(setNew) in set(recipe):
                            dictOfProbs[setNew]+=1
        ingredSetN = []
        ingredSetN.extend(ingredSetN1)
        f = open('subsetProbabilities'+str(nIngreds)+".txt", 'w')
        for k,v in dictOfProbs.iteritems():
            string = ""
            for ing in k:
                string += (str(ing)+" ")
            f.write(string + str(v) + "\n")
        f.close()
    return dictOfProbs

dataFile = "data.csv"
start_time = time.time()
correct = 0
wrong = 0
recipes = []
with open(dataFile, 'rb') as dataset:
        datareader = csv.reader(dataset)
        for row in datareader:
            recipes.append(row[1:])
f = open('mostLikelyNextIngredResults.txt', 'w')
for allIngreds in recipes:
        removedIngred = random.choice(allIngreds)
        allIngreds.remove(removedIngred)
        possAdds = process("data.csv",set(allIngreds))
        if possAdds.most_common(1)[0][0] == removedIngred:
            f.write("Correct - " + removedIngred + possAdds.most_common(1)[0][0] + str(allIngreds))
            correct+=1
        else:
            wrong +=1
            f.write("Wrong - " + removedIngred + possAdds.most_common(1)[0][0] + str(allIngreds))
        print "Total - %d, Fraction of Correct Predictions - %f" %(correct+wrong, correct*1.0/(correct+wrong))
f.close()
print("--- %s seconds ---" % (time.time() - start_time))
#dictOfProbs = calcProbs(recipes, listOfIngreds)
