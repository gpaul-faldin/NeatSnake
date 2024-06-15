import pygame

class SnakeGameGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.headDirectionFormat = ['up', 'down', 'left', 'right']
        self.visionFormat = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']
        self.clock.tick(60)

    def update_screen(self, snakeBody, snakeHeadDirection, score, foodPosition, snakeVision, map):
        game_section = pygame.Rect(0, 50, 800, 550)
        self.screen.fill((0, 0, 0), game_section)

        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 60))
        vision_text = self.font.render(f"Vision: {snakeVision}", True, (255, 255, 255))
        self.screen.blit(vision_text, (10, 90))
        vision_helper_text = self.font.render(f"Vision helper: ['up', 'down', 'left', 'right', 'u-l', 'u-r', 'd-l', 'd-r']", True, (255, 255, 255))
        self.screen.blit(vision_helper_text, (10, 120))
        head_direction_text = self.font.render(f"Head Direction: {self.headDirectionFormat[snakeHeadDirection]}", True, (255, 255, 255))
        self.screen.blit(head_direction_text, (10, 150))

        # Grid for snake and other game elements
        grid_section = pygame.Rect(0, 200, 800, 400)
        pygame.draw.rect(self.screen, (255, 255, 255), grid_section, 1)

        # Draw the snake body
        for i in range(len(snakeBody)):
            if i == 0:
                head_color = (255, 0, 0) # Orange color for the head
                pygame.draw.rect(self.screen, head_color, pygame.Rect(snakeBody[i][1]*50, snakeBody[i][0]*50 + 150, 50, 50))
            else:
                body_color = (255, 255, 0) # Yellow color for the body
                pygame.draw.rect(self.screen, body_color, pygame.Rect(snakeBody[i][1]*50, snakeBody[i][0]*50 + 150, 50, 50))

        # Draw the food
        food_color = (0, 255, 0) # Green color for the food
        pygame.draw.rect(self.screen, food_color, pygame.Rect(foodPosition[1]*50, foodPosition[0]*50 + 150, 50, 50))

        pygame.display.flip()

    def changeDisplayName(self, name):
        pygame.display.set_caption(name)

    def retrieveCurrentName(self):
        return pygame.display.get_caption()

    def display_top_section(self, simulation_count):
        top_section = pygame.Rect(0, 0, 800, 50)
        self.screen.fill((0, 0, 0), top_section)
        simulation_count_text = self.font.render(f"{simulation_count}", True, (255, 255, 255))
        self.screen.blit(simulation_count_text, (10, 10))

    def reset_screen(self, score, starved, lifetime):
        game_section = pygame.Rect(0, 50, 800, 550)
        self.screen.fill((0, 0, 0), game_section)
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(game_over_text, (350, 250))
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (350, 280))
        if starved:
            starved_text = self.font.render("Snake starved", True, (255, 255, 255))
        else:
            starved_text = self.font.render("Snake collided with wall", True, (255, 255, 255))
        self.screen.blit(starved_text, (350, 310))
        lifetime_text = self.font.render(f"Lifetime: {lifetime} seconds", True, (255, 255, 255))
        self.screen.blit(lifetime_text, (350, 340))
        pygame.display.flip()

    def close(self):
        pygame.quit()
