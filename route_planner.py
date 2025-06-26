import pygame
import sys
import heapq

# Constants for grid size
GRID_WIDTH, GRID_HEIGHT = 40, 40
GRID_CELL_SIZE = 20  # Size of each cell in pixels

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)  # Brown color for roads

# Map elements
OBSTACLE = 1
ROAD = 2
ACCIDENT = 3

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = GRID_WIDTH * GRID_CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid Map")

# Initialize the grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Traffic conditions map (initially empty)
traffic_map = {}

# Define A* functions
class State:
    def __init__(self, position, goal, g_score=0):
        self.position = position
        self.goal = goal
        self.g_score = g_score

    def f_score(self):
        return self.g_score + self.heuristic()

    def heuristic(self):
        x1, y1 = self.position
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)

    def __lt__(self, other):
        return self.f_score() < other.f_score() or (self.f_score() == other.f_score() and id(self) < id(other))

def get_neighbors(node):
    x, y = node
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < GRID_WIDTH - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < GRID_HEIGHT - 1:
        neighbors.append((x, y + 1))
    return neighbors

def a_star_search(start, goal, traffic_map):
    open_list = []
    heapq.heappush(open_list, (start.f_score(), id(start), start))
    came_from = {}
    g_score = [[float('inf')] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
    g_score[start.position[0]][start.position[1]] = 0

    while open_list:
        _, _, current_state = heapq.heappop(open_list)
        current = current_state.position

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start.position)
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            neighbor_state = State(neighbor, goal, g_score[current[0]][current[1]] + 1)
            tentative_g_score = neighbor_state.g_score

            if grid[neighbor[0]][neighbor[1]] == OBSTACLE:
                continue  # Skip obstacles

            # Consider traffic conditions
            if neighbor in traffic_map:
                tentative_g_score += traffic_map[neighbor]

            if tentative_g_score < g_score[neighbor[0]][neighbor[1]]:
                came_from[neighbor] = current
                g_score[neighbor[0]][neighbor[1]] = tentative_g_score
                heapq.heappush(open_list, (neighbor_state.f_score(), id(neighbor_state), neighbor_state))

    return None  # No path found

# Main loop
running = True
placing_element = ROAD  # Initial element to be placed
start = None
goal = None
path = None
simulation_running = False
user_placing_start = False
start_set = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not simulation_running:
            if event.type == pygame.KEYDOWN:
                # Change the element to be placed
                if event.key == pygame.K_o:
                    placing_element = OBSTACLE
                elif event.key == pygame.K_r:
                    placing_element = ROAD
                elif event.key == pygame.K_a:
                    placing_element = ACCIDENT
                elif event.key == pygame.K_SPACE:
                    if start and goal:
                        path = a_star_search(State(start, goal, 0), goal, traffic_map)
                        simulation_running = True
                        if path:
                            print("Optimal Path:")
                            for node in path:
                                print(node)
                            print("Optimal Path Cost:", len(path) - 1)  # The cost is the number of steps in the path
                        else:
                            print("No path found.")
                elif event.key == pygame.K_s:
                    user_placing_start = True
                    start_set = False
                elif event.key == pygame.K_c:
                    # Reset the simulation
                    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                    start = None
                    goal = None
                    path = None
                    traffic_map = {}
                    simulation_running = False

                elif event.key == pygame.K_w:
                    # Save the map configuration to a file
                    with open("map_configuration.txt", "w") as file:
                        for row in grid:
                            line = " ".join(map(str, row))
                            file.write(line + "\n")

                elif event.key == pygame.K_l:
                    # Load map configuration from a file
                    with open("map_configuration.txt", "r") as file:
                        lines = file.readlines()
                        for y, line in enumerate(lines):
                            elements = line.split()
                            for x, element in enumerate(elements):
                                grid[x][y] = int(element)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x = x // GRID_CELL_SIZE
                grid_y = y // GRID_CELL_SIZE

                if user_placing_start:
                    start = (grid_x, grid_y)
                    user_placing_start = False
                    start_set = True
                else:
                    # Set the grid cell to the selected element
                    grid[grid_x][grid_y] = placing_element

                    if placing_element == ROAD:
                        if not start_set:
                            start = (grid_x, grid_y)
                            start_set = True
                        elif goal is None:
                            goal = (grid_x, grid_y)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == OBSTACLE:
                pygame.draw.rect(screen, BLACK, (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))
            elif grid[x][y] == ROAD:
                pygame.draw.rect(screen, BROWN, (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))  # Use BROWN color for roads
            elif grid[x][y] == ACCIDENT:
                pygame.drawrect(screen, RED, (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

    # Draw the path
    if path:
        for node in path:
            x, y = node
            pygame.draw.rect(screen, GREEN, (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

    # Highlight the start and goal locations
    if start:
        x, y = start
        pygame.draw.rect(screen, (0, 0, 255), (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))
    if goal:
        x, y = goal
        pygame.draw.rect(screen, (255, 165, 0), (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

    # Display simulation status
    if simulation_running:
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 180, 30))
        font = pygame.font.Font(None, 36)
        text = font.render("Simulation Running", True, WHITE)
        screen.blit(text, (20, 15))

    # Display user instructions
    if user_placing_start:
        pygame.draw.rect(screen, (0, 0, 255), (10, 10, 220, 30))
        font = pygame.font.Font(None, 24)
        text = font.render("Click to set starting location", True, WHITE)
        screen.blit(text, (20, 15))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
