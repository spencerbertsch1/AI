# Spencer Bertsch
# October 2021
# Assignment 4
# CS 276 @ Dartmouth College

from general_csp import CSP, Solution

# define the variables
x = [(3, 2), (5, 2), (2, 3), (7, 1)]

board_size: tuple = (10, 3)
# first we need to generate the domains
a_domain, b_domain, c_domain, e_domain = [], [], [], []
for piece in range(len(x)):
    for n in range(board_size[0]):
        for m in range(board_size[1]):
            # width of the piece
            w = x[piece][0]
            # height of the piece
            h = x[piece][1]

            # if we fell off the board:
            if ((n + w) <= board_size[0]) & ((m + h) <= board_size[1]):
                new_domain = (n, m)
            else:
                continue

            # if we are still on the board, we add the location to the domain
            if piece == 0:
                a_domain.append(new_domain)
            elif piece == 1:
                b_domain.append(new_domain)
            elif piece == 2:
                c_domain.append(new_domain)
            elif piece == 3:
                e_domain.append(new_domain)


# we could also define the domains manually
# I left this commented because generating domains programmatically is better
# a_domain = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1),
#             (6, 0), (6, 1), (7, 0), (7, 1)]
# b_domain = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)]
# c_domain = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
# e_domain = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)]

# define domains for each variable in the CSP
d = {(3, 2): a_domain, (5, 2): b_domain, (2, 3): c_domain, (7, 1): e_domain}

# define the constraints
# there would be an incredibly huge number of constraints for this problem... let's just pass an empty list
c = []

sol = Solution(problem_type='Circuit Design')


if __name__ == "__main__":
    csp = CSP(x=x, d=d, c=c, verbose=False, csp_problem='circuits', solution=sol,
              use_inference=False,
              use_lcv=True,
              use_degree_heuristic=False,
              use_mrv=False)
    print(csp.backtracking_search())
