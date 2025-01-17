import util, collections
class MealPlanCSPConstructor():

    def __init__(self, recipebook, profile):
        """
        Saves the necessary data.

        @param recipebook: A recipe book with a list of recipes
        @param profile: A user's profile and requests
        """
        self.recipebook = recipebook.recipes
        self.profile = profile

    def get_basic_csp(self):
        """
        Return a CSP that only enforces the basic constraints that a course can
        only be taken when it's offered and that a request can only be satisfied
        in at most one quarter.

        @return csp: A CSP where basic variables and constraints are added.
        """
        csp = CSP()
        self.add_variables(csp)
        self.add_norepeating_constraints(csp)
        self.add_cooking_time_constraints(csp)
        self.add_calorie_count_constraint(csp)
        self.assign_validRecipe_everyMeal(csp)
        self.add_ingredient_quantity_constraint(csp)
        self.add_hot_contraints(csp)
        self.add_recipe_weights(csp)
        self.add_shelf_life_constraints(csp)
        return csp

    def add_variables(self, csp):
        """
        Adding the variables into the CSP. Each variable, (recipe, day),
        can take on the value of one of the courses requested in req or None.

        @param csp: The CSP where the additional constraints will be added to.
        """
        for req in self.profile.requests:
            for meal in self.profile.meals:
                csp.add_variable((req, meal), [True, False])

    def add_norepeating_constraints(self, csp):
        """
        No recipe can be repeated. 

        @param csp: The CSP where the additional constraints will be added to.
        """
        for req in self.profile.requests:
            for meal in self.profile.meals:
                for meal2 in self.profile.meals:
                    if meal == meal2: continue
                    csp.add_binary_factor((req, meal), (req, meal2), \
                        lambda taken1, taken2: not (taken1 and taken2))

    def assign_validRecipe_everyMeal(self, csp):
        for meal in self.profile.meals:
            requests = []
            for req in self.profile.requests:
                requests.append((req, meal))
            orVar = util.get_or_variable(csp, (meal), requests, True)    
            csp.add_unary_factor(orVar, lambda v: True if v else False)

    def add_cooking_time_constraints(self, csp):
        for req in self.profile.requests:
            for meal in self.profile.meals:
                csp.add_unary_factor((req, meal), lambda taken1: req.getCookingTime() <= self.profile.mealsToMaxTimes[meal] if taken1 else True)

    def add_hot_contraints(self,csp):
        def readHotVerbs(fileName):
            hotVerbs = []
            with open(fileName, 'rb') as dataset:
                for line in dataset:
                    line = line.replace("\n","")
                    hotVerbs.append(line)
            return hotVerbs
        def isHot(hotVerbs, recipe):
            for verb in hotVerbs:
                if verb in recipe.getInstructions():
                    return True
            return False
        hotVerbs = readHotVerbs("hotVerbs.txt")
        for req in self.profile.requests:
            for meal in self.profile.meals:
                if meal in self.profile.hotMeals:
                    csp.add_unary_factor((req, meal), lambda taken1: isHot(hotVerbs, req) if taken1 else True)

    def add_calorie_count_constraint(self, csp):
        varsList = []
        for req in self.profile.requests:
            for meal in self.profile.meals:
                var = (req.rid, meal)
                csp.add_variable(var, [0,req.getCalorieCount()])
                varsList.append(var)
                csp.add_binary_factor((req, meal), var, lambda taken1, calorieCount: calorieCount > 0 if taken1 else calorieCount == 0 )
        util.get_sum_variable(csp, "total", varsList, self.profile.maxTotalCalories)

    def add_ingredient_quantity_constraint(self, csp):
        for ingred in self.profile.availableIngreds:
            varsList = []
            for req in self.profile.requests:
                if req.getIngredients()[ingred] > 0:
                    for meal in self.profile.meals:                    
                        var = (req.rid, meal, ingred)
                        if ingred in req.getIngredients():
                            csp.add_variable(var, [0,req.getIngredients()[ingred]])
                        else:
                            csp.add_variable(var, [0])
                        varsList.append(var)
                        csp.add_binary_factor((req, meal), var, lambda taken1, ingredQty: ingredQty > 0 if taken1 else ingredQty == 0 )
            util.get_sum_variable(csp, ingred + "total", varsList, self.profile.availableIngreds[ingred])

    def add_recipe_weights(self, csp):
        for req in self.profile.requests:
            weight = req.getRating()
            for meal in self.profile.meals:
                csp.add_unary_factor((req, meal), lambda taken: weight if taken else 1.0)

    def add_shelf_life_constraints(self, csp):
        for req in self.profile.requests:
            for idx, meal in enumerate(self.profile.meals):
                csp.add_unary_factor((req, meal), lambda taken1: min(req.getShelfLife().values()) >= idx+1 if taken1 else True)

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
