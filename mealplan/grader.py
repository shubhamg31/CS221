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

profile = plannerReqs.Profile("exampleFamilyPref.txt")
# recipeBook = plannerReqs.RecipeBook('../recipeData.txt', profile)
# recipeBook = plannerReqs.RecipeBook('test.csv', profile)
recipeBook = plannerReqs.RecipeBook('recipeData.txt', profile)
profile.setRecipeBook(recipeBook)
#profile.print_info()
cspConstructor = csp.MealPlanCSPConstructor(recipeBook, copy.deepcopy(profile))
mealCSP = cspConstructor.get_basic_csp()
alg = algorithms.BacktrackingSearch()
alg.solve(mealCSP, True, True)
# assignment = alg.allAssignments[0]
# print assignment
solution = util.extract_meal_plan_solution(profile, alg.optimalAssignment)
util.print_meal_plan_solution(solution)
# for assignment in alg.allAssignments:
#     sol = util.extract_meal_plan_solution(profile, assignment)
#     util.print_meal_plan_solution(sol)
