import sys
from collections import deque
import heapq


def parse(floor):
    with open(floor, encoding='utf-16') as f:
        columns = int(f.readline())
        rows=int(f.readline())
        dirty = set()
        walls = set()

        for y in range(rows-1, -1, -1):
            row = f.readline()
            x = 0
            for x, space in enumerate(row.strip()):
                if space == '*':
                    dirty.add((x,y))
                elif space == '#':
                    walls.add((x,y))
                elif space == '@':
                    location = (x,y)
        return(columns,rows,dirty,walls,location)  

def output(came_from, endstate):
    path = []
    step = came_from[endstate]
    while step[0] is not None:
        path.insert(0, step[1])
        step = came_from[step[0]]
    for s in path:
        print(s)

#state: ((x,y), dirtyCells[(x,y), (x,y),...])
def ucs (state, xMax, yMax, walls):
    # visited = set()
    # visited.add(state)
    q = []
    heapq.heappush(q, (0, state)) #(cost, state)
    came_from = {}
    came_from[state] = (None, None)
    state_cost = {}
    state_cost[state] = 0
    direction = ['N','S','E','W']
    gen = 0
    exp = 0

    while q:
        cost, curr = heapq.heappop(q)
        exp += 1
        if curr[0] in curr[1]:
            new_dirty = frozenset(curr[1] - {curr[0]})
            new_state = (curr[0], new_dirty)
            new_cost = cost + 1
            if new_state not in state_cost or new_cost < state_cost[new_state]:
                state_cost[new_state] = new_cost
                heapq.heappush(q, (new_cost, new_state))
                gen += 1
                came_from[new_state] = (curr, 'V')
                if len(new_dirty) == 0:
                    output(came_from, new_state)
                    print(str(gen) + " nodes generated")
                    print(str(exp) + " nodes expanded")
                    return
            continue
        n = move(curr, 0, 1, xMax, yMax, walls)
        s = move(curr, 0, -1, xMax, yMax, walls)
        e = move(curr, 1, 0, xMax, yMax, walls)
        w = move(curr, -1, 0, xMax, yMax, walls)
        for new_state, label in zip([n,s,e,w], direction):
            if new_state is not None:
                new_cost = cost + 1
                if new_state not in state_cost or new_cost < state_cost[new_state]:
                    gen += 1
                    state_cost[new_state] = new_cost
                    heapq.heappush(q, (new_cost, new_state))
                    came_from[new_state] = (curr, label)

def dfs (state, xMax, yMax, walls):
    stack = []
    stack.append(state)
    visited = set()
    visited.add(state)
    came_from = {}
    came_from[state] = (None, None)
    direction = ['N','S','E','W']
    gen = 0
    exp = 0

    while stack:
        curr = stack.pop()
        exp += 1
        if curr[0] in curr[1]:
            new_dirty = frozenset(curr[1] - {curr[0]})
            new_state = (curr[0], new_dirty)
            if new_state not in visited:
                visited.add(new_state)
                stack.append(new_state)
                gen += 1
                came_from[new_state] = (curr, 'V')
                if len(new_dirty) == 0:
                    output(came_from, new_state)
                    print(str(gen) + " nodes generated")
                    print(str(exp) + " nodes expanded")
                    return
            continue
        n = move(curr, 0, 1, xMax, yMax, walls)
        s = move(curr, 0, -1, xMax, yMax, walls)
        e = move(curr, 1, 0, xMax, yMax, walls)
        w = move(curr, -1, 0, xMax, yMax, walls)
        for new_state, label in zip([n,s,e,w], direction):
            if new_state is not None and new_state not in visited:
                gen += 1
                visited.add(new_state)
                stack.append(new_state)
                came_from[new_state] = (curr, label)
    return 

def move(oldState, x, y, xMax, yMax, walls):
    # newState = copy.deepcopy(oldState)
    oldPos = oldState[0]
    newPos = (oldPos[0] + x, oldPos[1] + y)
    if not (0 <= newPos[0] < xMax):
        return None
    if not (0 <= newPos[1] < yMax):
        return None
    if newPos in walls:
        return None
    newState = (newPos, oldState[1])
    return newState





if __name__ == "__main__":
    columns,rows,dirty,walls,location=parse(sys.argv[2])
    state = (location, frozenset(dirty))
    search = sys.argv[1]
    if search == "uniform-cost":
        ucs(state, columns, rows, walls)
    elif search == "depth-first":
        dfs(state, columns, rows, walls)
    else:
        print("Unknown search argument")
        