#!/usr/bin/python

import random
import collections
import math
import sys
import csv
from collections import Counter

def process(filename)
	with open(filename, 'rb') as dataset:
		datareader = csv.reader(dataset)
		for row in datareader:
			print row[0]
			print ' '.join(row)



process(data.csv)