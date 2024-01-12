import pygame
import sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
paused_surface = title_font.render("Paused", True, Colors.white)
restart_surface = title_font.render("Press R to restart", True, Colors.white)
drop_surface_text = ["Press SPACE", "to drop"]

# Define DROP_KEY
DROP_KEY = pygame.K_SPACE

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

game = Game()
speed_up_factor = 0.050
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, int(250 - (game.score * speed_up_factor)))

PAUSE_KEY = pygame.K_p
RESTART_KEY = pygame.K_r
game.paused = False  # Add this line to initialize the paused attribute

# Initialize high score
high_score = 0

# Add grid_height attribute to Game class
game.grid_height = 20

# Add block attribute to Game class
game.block = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == PAUSE_KEY:
                game.paused = not game.paused
            elif event.key == RESTART_KEY:
                if game.game_over:
                    game.game_over = False
                    game.reset()
                    # Reset high score
                    high_score = 0
            elif not game.game_over and not game.paused:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)  # Pass both arguments here
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == DROP_KEY:
                    # Calculate the number of times to move down
                    if game.block is not None:
                        num_moves = game.grid_height
                        # Move down the block the required number of times
                        for _ in range(num_moves):
                            game.move_down()
                            game.update_score(0, 1)  # Pass both arguments here
                            pygame.time.set_timer(GAME_UPDATE, int(250 - (game.score * speed_up_factor)))
        elif event.type == GAME_UPDATE:
            if not game.game_over:
                if not game.paused:
                    game.move_down()
                    pygame.time.set_timer(GAME_UPDATE, int(250 - (game.score * speed_up_factor)))

    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))
    drop_surface_surface = title_font.render(drop_surface_text[0], True, Colors.white)
    drop_surface_surface2 = title_font.render(drop_surface_text[1], True, Colors.white)
    screen.blit(drop_surface_surface, (320, 450, 150, 30))
    screen.blit(drop_surface_surface2, (350, 480, 150, 30))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                  centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    if not game.game_over:
        game.draw(screen)
    if game.paused:
        screen.blit(paused_surface, (113, 280, 50, 50))
    if game.game_over:
        screen.blit(game_over_surface, (77, 280, 50, 50))
        screen.blit(restart_surface, (45, 350, 50, 50))
        game.paused = False  # Add this line to initialize the paused attribute

        # Update high score
        if game.score > high_score:
            high_score = game.score
        score_value_surface = title_font.render("High Score: " + str(high_score), True, Colors.white)
        screen.blit(score_value_surface, (10, 10, 100, 30))

    pygame.display.update()
    clock.tick(60)
