import csv
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import pyparsing

MINUTES_IN_DAY = 24*60
MINUTES_IN_HOUR = 60
LEMMATIZER = WordNetLemmatizer()

ACTIONS = [line.strip() for line in open("wordlists/food_adjectives.txt", 'r')]
UNITS = [line.strip() for line in open("wordlists/units_of_measure.txt", 'r')]

def getMinutesfromTime(time):
	time = time.split()
	minutes = 0
	curr = 0
	if 'd' in time:
		minutes += int(time[curr])*MINUTES_IN_DAY
		curr += 2
	
	if 'h' in time:
		minutes += int(time[curr])*MINUTES_IN_HOUR
		curr += 2
	
	if 'm' in time:
		minutes += int(time[curr])
	return minutes

def getTitle(row):
	title = ""
	for idx, elem in enumerate(row[1:]):
		if elem and elem != 'null':
			if idx != 0 and elem[0].isdigit():
				break
			else:
				title = title + elem	
		else:
			break
	return idx+1, title

def parseIngredients(ingredients):
	parsed_ingredients = []
	for elem in ingredients:
		if not elem or not elem[0].isdigit():
			continue

		elem = re.sub('\(.*?\)','', elem)
		elem = elem.replace("\xe5\xa8", "")
		elem = elem.replace("\x89\xe3\xa2", "")
		elem = elem.replace("\xc2\xae", "")
		elem = elem.replace("\xe2\x84\xa2", "")
		elem = elem.replace("\xe2\x80\x99s", "")
		elem = elem.replace("\xe2\x80\x99S", "")
		elem = elem.replace("\xc2\x96", "")
		elem = elem.replace("\xe2\x84\xa2", "")
		# To correct jalapeno
		elem = elem.replace("\xc3\xb1", "n")

		elem = elem.split()
		action = ""
		ingredient_name = ""
		units = ""
		measure = ""
		for e in elem:
			try:
				e = LEMMATIZER.lemmatize(e)
			except UnicodeDecodeError:
				return None

			if e in ACTIONS or e.endswith("ed"):
				action += e + " "
			elif e in UNITS:
				units += e + " "
			elif e[0].isdigit():
				measure += e + " "
			else:
				ingredient_name += e + " "
		parsed_ingredients.append(ingredient_name.strip()+";"+measure.strip())
	return parsed_ingredients

valid = 0
output = open('data.csv', 'wb')
csvwriter = csv.writer(output)

with open('scraped.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile)
	all = set()
	verbs = set()
	for row in spamreader:
		# print row
		id = int(row[0])
		idx, title = getTitle(row)
		# print idx
		if not row[idx] or row[idx] == 'null':
			continue
		time = getMinutesfromTime(row[idx])
		idx += 1

		if not row[idx] or row[idx] == 'null':
			continue
		calorie = row[idx]
		idx += 1

		if not calorie.isdigit():
			continue

		ingredients_list = parseIngredients(row[idx:])
		recipe = [id, title, time, calorie]

		if not ingredients_list:
			print id
			print row[idx:]
			continue

		for ingredient in ingredients_list:
			recipe.append(ingredient)

		csvwriter.writerow(recipe)
		valid += 1

output.close()
print valid

