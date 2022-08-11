from logging import raiseExceptions
from node import Node
import re
import sys

# init global variables
X_SHAPE = Y_SHAPE = 0
queue = []
visited = []
mode = ""
expanded_nodes = 0
fifo_count = 0


def expand(node):
    """
    input: node 
    output: list of unvisited children nodes
    """
    childs = []
    counter = 0
    visited.append(node.state)
    for action in actions:
        child = perform_action(node, action)
        if (child.state not in visited):
            child.set_insert_time(fifo_count+counter)
            childs.append(child)
            counter += 1

    return childs


def is_dirt(element):
    """
    input: one field in nxm grid
    output: number of dirt if dirt is on field, None else
    """
    dirt = re.findall(r'\d+', element)
    if (dirt):
        return dirt[0]
    else:
        return None


def get_manhattan_dist(state, x, y, a2=False):
    """
    input: state, position of cleaner 
    output: manhattan distance to closest dirt
    """
    # used for A*1
    distances = []
    for x_idx, row in enumerate(state):
        for y_idx, field in enumerate(row):
            if is_dirt(field):
                dist = abs(x_idx-x)+abs(y-y_idx)
                distances.append(dist)
    if (a2):
        return sum(distances)
    return min(distances)


def get_dirt_sum(state):
    """
    input: state
    output: sum of dirt in that state (a*2 heuristics)
    """
    sum_dirt = 0
    for row in state:
        for field in row:
            dirt = is_dirt(field)
            if (dirt):
                sum_dirt += int(dirt)

    return sum_dirt


def perform_action(node, action):
    """
    input: node, action
    output: node that contains state after performing action
    """
    node_values = node.copy()
    state = node_values.state
    x, y = find_cleaner(state)
    x_old, y_old = x, y
    if (action == "up"):
        x -= 1
    elif (action == "down"):
        x += 1
    elif (action == "left"):
        y -= 1
    elif (action == "right"):
        y += 1

    if (x > X_SHAPE or x < 0 or y > Y_SHAPE):
        x, y = x_old, y_old

    if (state[x][y] == 'j'):
        x += (x-x_old)
        y += (y-y_old)

    if (x > X_SHAPE or x < 0 or y > Y_SHAPE or y < 0 or state[x][y] == 'x'):
        x, y = x_old, y_old

    if (action == "suck"):
        old_dirt = is_dirt(state[x][y])
        if old_dirt:
            dirt = str(int(old_dirt)-1) if int(old_dirt) > 1 else ''
            state[x][y] = state[x][y].replace(old_dirt, dirt)
    else:
        old_dirt = is_dirt(state[x_old][y_old])
        if (old_dirt):
            state[x_old][y_old] = old_dirt
        else:
            state[x_old][y_old] = " "

        dirt = is_dirt(state[x][y])
        if (dirt):
            state[x][y] = "c"+dirt
        else:
            state[x][y] = "c"

    path = node_values.path
    path.append(action)

    cost = node_values.cost
    cost += costs[action]

    if (mode == "a*1" or mode == "gs"):
        dist = get_manhattan_dist(node.state, x, y)
    elif (mode == "a*2"):
        dist = get_manhattan_dist(node.state, x, y, True)
    else:
        dist = 0

    return Node(state, path, cost, dist)


def find_cleaner(state):
    """
    input: state
    output: x,y, coordinates of cleaner
    """
    c = 0
    for l in state:
        idx = [i for i, s in enumerate(l) if 'c' in s]
        try:
            return c, idx[0]
        except:
            c += 1


def is_goal(node):
    """
    input: node
    output: True if its goal state, i.e. if no dirt is in grid, else false
    """
    for l in node.state:
        if any(re.findall(r'\d+', s) for s in l):
            return False
    return True


def split(string):
    """
    input: string 
    output: split word into char
    """
    return [char for char in string]


"""
def sortPrio(el):
    
    val = 5
    for a in actions:
        if el == a:
            return val 
        val-=1
"""


def emulate_game(start_state, node):
    """
    input: state_state, node with final state 
    prints path from start_state to that node
    Can be used to visualize calculated game path
    """
    final_node = node.copy()
    path = final_node.path
    num_actions = len(path)
    current_state = start_state
    while (path):
        action = path.pop(0)
        if action in actions:
            current_state = perform_action(current_state, action)
        print(current_state)
    print(f"Game finished after {num_actions} moves")


if __name__ == "__main__":

    # read mode and init file path from command line arguments
    mode = sys.argv[1].lower()
    init_file = sys.argv[2].lower()

    # convert init file to initial state
    with open(init_file) as file:
        state = list(map(split, [line.replace('\n', '') for line in file]))

    # define shape of state space
    X_SHAPE = len(state)-1
    Y_SHAPE = len(state[0])-1

    # define actions and costs
    actions = ["suck", "left", "right", "down", "up"]
    costs = {
        "left": 1,
        "right": 1,
        "up": 2,
        "down": 2,
        "suck": 5
    }

    # append initial state to queue
    queue.append(Node(state))

    # main loop
    while (queue):

        # take element from fridge
        if (mode == "dfs"):
            # takes newest element (lifo)
            node = queue.pop()
        elif(mode == "bfs"):
            # takes oldest element (fifo)
            node = queue.pop(0)
        elif(mode == "ucs"):
            # takes element with lowest cost, if equal insertion order is used as tie breaker
            queue.sort(key=lambda x: (x.cost, x.insert_time), reverse=True)
            node = queue.pop()
        elif(mode == "gs"):
            # take element with lowest manhattan
            queue.sort(key=lambda x: (x.h, x.insert_time), reverse=True)
            node = queue.pop()
        elif(mode == "a*1" or mode == "a*2"):
            # takes element with lowest cost + h, if equal insertion order is used as tie breaker
            queue.sort(key=lambda x: (x.cost+x.h, x.insert_time), reverse=True)
            node = queue.pop()
        else:
            raiseExceptions("No valid method specified")

        # if state is goal terminate
        if is_goal(node):
            break

        # expand node, to find all unvisited children of state
        if (node.state not in visited):
            expanded_nodes += 1
            childs = expand(node)

            # add child nodes to queue
            queue.extend(childs)

            # increase counter, which is used to track insertion order
            fifo_count += len(childs)

    print(f"number of expanded nodes: {expanded_nodes}")
    print(f"path: {node.path[1:]}")
    print(f"cost of the solution: {node.cost}")
    if (mode == "a*2"):
        x, y = find_cleaner(state)
        print(f"H(initial_state): {get_manhattan_dist(state,x,y,True)} \n")
