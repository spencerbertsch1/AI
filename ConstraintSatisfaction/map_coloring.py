# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College
from general_csp import CSP

# Countries (regions) are the variables in the CSP problem
# define the variables
x = {'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T'}

# define the domains
doms = ['red', 'green', 'blue']
# we might need something like this in the future vvv
d = {'WA': doms, 'NT': doms, 'Q': doms, 'NSW': doms, 'V': doms, 'SA': doms, 'T': doms}

# define the constraints
# write a function that takes 2 countries and their colors and returns True if that is ok, False if it's illegal
c = [('SA', 'WA'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'WA'),
     ('SA', 'V'), ('WA', 'NT'), ('NT', 'Q'), ('Q', 'NSW'), ('NSW', 'V')]

if __name__ == "__main__":
    print('Testing Constraint Satisfaction: Map Coloring')
    m_csp = CSP(x=x, d=d, c=c, verbose=False)
    print('MAP COLORING SOLUTION:')
    print(m_csp.backtracking_search())

