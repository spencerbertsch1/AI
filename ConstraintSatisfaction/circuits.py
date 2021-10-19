# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College

from general_csp import CSP, Solution

# define the variables
# length tuple ()
x = {(3, 2), (5, 2), (2, 3), (7, 1)}

# define the domains
a_domain = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1),
            (6, 0), (6, 1), (7, 0), (7, 1)]
b_domain = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)]
c_domain = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
e_domain = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)]

# define domains for each variable in the CSP
d = {(3, 2): a_domain, (5, 2): b_domain, (2, 3): c_domain, (7, 1): e_domain}

# define the constraints
# there would be an incredibly huge number of constraints for this problem... let's just pass an empty list
c = []

sol = Solution(problem_type='Circuit Design')


if __name__ == "__main__":
    csp = CSP(x=x, d=d, c=c, verbose=True, csp_problem='circuits', solution=sol,
              use_inference=False,
              use_lcv=False,
              use_degree_heuristic=False,
              use_mrv=False)
    print(csp.backtracking_search())
