import csv

out = open("missin_ids.txt", "w")
data_1 = [int(line.rstrip('\n').split(',')[0]) for line in open('data.csv', 'r')]
data_2 = [int(line.rstrip('\n').split(',')[0]) for line in open('scraped_p2.txt', 'r')]

# count = 0
# for id in data_1:
# 	if id not in data_2:
# 		print id
# 		out.write(str(id) + "\n")
# 		count += 1
# out.close()
# print count

output = open('recipeData.txt', 'wb')
data_1 = [line.rstrip('\n') for line in open('data.csv', 'r')]
data_2_raw = [line.rstrip('\n') for line in open('scraped_p2.txt', 'r')]

data_2 = {}
for line in data_2_raw:
	id, features = line.rstrip('|').replace('|', ';').split(',', 1)
	data_2[id] = features

output = open('recipeData.txt', 'wb')
for line in data_1:
	id, title, time, calories, ingredients = line.split(',', 4)
	rating, review, directions = data_2[id].split(',', 2)
	data = id + "<>" + title + "<>" + time + "<>" + calories + "<>" + rating + "<>" + review + "<>" + ingredients.rstrip() + "<>" + directions + "\n"
	output.write(data)

output.close()
