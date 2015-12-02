import random
import csv, string

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

    def has_all_ingreds(self, ingredsAvailable):
        if ingredsAvailable is None:
            return True
        return set(self.ingredients.keys()) < set(ingredsAvailable)

    def short_str(self): return '%s: %s' % (self.rid, self.name)

    def __str__(self):
        return 'Recipe{rid: %s, name: %s, cuisine: %s, calorie count: %s, cooking time: %s, serving size: %s, ingredients: %s}' % (self.rid, self.name, self.cuisine, self.calorieCount, self.cookingTime, self.servingSize, self.ingredients)


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
            datareader = csv.reader(dataset)
            for row in datareader:
                ingredients = {}
                for ingred in row[4:]:
                    idx = string.find(ingred,";")
                    if idx<0:
                        ingredients[ingred[0:idx]] = 0
                    else:
                        idx2 = string.find(ingred[idx+1:],";")
                        ingredients[ingred[0:idx]] = ingred[idx+1:idx2]
                if set(ingredients.keys()).issubset(set(profile.availableIngreds.keys())):
                    recipeInfo = {}
                    recipeInfo["rid"] = row[0]
                    recipeInfo["name"] = row[1]
                    recipeInfo["cookingTime"] = int(row[2])
                    recipeInfo["calorieCount"] = int(row[3])
                    recipeInfo["cuisine"] = None
                    recipeInfo["servingSize"] = None
                    recipeInfo["ingredients"] = ingredients
                    self.recipes[row[0]] = Recipe(recipeInfo)

# A request to take one of a set of courses at some particular times.
class Request:
    def __init__(self, rid, meals, weight):
        """
        Create a Request object.

        @param rid: The rid of recipe
        @param meals: meals for which the recipe satisfies all contraints
        @param weight: real number denoting how good the recipe is. (if cuisine pref for meal is added)
        """
        self.rid = rid
        self.meals = meals
        self.weight = weight

    def __str__(self):
        return 'Request{Recipe Id: %s, Meals: %s, Weight: %s}' % \
            (self.id, self.meals, self.weight)

    def __eq__(self, other): return str(self) == str(other)

    def __cmp__(self, other): return cmp(str(self), str(other))

    def __hash__(self): return hash(str(self))

    def __repr__(self): return str(self)

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
            self.availableIngreds[ingredToQty[0]] = " ".join(j for j in ingredToQty[1:]).replace("\n","")
            i+=1
        if len(self.availableIngreds) == 0:
            self.availableIngreds = None
        self.requests = []
        '''
        i = 0
        nRecipes = 10
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
        for ingred, qty in self.availableIngreds.iteritems(): print '%s - %s' % (ingred, qty)

profile = Profile("exampleFamilyPref.txt")
recipeBook = RecipeBook("test.csv", profile)
profile.print_info()
print recipeBook.recipes
