import random
from collections import deque
from queue import PriorityQueue
import math
# Directions (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Random movement algorithm (limited moves)
def random_move(start, goal, obstacles, rows, cols):
    path = []
    current = start
    for _ in range(1000):  # Limit to 1000 moves
        direction = random.choice(DIRECTIONS)
        new_pos = (current[0] + direction[0], current[1] + direction[1])
        if (
            0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
            new_pos not in obstacles
        ):
            path.append(direction)
            current = new_pos
        if current == goal:
            return path
    return []

def bfs(start, goal, obstacles, rows, cols):
    q = deque([(start, [])]) # (position, path)
    v = set([start])
    while q is not None:
        cur, path = q.popleft()
        # Path found
        if cur == goal:
            return path
        for dir in DIRECTIONS:
            new = (cur[0] + dir[0], cur[1] + dir[1])
            if (0 <= new[0] < rows and 0 <= new[1] < cols and
                new not in obstacles and new not in v):
                v.add(new)
                q.append((new, path + [dir]))
    # No path found
    return []

def dfs(start, goal, obstacles, rows, cols):
    s = [(start, [])] # (position, path)
    v = set([start])
    while s is not None:
        cur, path = s.pop()
        # Path found
        if cur == goal:
            return path
        for dir in DIRECTIONS:
            new = (cur[0] + dir[0], cur[1] + dir[1])
            if (0 <= new[0] < rows and 0 <= new[1] < cols and
                new not in obstacles and new not in v):
                v.add(new)
                s.append((new, path + [dir]))
    # No path found
    return []

# Recursive DLS for IDS (starts from start node):
def dls(cur, goal, obstacles, rows, cols, depth, v, path):
    # Path found
    if cur == goal:
        return path
    if depth == 0:
        return []
    v.add(cur)
    for dir in DIRECTIONS:
        new = (cur[0] + dir[0], cur[1] + dir[1])
        if (0 <= new[0] < rows and 0 <= new[1] < cols and new not in obstacles and new not in v):
            m = dls(new, goal, obstacles, rows, cols, depth - 1, v, path + [dir])
            if m != []:
                return m
    # No path found
    return []

def ids(start, goal, obstacles, rows, cols):
    depth = 0
    while True:
        v = set()
        m = dls(start, goal, obstacles, rows, cols, depth, v, [])
        if m != []:
            return m
        depth += 1

def ucs(start, goal, obstacles, rows, cols):
    pq = PriorityQueue()
    pq.put((0, start, [])) # (cost, pos, path)
    v = {}
    while not pq.empty():
        cost, cur, path = pq.get()
        # Path found
        if cur == goal:
            return path
        # Skip if cheaper or equal cost path found
        if cur in v and v[cur] <= cost:
            continue
        v[cur] = cost
        for dir in DIRECTIONS:
            new = (cur[0] + dir[0], cur[1] + dir[1])
            if (0 <= new[0] < rows and 0 <= new[1] < cols and new not in obstacles):
                pq.put((cost + 1, new, path + [dir]))
    # No path found
    return []

# Used with Greedy Best-First Search
def manhattan_distance(a, b):
    # |x1 - y1| + |x2 - y2|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_bfs(start, goal, obstacles, rows, cols):
    pq = PriorityQueue()
    pq.put((manhattan_distance(start, goal), start, [])) # ()
    v = set()
    while not pq.empty():
        f, cur, path = pq.get()
        # Path found
        if cur == goal:
            return path
        if cur in v:
            continue
        v.add(cur)
        for dir in DIRECTIONS:
            new = (cur[0] + dir[0], cur[1] + dir[1])
            if (0 <= new[0] < rows and 0 <= new[1] < cols and new not in obstacles and new not in v):
                pq.put((manhattan_distance(new, goal), new, path + [dir]))
    # No path found
    return []

# Used with A* Search
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Variant of Euclidean Distance but with a Sin component
# Not optimal, or efficient
def my_heuristic(pos, goal):
    return euclidean_distance(pos, goal) + 2 * math.sin(0.5 * pos[0])

# Higher the weight, the lower number of paths checked and
# goal is reached faster (over a longer time period)
def weighted_euclidean(pos, goal, weight=5):
    dx, dy = abs(pos[0] - goal[0]), abs(pos[1] - goal[1])
    return weight * math.sqrt(dx ** 2 + dy ** 2)

def astar(start, goal, obstacles, rows, cols, heuristic=weighted_euclidean):
    pq = PriorityQueue()
    pq.put((0, 0, start, []))  # (Heuristic, Cost, Position, Path)
    v = {}
    while not pq.empty():
        f, g, cur, path = pq.get()
        # Path found
        if cur == goal:
            return path
        # Skip if cheaper or equal cost path found
        if cur in v and v[cur] <= g:
            continue
        v[cur] = g
        for dir in DIRECTIONS:
            new = (cur[0] + dir[0], cur[1] + dir[1])
            if (0 <= new[0] < rows and 0 <= new[1] < cols and
                new not in obstacles):
                gnew = g + 1
                f = gnew + heuristic(new, goal)
                pq.put((f, gnew, new, path + [dir]))
    # No path found
    return []