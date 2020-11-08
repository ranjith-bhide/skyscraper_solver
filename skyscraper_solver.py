import time


# returns Whether the given list "heights" satift the viewing conditions from Left and from Right.
def valid_heights(left: int, right: int, heights: list) -> bool:
    length = len(heights)
    lview = 0
    lmax = 0
    rview = 0
    rmax = 0
    for i in range(length):
        lview += heights[i] > lmax
        lmax = heights[i] * (heights[i] > lmax) + lmax * (heights[i] < lmax)
    for i in range(length - 1, -1, -1):
        rview += heights[i] > rmax
        rmax = heights[i] * (heights[i] > rmax) + rmax * (heights[i] < rmax)
    return (left == lview or left < 1) and (right == rview or right < 1)


# Recursive function to give out all possible combinations of heights satisfying a viewing conditions from
# left and right
def populate_combinations_recurse(length, len_pending, curr_values, left, right):
    combinations = []
    if len_pending == 0 and valid_heights(left, right, curr_values):
        combinations += [curr_values]

    for i in range(1, length + 1, 1):
        if i not in curr_values:
            res = populate_combinations_recurse(length, len_pending - 1, curr_values + [i], left, right)
            if any(res):
                combinations += res
    return combinations


# Returns all possible combinations of heights satisfying a viewing conditions from left and right
# Wrapper for the recursive function.
def get_one_row_solutions(left, right, length):
    return populate_combinations_recurse(length, length, [], left, right)


# Returns all possible combinations of independent solutions for each row for the given set of viewing conditions
# from left and right
def get_all_row_solutions(left, right):
    length = len(left)
    sols = []
    for i in range(length):
        sols.append(get_one_row_solutions(left[i], right[i], length))
        print("Number of possible solutions for row ", i, ":", len(sols[i]))
    return sols


# Returns the combination of independent row solutions that satisfy the given set of viewing conditions
# from top and bottom
# Recursive function
def get_full_sol_rec(selected_rs, remaining_rs, top, bottom):
    sols = []
    length = len(remaining_rs)
    cols = []

    if len(selected_rs) > 1:
        cols = list(map(list, zip(*selected_rs)))
        for i in cols:
            if len(set(i)) != len(i):
                return sols

    # if not any(remaining_rs):
    if length == 0:
        for i in range(len(cols)):
            if not valid_heights(top[i], bottom[i], cols[i]):
                return sols
        sols.append(selected_rs)
    else:
        for i in remaining_rs[0]:
            res = get_full_sol_rec(selected_rs + [i], remaining_rs[1:], top, bottom)
            if any(res):
                sols += res
                break
    return sols


# Returns the combination of independent row solutions that satisfy the given set of viewing conditions
# from top and bottom
# Wrapper for the recursive function.
def get_full_sol(row_sols, top, bottom):
    return get_full_sol_rec([], row_sols, top, bottom)


# valid upto gridsize 9x9
def pretty_print_solution(top, bottom, left, right, sol):
    print(" ", end="")
    for i in top:
        print("  ", i, end="")
    print("")

    for i in range(len(left)):
        print("  ", end="")
        for j in range(len(left)):
            print("+---", end="")
        print("+")

        print(left[i], end="")
        for j in range(len(left)):
            print(" |", sol[0][i][j], end="")
        print(" |", right[i])
        # print("")
    print("  ", end="")
    for j in range(len(left)):
        print("+---", end="")
    print("+")

    print(" ", end="")
    for i in bottom:
        print("  ", i, end="")
    print("")

def print_skyscraper_solution(top, bottom, left, right):
    print(top)
    print(bottom)
    print(left)
    print(right)
    row_sols = get_all_row_solutions(left, right)
    sols = get_full_sol(row_sols, top, bottom)
    print(sols)
    pretty_print_solution(top, bottom, left, right,sols)


tp = [3, 2, 2, 3, 2, 1]
bt = [3, 4, 2, 2, 1, 5]
lf = [4, 2, 2, 1, 2, 3]
rt = [1, 2, 3, 3, 2, 2]
# tp = [0, 0, 2, 1, 0]
# bt = [2, 0, 1, 0, 0]
# lf = [4, 4, 0, 0, 0]
# rt = [0, 0, 5, 0, 0]

start_time = time.time()
print_skyscraper_solution(tp, bt, lf, rt)
print("--- %s seconds ---" % (time.time() - start_time))
