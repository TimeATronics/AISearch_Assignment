import pygame
import random
import time
import sys
import csv
from search_algorithms import *

# Updated: For 2 Players
TWO_PLAYERS = "--two" in sys.argv

# Parse command-line arguments
if len(sys.argv) < 3 or (TWO_PLAYERS and len(sys.argv) < 5):
    print("Usage: python snake.py <level> <search_algorithm> [--two <search_algorithm2>]")
    sys.exit(1)

level = sys.argv[1].lower()
search_algorithm1 = sys.argv[2].lower()
# Updated: For 2 Players
search_algorithm2 = sys.argv[4].lower() if TWO_PLAYERS else None

# Validate level
LEVELS = {"level0": 0, "level1": 5, "level2": 10, "level3": 15}
if level not in LEVELS:
    print("Invalid level! Choose from: level0, level1, level2, level3")
    sys.exit(1)

# Validate search algorithm
ALGORITHMS = {"bfs": bfs, "dfs": dfs, "ucs": ucs, "ids": ids, "a*": astar, "random": random_move, "greedy_bfs": greedy_bfs}
if search_algorithm1 not in ALGORITHMS or (TWO_PLAYERS and search_algorithm2 not in ALGORITHMS):
    print("Invalid search algorithm! Choose from: bfs, dfs, ucs, ids, a*, random, greedy_bfs")
    sys.exit(1)

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 20
WHITE, BLACK, GREEN, RED, GRAY, BLUE = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0), (128, 128, 128), (0, 0, 255)
FONT = pygame.font.Font(None, 36)

