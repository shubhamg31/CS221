import json, re, csv, string

# General code for representing a weighted CSP (Constraint Satisfaction Problem).
# All variables are being referenced by their index instead of their original
# names.
class CSP:
    def __init__(self):
        # Total number of variables in the CSP.
        self.numVars = 0

        # The list of variable names in the same order as they are added. A
        # variable name can be any hashable objects, for example: int, str,
        # or any tuple with hashtable objects.
        self.variables = []

        # Each key K in this dictionary is a variable name.
        # values[K] is the list of domain values that variable K can take on.
        self.values = {}

        # Each entry is a unary factor table for the corresponding variable.
        # The factor table corresponds to the weight distribution of a variable
        # for all added unary factor functions. If there's no unary function for 
        # a variable K, there will be no entry for K in unaryFactors.
        # E.g. if B \in ['a', 'b'] is a variable, and we added two
        # unary factor functions f1, f2 for B,
        # then unaryFactors[B]['a'] == f1('a') * f2('a')
        self.unaryFactors = {}

        # Each entry is a dictionary keyed by the name of the other variable
        # involved. The value is a binary factor table, where each table
        # stores the factor value for all possible combinations of
        # the domains of the two variables for all added binary factor
        # functions. The table is represented as a dictionary of dictionary.
        #
        # As an example, if we only have two variables
        # A \in ['b', 'c'],  B \in ['a', 'b']
        # and we've added two binary functions f1(A,B) and f2(A,B) to the CSP,
        # then binaryFactors[A][B]['b']['a'] == f1('b','a') * f2('b','a').
        # binaryFactors[A][A] should return a key error since a variable
        # shouldn't have a binary factor table with itself.

        self.binaryFactors = {}

    def add_variable(self, var, domain):
        """
        Add a new variable to the CSP.
        """
        if var in self.variables:
            raise Exception("Variable name already exists: %s" % str(var))

        self.numVars += 1
        self.variables.append(var)
        self.values[var] = domain
        self.unaryFactors[var] = None
        self.binaryFactors[var] = dict()


    def get_neighbor_vars(self, var):
        """
        Returns a list of variables which are neighbors of |var|.
        """
        return self.binaryFactors[var].keys()

    def add_unary_factor(self, var, factorFunc):
        """
        Add a unary factor function for a variable. Its factor
        value across the domain will be *merged* with any previously added
        unary factor functions through elementwise multiplication.

        How to get unary factor value given a variable |var| and
        value |val|?
        => csp.unaryFactors[var][val]
        """
        factor = {val:float(factorFunc(val)) for val in self.values[var]}
        if self.unaryFactors[var] is not None:
            assert len(self.unaryFactors[var]) == len(factor)
            self.unaryFactors[var] = {val:self.unaryFactors[var][val] * \
                factor[val] for val in factor}
        else:
            self.unaryFactors[var] = factor

    def add_binary_factor(self, var1, var2, factor_func):
        """
        Takes two variable names and a binary factor function
        |factorFunc|, add to binaryFactors. If the two variables already
        had binaryFactors added earlier, they will be *merged* through element
        wise multiplication.

        How to get binary factor value given a variable |var1| with value |val1| 
        and variable |var2| with value |val2|?
        => csp.binaryFactors[var1][var2][val1][val2]
        """
        # never shall a binary factor be added over a single variable
        try:
            assert var1 != var2
        except:
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            print '!! Tip:                                                                       !!'
            print '!! You are adding a binary factor over a same variable...                  !!'
            print '!! Please check your code and avoid doing this.                               !!'
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            raise

        self.update_binary_factor_table(var1, var2,
            {val1: {val2: float(factor_func(val1, val2)) \
                for val2 in self.values[var2]} for val1 in self.values[var1]})
        self.update_binary_factor_table(var2, var1, \
            {val2: {val1: float(factor_func(val1, val2)) \
                for val1 in self.values[var1]} for val2 in self.values[var2]})

    def update_binary_factor_table(self, var1, var2, table):
        """
        Private method you can skip for 0c, might be useful for 1c though.
        Update the binary factor table for binaryFactors[var1][var2].
        If it exists, element-wise multiplications will be performed to merge
        them together.
        """
        if var2 not in self.binaryFactors[var1]:
            self.binaryFactors[var1][var2] = table
        else:
            currentTable = self.binaryFactors[var1][var2]
            for i in table:
                for j in table[i]:
                    assert i in currentTable and j in currentTable[i]
                    currentTable[i][j] *= table[i][j]

