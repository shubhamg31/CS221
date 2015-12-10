import random
import csv, string
import collections

############################################################
# Meal Plan specifics.

# Information about a Recipe:
# - self.rid: recipe ID 
# - self.name: name of the recipe
# - self.cuisine: cuisine of recipe
# - self.calorieCount: calorie count of recipe
# - self.cookingTime: cooking time of recipe
# - self.servingSize: number of servings
# - self.ingredients: dictionary of ingredient names to quantity required (infinity for now)
class Recipe:
    def __init__(self, info):
        self.__dict__.update(info)

    def getName(self):
        return self.name

    def getCalorieCount(self):
        return self.calorieCount

    def getCookingTime(self):
        return self.cookingTime

    def getServingSize(self):
        return self.servingSize

    def getIngredients(self):
        return self.ingredients

    def getCuisine(self):
        return self.cuisine

    def getRating(self):
        return self.rating

    def getReviewCount(self):
        return self.reviewCount

    def has_all_ingreds(self, ingredsAvailable):
        if ingredsAvailable is None:
            return True
        return set(self.ingredients.keys()) < set(ingredsAvailable)

    def short_str(self): return '%s: %s' % (self.rid, self.name)

    def __str__(self):
        return 'Recipe{rid: %s, name: %s, cuisine: %s, calorie count: %s, cooking time: %s, serving size: %s, ingredients: %s}' % (self.rid, self.name, self.cuisine, self.calorieCount, self.cookingTime, self.servingSize, self.ingredients)

    def __eq__(self, other): return str(self) == str(other)

    def __cmp__(self, other): return cmp(str(self), str(other))

    def __hash__(self): return hash(str(self))

    def __repr__(self): return str(self)


# Information about all the Recipes
class RecipeBook:
    def __init__(self, recipesPath, profile):
        """
        Initialize the recipe book.

        @param recipesPath: Path of a file containing all the recipe information.
        """
        # Read recipes (CSV format)
        self.recipes = {}
        with open(recipesPath, 'rb') as dataset:
            for line in dataset:
                ingredients = collections.OrderedDict()
                line = line.split("<>")
                ingredString = line[6]
                ingredList = ingredString.split(',')
                for ingred in ingredList:
                    ingred = ingred.split(';')
                    slashPos = ingred[1].find('/')
                    intPart = 0
                    floatPart = 0.0
                    try:
                        if slashPos >= 0:
                            splits = ingred[1][:slashPos].split()
                            if len(splits)>1:
                                intPart = int(splits[0])
                            floatPart = (float(splits[-1])/float(ingred[1][slashPos+1:]))
                        else:
                            intPart = int(ingred[1])
                    except ValueError:
                        intPart = 0
                    ingredients[ingred[0]] = intPart + floatPart
#                if set(ingredients.keys()).issubset(set(profile.availableIngreds.keys())):
                flag = True
                for ingred in ingredients:
                    if ingred not in profile.availableIngreds or ingredients[ingred]>profile.availableIngreds[ingred]:
                        flag = False
                if flag:
                    recipeInfo = {}
                    recipeInfo["rid"] = line[0]
                    recipeInfo["name"] = line[1]
                    recipeInfo["cookingTime"] = int(line[2])
                    recipeInfo["calorieCount"] = int(line[3])
                    recipeInfo["rating"] = float(line[4])
                    recipeInfo["reviewCount"] = int(line[5])
                    recipeInfo["cuisine"] = None
                    recipeInfo["servingSize"] = None
                    recipeInfo["ingredients"] = ingredients
                    self.recipes[line[0]] = Recipe(recipeInfo)

# Given the path to a preference file and a
class Profile:
    def __init__(self, prefsPath):
        """
        Parses the preference file and generates a family's preferences.

        @param prefsPath: Path to a txt file that specifies the family's preferences
            in a particular format.
        """
        

        # Read preferences
        self.meals = []
        self.maxTotalCalories = float('inf')  # maximum total calories
        self.mealsToMaxTimes = {} # dict from meal to max cooking time
        self.availableIngreds = {} # dict from ingred to quantity
        lines = []
        file1 = open(prefsPath)
        lines = file1.readlines()
        self.maxTotalCalories = int(lines[0])
        i = 1
        while lines[i] != "---\n":
            mealToTimeReq = lines[i].split()
            if mealToTimeReq[0] in self.mealsToMaxTimes.keys():
                raise Exception("Cannot request %s more than once" % mealToTimeReq[0])
            self.meals.append(mealToTimeReq[0])
            self.mealsToMaxTimes[mealToTimeReq[0]] = int(mealToTimeReq[1])
            i+=1
        i+=1
        while lines[i] != "---\n":
            ingredToQty = lines[i].split(";")
            ingredToQty[0] = ingredToQty[0].replace("\n","")
            if ingredToQty[0] in self.availableIngreds.keys():
                raise Exception("Cannot mention %s more than once" % ingredToQty[0])
            if len(ingredToQty) > 1:
                slashPos = ingredToQty[1].find('/')
                intPart = 0
                floatPart = 0.0
                if slashPos >= 0:
                    splits = ingredToQty[1][:slashPos].split()
                    if len(splits)>1:
                        intPart = int(splits[0])
                    floatPart = (float(splits[-1])/float(ingredToQty[1][slashPos+1:]))
                else:
                    try:
                        intPart = int(ingredToQty[1])
                    except ValueError:
                        intPart = 0
                self.availableIngreds[ingredToQty[0].strip()] = intPart + floatPart
            else:
                self.availableIngreds[ingredToQty[0].strip()] = float("inf")
            i+=1
        if len(self.availableIngreds) == 0:
            self.availableIngreds = None
        self.requests = []
        '''
        i = 0
        nRecipes = 5
        maxCookingTime = max(self.mealsToMaxTimes.values())
        while i < nRecipes:
            recipe = random.choice(recipeBook.recipes.values())
            if recipe not in self.requests and recipe.getCookingTime() < maxCookingTime:
                self.requests.append(recipe)
                i+=1
        '''
    def setRecipeBook(self,recipeBook):
        self.recipeBook = recipeBook
        self.requests.extend(recipeBook.recipes.values())
    def print_info(self):
        print "Maximum Total Calories: %d" % self.maxTotalCalories
        print "Meals: %s" % self.mealsToMaxTimes.keys()
        print "Maximum Time per meal: %s" % self.mealsToMaxTimes
        print "Ingredients:"
        for ingred, qty in self.availableIngreds.iteritems(): print '%s: %s' % (ingred, qty)

'''
profile = Profile("exampleFamilyPref.txt")
profile.print_info()
recipeBook = RecipeBook("recipeData.txt", profile)
print recipeBook.recipes
'''
