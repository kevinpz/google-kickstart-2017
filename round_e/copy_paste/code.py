import time
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
logger.addHandler(ch)

# class to store intermediate strings with the minimal distance (action) to reach each of them
class Part():
    def __init__(self, my_string, dist, buff_list):
        self.my_string = my_string
        self.dist = dist
        self.buff_list = buff_list

    def __str__(self):
        return "String: {} Dist: {} Buff List: {}".format(self.my_string, self.dist, self.buff_list)

# read the input from the files
def read_input(input_file):
    source_val = []
    with open('data/' + input_file + '.in', 'r') as file:
        for line in file:
            source_val.append(line.strip())

    input_list = source_val[1:]
    return input_list

# write the output to the file
def write_output(res_list, input_file):
    size = len(res_list)
    with open('data/' + input_file + '.out', 'w+') as file:
        for i in range(size):
            file.write("Case #{}: {}\n".format(i + 1, res_list[i]))

# find the minimum distance for a giving 
def find_min_dist(i, cur_string, dist_list):
    # list of all possible solutions
    sol_list = []
    logger.debug(i)
    # get the buffer store in the previous string
    buff_list = dist_list[i -1].buff_list
    val = dist_list[i - 1].dist + 1
    # append the solution from ths string with one less char and type a new one
    sol_list.append(Part(cur_string, val, buff_list))

    # now we will check if we can have better distance using a copy / past move
    for j in range(2, i // 2 + 1):
        rev_string = cur_string[-j:]
        # id the current substring (from end) already exists, it means we can copy / paste it
        if cur_string.count(rev_string) > 1:
            # get the previous distance
            val = dist_list[i - j].dist + 1
            # and check of the string is already in the buffer, else add a copy action
            if rev_string not in dist_list[i - j].buff_list:
                val += 1
            buff = rev_string
            # add the solution
            sol_list.append(Part(cur_string, val, [buff]))

    # sort the list to have the solution with the fewer distance in the beginning 
    sol_list.sort(key=lambda x: x.dist)
    best_sol = sol_list[0]
    min_val = best_sol.dist
    # get all the possible buffer to arrive with the min dist
    buff_list = [my_buff for sol in sol_list if sol.dist == min_val for my_buff in sol.buff_list]
    best_sol.buff_list = buff_list

    dist_list.append(best_sol)

# calculate the min number of action to write a string
def solve_pb(target_string):
    cur_string = ""
    size = len(target_string)
    dist_list = []
    dist_list.append(Part("", 0, []))
    # for a substring starting with size 1 to the full string
    for i in range(1, size + 1):
            cur_string = target_string[:i]
            # find the minimum distance to write the current string
            find_min_dist(i, cur_string, dist_list)

    for d in dist_list:
        logger.debug(d)

    # return the distance for the full string
    return dist_list[-1].dist

# for each case
def answer(input_file):
    res_list = []
    input_list = read_input(input_file)
    # for each string in the file
    for target_string in input_list:
        res = solve_pb(target_string)
        res_list.append(res)
        logger.debug("")
    logger.info(res_list)
    write_output(res_list, input_file)

# try each case
start=datetime.now()
answer("sample")
answer("A-small-practice")
answer("A-large-practice")
logger.warning('Total time: ' + str(datetime.now()-start))