def get_or_variable(csp, name, variables, value):
    """
    Create a new variable with domain [True, False] that can only be assigned to
    True iff at least one of the |variables| is assigned to |value|. You should
    add any necessary intermediate variables, unary factors, and binary
    factors to achieve this. Then, return the name of this variable.

    @param name: Prefix of all the variables that are going to be added.
        Can be any hashable objects. For every variable |var| added in this
        function, it's recommended to use a naming strategy such as
        ('or', |name|, |var|) to avoid conflicts with other variable names.
    @param variables: A list of variables in the CSP that are participating
        in this OR function. Note that if this list is empty, then the returned
        variable created should never be assigned to True.
    @param value: For the returned OR variable being created to be assigned to
        True, at least one of these variables must have this value.

    @return result: The OR variable's name. This variable should have domain
        [True, False] and constraints s.t. it's assigned to True iff at least
        one of the |variables| is assigned to |value|.
    """
    result = ('or', name, 'aggregated')
    csp.add_variable(result, [True, False])

    # no input variable, result should be False
    if len(variables) == 0:
        csp.add_unary_factor(result, lambda val: not val)
        return result

    # Let the input be n variables X0, X1, ..., Xn.
    # After adding auxiliary variables, the factor graph will look like this:
    #
    # ^--A0 --*-- A1 --*-- ... --*-- An --*-- result--^^
    #    |        |                  |
    #    *        *                  *
    #    |        |                  |
    #    X0       X1                 Xn
    #
    # where each "--*--" is a binary constraint and "--^" and "--^^" are unary
    # constraints. The "--^^" constraint will be added by the caller.
    for i, X_i in enumerate(variables):
        # create auxiliary variable for variable i
        # use systematic naming to avoid naming collision
        A_i = ('or', name, i)
        # domain values:
        # - [ prev ]: condition satisfied by some previous X_j
        # - [equals]: condition satisfied by X_i
        # - [  no  ]: condition not satisfied yet
        csp.add_variable(A_i, ['prev', 'equals', 'no'])

        # incorporate information from X_i
        def factor(val, b):
            if (val == value): return b == 'equals'
            return b != 'equals'
        csp.add_binary_factor(X_i, A_i, factor)

        if i == 0:
            # the first auxiliary variable, its value should never
            # be 'prev' because there's no X_j before it
            csp.add_unary_factor(A_i, lambda b: b != 'prev')
        else:
            # consistency between A_{i-1} and A_i
            def factor(b1, b2):
                if b1 in ['equals', 'prev']: return b2 != 'no'
                return b2 != 'prev'
            csp.add_binary_factor(('or', name, i - 1), A_i, factor)

    # consistency between A_n and result
    # hacky: reuse A_i because of python's loose scope
    csp.add_binary_factor(A_i, result, lambda val, res: res == (val != 'no'))
    return result

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
        return set(self.ingredients.keys()) < set(ingredsAvailable)

    def short_str(self): return '%s: %s' % (self.rid, self.name)

    def __str__(self):
        return 'Recipe{rid: %s, name: %s, cuisine: %s, calorie count: %s, cooking time: %s, serving size: %s, ingredients: %s}' % (self.rid, self.name, self.cuisine, self.calorieCount, self.cookingTime, self.servingSize, self.ingredients)


# Information about all the Recipes
class RecipeBook:
    def __init__(self, recipesPath):
        """
        Initialize the recipe book.

        @param recipesPath: Path of a file containing all the recipe information.
        """
        # Read recipes (CSV format)
        self.recipes = {}
        with open(recipesPath, 'rb') as dataset:
            datareader = csv.reader(dataset)
            for row in datareader:
                recipeInfo = {}
                recipeInfo["rid"] = row[0]
                recipeInfo["name"] = row[1]
                recipeInfo["cookingTime"] = int(row[2])
                recipeInfo["calorieCount"] = int(row[3])
                ingredients = {}
                for ingred in row[4:]:
                    idx = string.find(ingred,";")
                    if idx<0:
                        ingredients[ingred[0:idx]] = 0
                    else:
                        idx2 = string.find(ingred[idx+1:],";")
                        ingredients[ingred[0:idx]] = ingred[idx+1:idx2]
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
    def __init__(self, recipeBook, prefsPath):
        """
        Parses the preference file and generates a family's preferences.

        @param prefsPath: Path to a txt file that specifies the family's preferences
            in a particular format.
        """
        self.recipeBook = recipeBook

        # Read preferences
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
            self.mealsToMaxTimes[mealToTimeReq[0]] = int(mealToTimeReq[1])
            i+=1
        i+=1
        while lines[i] != "---\n":
            ingredToQty = lines[i].split(";")
            if ingredToQty[0] in self.availableIngreds.keys():
                raise Exception("Cannot mention %s more than once" % ingredToQty[0])
            self.availableIngreds[ingredToQty[0]] = " ".join(j for j in ingredToQty[1:])
            i+=1

    def print_info(self):
        print "Maximum Total Calories: %d" % self.maxTotalCalories
        print "Meals: %s" % self.mealsToMaxTimes.keys()
        print "Maximum Time per meal: %s" % self.mealsToMaxTimes
        print "Ingredients:"
        for ingred, qty in self.availableIngreds.iteritems(): print '%s - %s' % (ingred, qty)

#def extract_meal_plan_solution(profile, assign):
#    """
#    Given an assignment returned from the CSP solver, reconstruct the plan. It
#    is assume that (recipe, meal) is used as the variable to indicate if a recipe
#    is being assigned to a speific meal
#
#    @param profile: A family's preference
#    @param assign: An assignment of your variables as generated by the CSP
#        solver.
#
#    @return result: return a list of (quarter, courseId, units) tuples according
#        to your solution sorted in chronological of the quarters provided.
#    """
#    result = []
#    if not assign: return result
#    for quarter in profile.quarters:
#        for req in profile.requests:
#            cid = assign[(req, quarter)]
#            if cid == None: continue
#            if (cid, quarter) not in assign:
#                result.append((quarter, cid, None))
#            else:
#                result.append((quarter, cid, assign[(cid, quarter)]))
#    return result

def print_meal_plan_solution(solution):
    """
    Print a meal plan in a nice format based on a solution.

    @para solution: A list of (recipe, meal). 
    """

    if solution == None:
        print "No schedule found that satisfied all the constraints."
    else:
        print "Here's the best schedule:"
        print "Quarter\t\tUnits\tCourse"
        for quarter, course, units in solution:
            if units != None:
                print "  %s\t%s\t%s" % (quarter, units, course)
            else:
                print "  %s\t%s\t%s" % (quarter, 'None', course)

recipeBook = RecipeBook('test.csv')
profile = Profile(recipeBook, "exampleFamilyPref.txt")
profile.print_info()
