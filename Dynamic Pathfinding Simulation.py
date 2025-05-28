import pygame
import sys
import random
import heapq
import time

# Constants
GRID_WIDTH, GRID_HEIGHT = 40, 20
CELL_SIZE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + 60  # extra for info panel
BG_COLOR = (30, 30, 30)
GRID_COLOR_1 = (40, 40, 40)
GRID_COLOR_2 = (50, 50, 50)
OBSTACLE_COLOR = (139, 69, 19)  # brown crates
ROBOT_COLOR = (50, 205, 50)     # lime green
GOAL_COLOR = (220, 20, 60)      # crimson
PATH_COLOR = (65, 105, 225)     # royal blue
TRAIL_COLOR = (100, 149, 237)   # cornflower blue
TEXT_COLOR = (230, 230, 230)
WARNING_COLOR = (255, 80, 80)

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Consolas", 18)
BIG_FONT = pygame.font.SysFont("Consolas", 28, bold=True)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dynamic A* Pathfinding - No Stuck Guarantee")
clock = pygame.time.Clock()

grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

start_point = (0, 0)
end_point = (GRID_WIDTH - 1, GRID_HEIGHT - 1)
robot_pos = list(start_point)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(node):
    x, y = node
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            if grid[nx][ny] == 0:
                yield (nx, ny)

def a_star(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break
        for nxt in neighbors(current):
            new_cost = cost_so_far[current] + 1
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(goal, nxt)
                heapq.heappush(frontier, (priority, nxt))
                came_from[nxt] = current

    current = goal
    path = []
    while current != start:
        if current not in came_from:
            return []  # no path
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GRID_COLOR_1 if (x+y) % 2 == 0 else GRID_COLOR_2
            pygame.draw.rect(screen, color, rect)

            if grid[x][y] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, rect.inflate(-4, -4))
                pygame.draw.line(screen, (160,82,45), (rect.left+4, rect.top+4), (rect.right-4, rect.top+4), 2)
                pygame.draw.line(screen, (160,82,45), (rect.left+4, rect.top+4), (rect.left+4, rect.bottom-4), 2)

def draw_path(path):
    for px, py in path:
        rect = pygame.Rect(px*CELL_SIZE, py*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, PATH_COLOR, rect.inflate(-8, -8), border_radius=4)

def draw_trail(trail):
    for (tx, ty) in trail:
        rect = pygame.Rect(tx*CELL_SIZE, ty*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, TRAIL_COLOR, rect.inflate(-12, -12), border_radius=3)

def draw_robot(pos):
    x = pos[0]*CELL_SIZE + CELL_SIZE//2
    y = pos[1]*CELL_SIZE + CELL_SIZE//2
    for radius, alpha in [(14, 50), (10, 80), (6, 150)]:
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (ROBOT_COLOR[0], ROBOT_COLOR[1], ROBOT_COLOR[2], alpha), (radius, radius), radius)
        screen.blit(s, (x - radius, y - radius))
    pygame.draw.circle(screen, ROBOT_COLOR, (x, y), CELL_SIZE//3)

def draw_goal():
    x = end_point[0]*CELL_SIZE + CELL_SIZE//2
    y = end_point[1]*CELL_SIZE + CELL_SIZE//2
    for radius, alpha in [(16, 60), (12, 100), (8, 200)]:
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (GOAL_COLOR[0], GOAL_COLOR[1], GOAL_COLOR[2], alpha), (radius, radius), radius)
        screen.blit(s, (x - radius, y - radius))
    pygame.draw.circle(screen, GOAL_COLOR, (x, y), CELL_SIZE//3)

def draw_info_panel(steps_taken, obstacles_added, elapsed_time):
    panel_rect = pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
    pygame.draw.rect(screen, (20, 20, 20), panel_rect)
    pygame.draw.line(screen, (70, 70, 70), (0, SCREEN_HEIGHT - 60), (SCREEN_WIDTH, SCREEN_HEIGHT - 60), 2)

    texts = [
        f"Steps Taken: {steps_taken}",
        f"Obstacles Added: {obstacles_added}",
        f"Elapsed Time: {elapsed_time:.1f}s",
        "Press [X] to Quit"
    ]
    for i, text in enumerate(texts):
        render = FONT.render(text, True, TEXT_COLOR)
        screen.blit(render, (10 + i*220, SCREEN_HEIGHT - 45))

def add_random_obstacles(num=150):
    added = 0
    while added < num:
        x = random.randint(0, GRID_WIDTH-1)
        y = random.randint(0, GRID_HEIGHT-1)
        if (x, y) != start_point and (x, y) != end_point and grid[x][y] == 0:
            grid[x][y] = 1
            added += 1

def remove_obstacle(pos):
    x, y = pos
    if grid[x][y] == 1:
        grid[x][y] = 0

def main():
    global robot_pos

    add_random_obstacles(num=150)
    path = a_star(tuple(robot_pos), end_point)
    if not path:
        print("No initial path found!")
        pygame.quit()
        sys.exit()

    move_timer = 0
    obstacle_timer = 0
    running = True

    MOVE_INTERVAL = 375
    OBSTACLE_INTERVAL = 2000

    STEPS_PER_MOVE = 1
    steps_taken = 0
    obstacles_added = 150
    start_time = time.time()
    trail = []

    while running:
        dt = clock.tick(60)
        move_timer += dt
        obstacle_timer += dt
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    running = False

        if tuple(robot_pos) == end_point:
            screen.fill(BG_COLOR)
            draw_grid()
            draw_trail(trail)
            draw_goal()
            draw_robot(robot_pos)
            success_msg = BIG_FONT.render("Goal Reached! 🎉", True, (0, 255, 100))
            screen.blit(success_msg, (SCREEN_WIDTH//2 - success_msg.get_width()//2, SCREEN_HEIGHT//2 - 30))
            pygame.display.flip()
            continue

        if move_timer > MOVE_INTERVAL:
            if path:
                for _ in range(STEPS_PER_MOVE):
                    if path:
                        trail.append(tuple(robot_pos))
                        robot_pos[0], robot_pos[1] = path.pop(0)
                        steps_taken += 1
            move_timer = 0

        # Only add obstacles if goal not yet reached
        if obstacle_timer > OBSTACLE_INTERVAL and tuple(robot_pos) != end_point:
            possible_positions = [pos for pos in path if pos != tuple(robot_pos) and pos != end_point]
            if possible_positions:
                ox, oy = random.choice(possible_positions)
                grid[ox][oy] = 1
                obstacles_added += 1
                path = a_star(tuple(robot_pos), end_point)
                if not path:
                    remove_obstacle((ox, oy))
                    obstacles_added -= 1
                    path = a_star(tuple(robot_pos), end_point)
            else:
                while True:
                    ox, oy = random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)
                    if grid[ox][oy] == 0 and (ox, oy) != tuple(robot_pos) and (ox, oy) != end_point:
                        grid[ox][oy] = 1
                        obstacles_added += 1
                        break
                path = a_star(tuple(robot_pos), end_point)

            obstacle_timer = 0

        screen.fill(BG_COLOR)
        draw_grid()
        draw_trail(trail)
        draw_path(path)
        draw_goal()
        draw_robot(robot_pos)
        draw_info_panel(steps_taken, obstacles_added, elapsed_time)

        title_surf = BIG_FONT.render("Dynamic A* Pathfinding Simulation - No Stuck Guarantee", True, PATH_COLOR)
        screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 5))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
