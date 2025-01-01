import pygame
import numpy as np

class Environment:
    def __init__(self, num_tasks, num_students):
        self.num_tasks = num_tasks
        self.num_students = num_students
        self.task_durations = np.random.randint(1, 2, size=num_tasks)
        self.task_priorities = np.random.randint(1, 6, size=num_tasks)
        self.student_efficiencies = np.random.uniform(0.5, 1.5, size=num_students)

    def generate_assignments(self):
        return [np.random.randint(0, self.num_students, size=self.num_tasks) for _ in range(50)]

    def draw_grid(self, screen, font, task_assignments):
        screen.fill((245, 245, 245))  # Background color

        cell_size = 80
        margin_left = 150
        margin_top = 100
        color_map = [(0, 0, 255 - i * 25) for i in range(10)]  # Gradient for durations

        for col in range(self.num_tasks):
            task_text = font.render(f"Task {col + 1}", True, (0, 0, 0))
            screen.blit(task_text, (margin_left + col * cell_size + 10, margin_top - 30))

        for row in range(self.num_students):
            efficiency_text = font.render(f"student {row}: {self.student_efficiencies[row]:.2f}", True, (0, 0, 0))
            screen.blit(efficiency_text, (10, margin_top + row * cell_size + 10))

            for col in range(self.num_tasks):
                assigned_student = task_assignments[col]
                color = color_map[self.task_durations[col] - 1] if assigned_student == row else (200, 200, 200)

                cell_rect = pygame.Rect(margin_left + col * cell_size, margin_top + row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

                if assigned_student == row:
                    priority_text = font.render(f"P{self.task_priorities[col]}", True, (255, 255, 255))
                    duration_text = font.render(f"{self.task_durations[col]}h", True, (255, 255, 255))
                    screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 5))
                    screen.blit(duration_text, (cell_rect.x + 5, cell_rect.y + 30))
