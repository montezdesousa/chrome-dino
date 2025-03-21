import math
import random

import numpy as np


def generate_obstacle_time(current_lambda):
    """Generate the time for the next obstacle using an exponential distribution."""
    return max(random.expovariate(current_lambda), 1.0)


def generate_game_acceleration(elapsed_time):
    """Gera aceleração lognormal progressiva ao longo do tempo, entre 0.02 e 0.025."""
    mean = np.log(0.0225) + 0.00005 * elapsed_time
    sigma = 0.05 + 0.0001 * elapsed_time
    acceleration = np.random.lognormal(mean, sigma)
    return max(0.015, min(acceleration, 0.05))


def generate_cloud_time():
    """Generate the time for the next cloud."""
    return abs(random.gauss(5, 2))


def generate_select_obstacle(obstacle_choices: list):
    """Select an obstacle based on specified probabilities."""
    return random.choices(obstacle_choices, weights=[0.6, 0.4], k=1)[0]


def generate_num_trees(sprite_max_elements: int):
    """Get the number of trees to display."""
    return random.randint(1, sprite_max_elements)


def generate_cloud_height(height):
    """Returns a random vertical position for the cloud."""
    return random.randint(0, height // 2)
