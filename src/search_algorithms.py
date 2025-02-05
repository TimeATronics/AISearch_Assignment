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
    queue = deque([(start, [])])
    visited = set([start])
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for direction in DIRECTIONS:
            new_pos = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                new_pos not in obstacles and new_pos not in visited):
                visited.add(new_pos)
                queue.append((new_pos, path + [direction]))
    return []

def dfs(start, goal, obstacles, rows, cols):
    stack = [(start, [])]
    visited = set([start])
    while stack:
        current, path = stack.pop()
        if current == goal:
            return path
        for direction in DIRECTIONS:
            new_pos = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                new_pos not in obstacles and new_pos not in visited):
                visited.add(new_pos)
                stack.append((new_pos, path + [direction]))
    return []

def ids(start, goal, obstacles, rows, cols):
    def dls(node, depth, visited, path):
        if node == goal:
            return path
        if depth == 0:
            return None
        visited.add(node)
        for direction in DIRECTIONS:
            new_pos = (node[0] + direction[0], node[1] + direction[1])
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                new_pos not in obstacles and new_pos not in visited):
                result = dls(new_pos, depth - 1, visited, path + [direction])
                if result is not None:
                    return result
        return None
    depth = 0
    while True:
        visited = set()
        result = dls(start, depth, visited, [])
        if result is not None:
            return result
        depth += 1

def ucs(start, goal, obstacles, rows, cols):
    pq = PriorityQueue()
    pq.put((0, start, []))
    visited = {}
    while not pq.empty():
        cost, current, path = pq.get()
        if current == goal:
            return path
        if current in visited and visited[current] <= cost:
            continue
        visited[current] = cost
        for direction in DIRECTIONS:
            new_pos = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                new_pos not in obstacles):
                pq.put((cost + 1, new_pos, path + [direction]))
    return []

# Used with Greedy Best-First Search
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_bfs(start, goal, obstacles, rows, cols):
    pq = PriorityQueue()
    pq.put((manhattan_distance(start, goal), start, []))
    visited = set()
    while not pq.empty():
        f, current, path = pq.get()
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction in DIRECTIONS:
            new_pos = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                new_pos not in obstacles and new_pos not in visited):
                pq.put((manhattan_distance(new_pos, goal), new_pos, path + [direction]))
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
    visited = {}
    while not pq.empty():
        f, g, current, path = pq.get()
        if current == goal:
            return path
        if current in visited and visited[current] <= g:
            continue
        visited[current] = g
        for direction in DIRECTIONS:
            new_pos = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and
                new_pos not in obstacles):
                new_g = g + 1
                f = new_g + heuristic(new_pos, goal)
                pq.put((f, new_g, new_pos, path + [direction]))
    return []