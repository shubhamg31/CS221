import random
import collections
import math
import sys
import csv
from collections import Counter

cuisineIngrDict = collections.defaultdict(list)
ingrCount = {}
common5 = {}
def readFile(filename):
	with open(filename, 'rb') as dataset:
		datareader = csv.reader(dataset)
		for row in datareader:
			cuisineIngrDict[row[0]].append(row[1:])
	for k, v in cuisineIngrDict.iteritems():
		ingrCount[k] = collections.Counter()
		for ingrList in v:
			for ingr in ingrList:
				ingrCount[k][ingr]+=1
		common5[k] = ingrCount[k].most_common(5)
		print k, "&", "&".join(s[0] for s in common5[k])

readFile("data.csv")
