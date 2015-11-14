import random
import collections
import math
import sys
import csv
import bisect
from collections import Counter
import time


file1 = "data.csv"
#file2 = "dataWithRandTime.csv"

listOfRecipes = []
allIngred = set([])

reader = csv.reader(open(file1, 'rb'))
for row in reader:
    listOfRecipes.append([random.randint(10,300)] + row)
    allIngred.update(row[1:])

print len(listOfRecipes)
inpListIngred = random.sample(listOfRecipes, 1)[0][2:]
print inpListIngred
listOfRecipes.sort(key=lambda x: x[0])
start_time = time.time()
for recipe in listOfRecipes:
    setIngrInRecipe = set(recipe[2:])
    setInpList = set(inpListIngred)
    if setIngrInRecipe.issubset(setInpList):
        if len(setIngrInRecipe-setInpList)<3 and abs(len(setIngrInRecipe)-len(setInpList))<3:
            print recipe
            break
print("--- %s seconds ---" % (time.time() - start_time))
