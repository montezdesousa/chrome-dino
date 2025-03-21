import pygame
import time

from constants import BLACK, DEVELOPMENT, GREY, INITIAL_VEL, screen
from elements import Cloud, Floor, Dino, BigTree, Obstacle, SmallTree, GameOver, Restart
from utils import draw_grid
from random_variables import (
    generate_cloud_time,
    generate_game_acceleration,
    generate_obstacle_time,
    generate_select_obstacle,
    generate_select_obstacle,
)

# Initial game parameters
INITIAL_LAMBDA = 0.5  # Initial obstacle spawn rate (~1 every 2s)
MAX_LAMBDA = 5  # Maximum spawn rate (~1 every 0.2s)

def check_collision(dino: Dino, obstacle: Obstacle, speed: int) -> bool:
    """Detects if the dino collides with an obstacle."""

    radius = int(dino.frames[dino.current_frame].get_width() * 0.5)
    center_x = dino.x + dino.frames[dino.current_frame].get_width() // 2
    center_y = dino.y - dino.height // 2

    if DEVELOPMENT:
        pygame.draw.circle(screen, BLACK, (center_x, center_y), radius, 1)

    # Adjustment for collision accuracy
    if (
        dino.x <= obstacle.x + obstacle.width
        and dino.x + dino.frames[dino.current_frame].get_width() >= obstacle.x
    ):
        adjustment_x = 0
        adjustment_y = 0
    else:
        adjustment_x = 0
        adjustment_y = 0

    return pygame.Rect(obstacle.get_next_rect()).collidepoint(
        center_x + adjustment_x, center_y + adjustment_y
    )


def game():
    """Main game loop."""
    running = True
    is_game_over = False
    obstacle_choices = [SmallTree, BigTree]
    active_obstacles = []
    active_clouds = []

    # Initial game parameters
    game_speed = INITIAL_VEL
    start_time = time.time()
    next_obstacle_time = time.time() + generate_obstacle_time(INITIAL_LAMBDA) * 0.1
    next_cloud_time = time.time() + generate_cloud_time()

    floor = Floor(speed=game_speed)
    dino = Dino()
    game_over = GameOver()
    restart = Restart()

    clock = pygame.time.Clock()

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Increase difficulty over time by increasing lambda over time
        current_lambda = INITIAL_LAMBDA + (MAX_LAMBDA - INITIAL_LAMBDA) * (elapsed_time / 60)
        current_lambda = min(current_lambda, MAX_LAMBDA)  # Cap at MAX_LAMBDA
        game_speed += generate_game_acceleration(elapsed_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if is_game_over:
                        # Restart the game
                        is_game_over = False
                        dino = Dino()
                        active_obstacles = []
                        active_clouds = []
                        game_speed = INITIAL_VEL
                        start_time = time.time()
                        next_obstacle_time = current_time + generate_obstacle_time(
                            INITIAL_LAMBDA
                        )
                        next_cloud_time = current_time + generate_cloud_time()
                    else:
                        dino.jump()

        screen.fill(GREY)
        if DEVELOPMENT:
            draw_grid()

        if not is_game_over:
            floor.update()
            dino.update()

            if current_time >= next_obstacle_time:
                # Add a new obstacle
                active_obstacles.append(
                    generate_select_obstacle(obstacle_choices)(speed=game_speed)
                )
                next_obstacle_time = current_time + generate_obstacle_time(
                    current_lambda
                )

            if current_time >= next_cloud_time:
                # Add a new cloud
                active_clouds.append(Cloud(speed=game_speed))
                next_cloud_time = current_time + generate_cloud_time()

            # Update all active obstacles
            for obstacle in active_obstacles[:]:
                obstacle.update()
                if check_collision(dino, obstacle, game_speed):
                    is_game_over = True

            # Remove obstacles that have moved off the screen
            active_obstacles = [
                obstacle
                for obstacle in active_obstacles
                if obstacle.x + obstacle.image.get_width() > 0
            ]

            for cloud in active_clouds[:]:
                cloud.update()
                if cloud.x + cloud.image.get_width() < 0:
                    active_clouds.remove(cloud)

        floor.draw()
        dino.draw()

        # Draw all obstacles
        for obstacle in active_obstacles:
            obstacle.draw()

        for cloud in active_clouds:
            cloud.draw()

        if is_game_over:
            game_over.draw()
            restart.draw()
            dino.update(is_game_over)

        pygame.display.flip()
        clock.tick(game_speed)

    pygame.quit()


if __name__ == "__main__":
    game()
