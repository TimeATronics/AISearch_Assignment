import csv
import matplotlib.pyplot as plt

# Read the CSV file
filename = 'scores.csv'
times_goal_reached_1 = []
times_goal_reached_2 = []
avg_moves_1 = []
avg_moves_2 = []
avg_time_1 = []
avg_time_2 = []

# Read data from CSV
with open(filename, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    #next(csvreader)  # Skip the header
    for row in csvreader:
        times_goal_reached_1.append(int(row[1]))
        times_goal_reached_2.append(int(row[2]) if row[2] else 0)  # Handle empty case
        avg_moves_1.append(float(row[3]))
        avg_moves_2.append(float(row[4]) if row[4] else 0)  # Handle empty case
        avg_time_1.append(float(row[5]))
        avg_time_2.append(float(row[6]) if row[6] else 0)  # Handle empty case

# Default weight
weight = 2

# Check if Player 2 has data (i.e., not all zeros or empty)
player_2_has_data = any(val > 0 for val in times_goal_reached_2)

# Calculate the weighted metric for player 1
weighted_metric_1 = [
    (times_goal_reached_1[i] / times_goal_reached_1[i])**weight / avg_time_1[i] if times_goal_reached_1[i] != 0 else 0
    if not player_2_has_data else
    (times_goal_reached_1[i] / (times_goal_reached_1[i] + times_goal_reached_2[i]))**weight / avg_time_1[i]
    if (times_goal_reached_1[i] + times_goal_reached_2[i]) > 0 else 0  # Avoid division by zero
    for i in range(len(times_goal_reached_1))
]

if player_2_has_data:
    weighted_metric_2 = [
        (times_goal_reached_2[i] / (times_goal_reached_1[i] + times_goal_reached_2[i]))**weight / avg_time_2[i] if times_goal_reached_2[i] != 0 else 0
        if (times_goal_reached_1[i] + times_goal_reached_2[i]) > 0 else 0  # Avoid division by zero
        for i in range(len(times_goal_reached_2))
    ]

# X-axis: iteration count (row index)
iterations = list(range(1, len(times_goal_reached_1) + 1))
if player_2_has_data:
    iterations2 = list(range(1, len(times_goal_reached_2) + 1))

# Plot the first graph for the weighted metric
plt.plot(iterations, weighted_metric_1, label='Player 1 Weighted Metric', marker='o')
if player_2_has_data:
    plt.plot(iterations2, weighted_metric_2, label='Player 2 Weighted Metric', marker='o')
plt.xlabel('Iteration (Row Number)')
plt.ylabel('Weighted Metric for Player')
plt.title('Weighted Metric of Success')
plt.grid(True)
plt.legend()
plt.show()


# Plot the second graph for average moves
plt.plot(iterations, avg_moves_1, label='Player 1 Average Moves', marker='o')

if player_2_has_data:
    plt.plot(iterations2, avg_moves_2, label='Player 2 Average Moves', marker='o')

plt.xlabel('Iteration (Row Number)')
plt.ylabel('Average Moves to Reach Goal')
plt.title('Average Moves to Reach Goal')
plt.grid(True)
plt.legend()
plt.show()

plt.plot(iterations, avg_time_1, label='Player 1 Average Time', marker='o')
if player_2_has_data:
    plt.plot(iterations2, avg_time_2, label='Player 2 Average Time', marker='o')
plt.xlabel('Iteration (Row Number)')
plt.ylabel('Average Time to Reach Goal (seconds)')
plt.title('Average Time to Reach Goal')
plt.grid(True)
plt.legend()
plt.show()

plt.plot(iterations, times_goal_reached_1, label='Player 1 Score', marker='o')
if player_2_has_data:
    plt.plot(iterations2, times_goal_reached_2, label='Player 2 Score', marker='o')
plt.xlabel('Iteration (Row Number)')
plt.ylabel('Score')
plt.title('Scores')
plt.grid(True)
plt.legend()
plt.show()