# Grid settings
ROWS, COLS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Updated: AI Snakes' starting position
snake1_pos = [ROWS // 4, COLS // 4]
snake2_pos = [ROWS - ROWS // 4, COLS - COLS // 4] if TWO_PLAYERS else None

# Food position
food_pos = None  # Set initially to None

# Timer settings (Originally 30, set to 10 for plotting scores)
TIME_LIMIT = 5
start_time = time.time()

# Setup Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"AI Snake Game ({search_algorithm1.upper()} - {level.upper()})")
clock = pygame.time.Clock()

# Updated: Scores for Players 1 and 2
score1 = 0
score2 = 0 if TWO_PLAYERS else None

# Generate obstacles based on level
obstacles = set()
OBSTACLE_COUNT = (ROWS * COLS * LEVELS[level]) // 100 # % of total grid size
while len(obstacles) < OBSTACLE_COUNT:
    obstacle = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    if obstacle not in (tuple(snake1_pos), tuple(snake2_pos or [])):
        obstacles.add(obstacle)

# Directions (Up, Down, Left, Right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Updated: Metric for evaluation
moves1 = 0
moves2 = 0
food_times = {}
times1 = {}
times2 = {}
food_num = 0
moves_per_goal1 = []
moves_per_goal2 = []

# Fix: Check if new food position after score is valid or an obstacle
def generate_food():
    while True:
        new_food = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if new_food not in obstacles and new_food != tuple(snake1_pos) and (not TWO_PLAYERS or new_food != tuple(snake2_pos)):
            return list(new_food)
food_pos = generate_food()
food_num += 1
food_times[food_num] = time.time()

# Game Over function (Updated to handle 2 players and 2 scores)
def game_over():
    winner = "Player 1" if not TWO_PLAYERS or score1 > score2 else "Player 2" if score2 > score1 else "Draw"
    game_over_surface = FONT.render(f"{winner} Wins!", True, RED)
    screen.blit(game_over_surface, (WIDTH // 3, HEIGHT // 3))
    avg_moves1 = sum(moves_per_goal1) / len(moves_per_goal1) if moves_per_goal1 else 0
    avg_moves2 = sum(moves_per_goal2) / len(moves_per_goal2) if moves_per_goal2 else 0
    # Upon exiting, store the scores to a csv file, used for plotting
    with open('scores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        avg_time1 = sum(list(times1.values()))/len(list(times1.values())) if len(list(times1.values())) > 0 else 0
        avg_time2 = sum(list(times2.values()))/len(list(times2.values())) if len(list(times2.values())) > 0 else 0
        writer.writerow([level, score1, score2, avg_moves1, avg_moves2, avg_time1, avg_time2])
    pygame.display.flip()
    # after 2 seconds we will quit the program
    #time.sleep(2)
    # deactivating pygame library
    pygame.quit()
    # quit the program (using sys.exit() instead of quit())
    sys.exit()

running = True
path1, path2 = [], []

while running:
    screen.fill(BLACK)
    # Timer logic
    elapsed_time = time.time() - start_time
    time_left = max(0, TIME_LIMIT - int(elapsed_time))
    # If time runs out, end game
    if time_left == 0:
        running = False
        game_over()

    if not path1:
        path1 = ALGORITHMS[search_algorithm1](tuple(snake1_pos), tuple(food_pos), obstacles, ROWS, COLS)
    # Updated: For Player 2
    if TWO_PLAYERS and not path2:
        path2 = ALGORITHMS[search_algorithm2](tuple(snake2_pos), tuple(food_pos), obstacles, ROWS, COLS)

    # Updated: Move AI Snake
    if path1:
        move = path1.pop(0)
        moves1 += 1
        snake1_pos[0] += move[0]
        snake1_pos[1] += move[1]
    # Updated: For Player 2
    if TWO_PLAYERS and path2:
        move = path2.pop(0)
        moves2 += 1
        snake2_pos[0] += move[0]
        snake2_pos[1] += move[1]

    # Check if AI hits wall or obstacle (Game Over)
    if tuple(snake1_pos) in obstacles or (TWO_PLAYERS and tuple(snake2_pos) in obstacles):
        running = False
        game_over()

    # Check if AI reaches food (Increase Score, Relocate Food)
    # Updated: Fix for generating valid food positions + metrics for evaluation
    if snake1_pos == food_pos and (not TWO_PLAYERS or snake2_pos != food_pos):
        score1 += 1
        food_num += 1
        food_times[food_num] = time.time()
        times1[food_num] = time.time() - food_times[food_num - 1]
        if food_num > 1:
            moves_per_goal1.append(moves1)  # Store moves used to reach the goal
        moves1 = 0  # Reset move counter
        food_pos = generate_food()
        path1 = []
        if TWO_PLAYERS:
            path2 = []
    # Updated: For Player 2
    if TWO_PLAYERS and snake2_pos == food_pos and snake1_pos != food_pos:
        score2 += 1
        food_num += 1
        food_times[food_num] = time.time()
        times2[food_num] = time.time() - food_times[food_num - 1]
        if food_num > 1:
            moves_per_goal2.append(moves2)
        moves2 = 0
        food_pos = generate_food()
        path1 = []
        path2 = []
    # Case: When both snakes' paths coincide and reach the food at the same time
    # In that case, both receive the point 
    if TWO_PLAYERS and snake1_pos == snake2_pos == food_pos:
        score1 += 1
        score2 += 1
        food_num += 1
        food_times[food_num] = time.time()
        times1[food_num] = time.time() - food_times[food_num - 1]
        times2[food_num] = time.time() - food_times[food_num - 1]
        if food_num > 1:
            moves_per_goal1.append(moves1)
            moves_per_goal2.append(moves2)
        moves1 = 0
        moves2 = 0
        food_pos = generate_food()
        path1 = []
        path2 = []

    # Draw Snake (Player 1)
    pygame.draw.rect(screen, GREEN, (snake1_pos[1] * CELL_SIZE, snake1_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Updated: Draw Snake (Player 2)
    if TWO_PLAYERS:
        pygame.draw.rect(screen, BLUE, (snake2_pos[1] * CELL_SIZE, snake2_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw food
    pygame.draw.rect(screen, RED, (food_pos[1] * CELL_SIZE, food_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, (obs[1] * CELL_SIZE, obs[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Display Timer
    timer_text = FONT.render(f"Time Left: {time_left}s", True, WHITE)
    screen.blit(timer_text, (20, 20))
    
    # Display Score
    score_text1 = FONT.render(f"P1 Score: {score1}", True, WHITE)
    screen.blit(score_text1, (20, 50))
    
    # Updated: For Player 2
    if TWO_PLAYERS:
        score_text2 = FONT.render(f"P2 Score: {score2}", True, WHITE)
        screen.blit(score_text2, (20, 80))

    pygame.display.update()
    # Faster tick for faster gameplay used for plotting
    clock.tick(20)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_over()
pygame.quit()