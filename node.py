from copy import deepcopy


class Node:
    def __init__(self, state, path=['S'], cost=0, h=0, i=0) -> None:
        
        """
        state: current state
        path: actions that lead from start state to current state
        cost: accumulated cost along path
        h: heuristic value
        insert_time: integer that specifies insert time 
        """

        self.state = state 
        self.path = path
        self.cost = cost
        self.h = h
        self.insert_time = i

    
    def __repr__(self):
        final = ''
        for row in self.state:
             final+=(''.join(map(str, row))+"\n")
        
        return final

    def copy(self):
        return deepcopy(self)

    def set_insert_time(self, time):
        self.insert_time=time





    