import json, re
import plannerReqs
import csp
import algorithms
import util

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

def get_sum_variable(csp, name, variables, maxSum):
    """
    Given a list of |variables| each with non-negative integer domains,
    returns the name of a new variable with domain range(0, maxSum+1), such that
    it's consistent with the value |n| iff the assignments for |variables|
    sums to |n|.

    @param name: Prefix of all the variables that are going to be added.
        Can be any hashable objects. For every variable |var| added in this
        function, it's recommended to use a naming strategy such as
        ('sum', |name|, |var|) to avoid conflicts with other variable names.
    @param variables: A list of variables that are already in the CSP that
        have non-negative integer values as its domain.
    @param maxSum: An integer indicating the maximum sum value allowed. You
        can use it to get the auxiliary variables' domain

    @return result: The name of a newly created variable with domain range
        [0, maxSum] such that it's consistent with an assignment of |n|
        iff the assignment of |variables| sums to |n|.
    """
    # BEGIN_YOUR_CODE (around 20 lines of code expected)
    result = ('sum', name, 'aggregated')
    csp.add_variable(result, range(maxSum+1))

    if len(variables) == 0:
        csp.add_unary_factor(result, lambda val: not val)
        return result

    prev_domain = [(0,0)]
    # for i in range(maxSum+1):
    #     for j in range():
    #         domain.append(i, j)
    for i, X_i in enumerate(variables):
        domain_i = csp.values[X_i]
        curr_domain = list(set([(x1[1], x1[1]+x2) for x1 in prev_domain for x2 in domain_i if x1[1]+x2<=maxSum]))
        A_i = ('sum', name, i)
        csp.add_variable(A_i, curr_domain)
        prev_domain = curr_domain
        if i == 0:
            csp.add_unary_factor(A_i, lambda b: b[0] == 0)
        else:
            csp.add_binary_factor(('sum', name, i-1), A_i, lambda a,b: a[1] == b[0])
        csp.add_binary_factor(X_i, A_i, lambda a,b: b[1] == b[0] + a)

    csp.add_binary_factor(A_i, result, lambda a, b: a[1] == b)
    return result
    # def checkPrev(prevVal, curVal):
    #     if(prevVal[1] == curVal[0]):
    #         return True
    #     return False
    # domainVals = []
    # for k in xrange(maxSum + 1):
    #     for l in xrange(maxSum + 1):
    #         domainVals.append((k, l))

    # result = ('sum', name, 'aggregated')
    # csp.add_variable(result, range(maxSum+1))
    # if len(variables) == 0:
    #     csp.add_unary_factor(result, lambda val: not val)
    #     return result
    # for i, X_i in enumerate(variables):
    #     A_i = ('sum', name, i)
    #     csp.add_variable(A_i, domainVals)
    #     def checkSum(xval, bval):
    #         if(xval + bval[0] == bval[1]): return True
    #         return False
    #     csp.add_binary_factor(X_i, A_i, checkSum)
    #     if i == 0:
    #         csp.add_unary_factor(A_i, lambda b: b[0] == 0)
    #     else:
    #         csp.add_binary_factor(('sum', name, i - 1), A_i, checkPrev)
    # csp.add_binary_factor(A_i, result, lambda aval, rval: rval == aval[1])
    # return result
    # END_YOUR_CODE

def extract_meal_plan_solution(profile, assign):
   """
   Given an assignment returned from the CSP solver, reconstruct the plan. It
   is assume that (recipe, meal) is used as the variable to indicate if a recipe
   is being assigned to a speific meal

   @param profile: A family's preference
   @param assign: An assignment of your variables as generated by the CSP
       solver.

   @return result: return a list of (quarter, courseId, units) tuples according
       to your solution sorted in chronological of the quarters provided.
   """
   result = []
   if not assign: return result
   for meal in profile.meals:
       for req in profile.requests:
            isCooked = assign[(req, meal)]
            if isCooked == False: 
                continue
            else:
                result.append((req, meal))
   return result

def print_meal_plan_solution(solution):
    """
    Print a meal plan in a nice format based on a solution.

    @para solution: A list of (recipe, meal). 
    """

    if solution == None:
        print "No schedule found that satisfied all the constraints."
    else:
        print "Here's the best schedule:"
        print "Recipe\t\tMeal"
        for recipe, meal in solution:
            print "  %s\t%s" % (recipe, meal) 

# recipeBook = RecipeBook('test.csv')
# profile = Profile(recipeBook, "exampleFamilyPref.txt")
