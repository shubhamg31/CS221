import random
import plannerReqs
import csp
import algorithms
import util
import collections
import copy

def verify_meal_plan(recipeBook, profile, meal_plan):
    """
    Returns true if the meal plan satisifies all requirements given by the profile.
    Meal Plan is a tuple of (meal, recipe)
    """
    goodSchedule = True
    all_recipes = [s[1] for s in meal_plan]

    # No recipe can be made twice.
    goodSchedule *= len(set(all_recipes)) == len(all_recipes)
    if not goodSchedule:
        print 'recipe repeated'
        return False

    # # Ingredients of recipe should be available
    # goodSchedule *= all(recipe.has_all_ingreds(profile.availableIngreds) for recipe in all_recipes)
    # if not goodSchedule:
    #     print 'ingredients not available for recipe'
    #     return False

    # Check for calorie counts
    calorieCount = 0
    for recipe in all_recipes:
        calorieCount += recipe.getCalorieCount()
    goodSchedule *= calorieCount <= profile.maxTotalCalories
    if not goodSchedule:
        print 'calorie count out of bound'
        return False

    # Check for cooking times
    goodSchedule *= all(profile.mealsToMaxTimes[meal]>=recipe.getCookingTime() for meal, recipe in meal_plan)
    if not goodSchedule:
        print 'cooking time out of bound'
        return False

    return goodSchedule

recipeBook = plannerReqs.RecipeBook('test.csv')
profile = plannerReqs.Profile(recipeBook, "../exampleFamilyPref.txt")
profile.print_info()
cspConstructor = csp.MealPlanCSPConstructor(recipeBook, copy.deepcopy(profile))
mealCSP = cspConstructor.get_basic_csp()
alg = submission.BacktrackingSearch()
alg.solve(mealCSP)