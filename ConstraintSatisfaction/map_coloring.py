# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College


#  Countries (regions) are the variables in the CSP problem

class map_csp:

    def __init__(self, x, d, c):
        self.x = x
        self.d = d
        self.c = c

    def __repr__(self):
        return '\n'.join([
            f'Variables: {self.x}',
            f'Domains: {self.d}',
            f'Constraints: {self.c}'
        ])


if __name__ == "__main__":
    print('Testing Constraint Satisfaction: Map Coloring')

    # define the variables
    x = {'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T'}

    # define the domains
    d = {'WA': {'red', 'green', 'blue'},
         'NT': {'red', 'green', 'blue'},
         'Q': {'red', 'green', 'blue'},
         'NSW': {'red', 'green', 'blue'},
         'V': {'red', 'green', 'blue'},
         'SA': {'red', 'green', 'blue'},
         'T': {'red', 'green', 'blue'}
         }

    # define the constraints
    c = [('SA', 'WA'), ('SA', 'NT'), ('SA', 'Q'), ('SA', 'NSW'), ('SA', 'WA'),
         ('SA', 'V'), ('WA', 'NT'), ('NT', 'Q'), ('Q', 'NSW'), ('NSW', 'V')]

    m_csp = map_csp(x=x, d=d, c=c)
    print(m_csp)
