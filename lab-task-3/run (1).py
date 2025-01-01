import pygame
from agent import Agent
from environment import Environment
import numpy as np
import random

pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Task Assignment Optimization")
font = pygame.font.Font(None, 24)

num_tasks = 10
num_students = 5
environment = Environment(num_tasks, num_students)
task_assignments = environment.generate_assignments()

agents = [Agent(id=i, efficiency=environment.student_efficiencies[i]) for i in range(num_students)]

population_size = 50
mutation_rate = 0.1
n_generations = 100
generation_delay = 1000  # Reduced for smoother visualization

def fitness(individual):
    student_times = np.zeros(num_students)
    for task, student in enumerate(individual):
        student_times[student] += environment.task_durations[task] / agents[student].efficiency * environment.task_priorities[task]
    total_time = np.max(student_times)
    workload_balance = np.std(student_times)
    return total_time + workload_balance

def selection(population):
    return sorted(population, key=fitness)[:population_size // 2]

def crossover(parent1, parent2):
    point = random.randint(1, num_tasks - 1)
    return np.concatenate([parent1[:point], parent2[point:]])

def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, num_students - 1)
    return individual

population = environment.generate_assignments()
best_solution = None
best_fitness = float('inf')
max_fitness_achieved = float('inf')
generation_count = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    selected = selection(population)
    next_generation = []
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        next_generation.append(mutate(child))

    population = next_generation
    current_best = min(population, key=fitness)
    current_fitness = fitness(current_best)
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        best_solution = current_best

    environment.draw_grid(screen, font, current_best)
    max_fitness_achieved = min(max_fitness_achieved, current_fitness)

    generation_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
    fitness_text = font.render(f"Best Fitness: {best_fitness:.2f}", True, (0, 0, 0))
    max_fitness_text = font.render(f"Max Fitness Achieved: {max_fitness_achieved:.2f}", True, (0, 0, 0))
    screen.blit(max_fitness_text, (SCREEN_WIDTH - 300, 500))
    screen.blit(generation_text, (SCREEN_WIDTH - 200, 20))
    screen.blit(fitness_text, (SCREEN_WIDTH - 200, 50))

    pygame.display.flip()
    pygame.time.delay(generation_delay)

    generation_count += 1
    if generation_count >= n_generations:
        break

pygame.quit()
