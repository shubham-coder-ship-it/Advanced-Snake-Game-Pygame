import pygame
import random

# Initialize pygame
pygame.init()
#add the food eat sound
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.mp3")
# Screen settings
WIDTH, HEIGHT = 600, 400
BLOCK = 20
GAME_HEIGHT = HEIGHT - 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
PINK =(255,105,180)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (50, 255, 50)
PINK = (255, 105, 180)

font = pygame.font.SysFont("Arial", 25)
title_font = pygame.font.SysFont("Arial", 40, bold=True)
countdown_font=pygame.font.SysFont("Arial", 100, bold=True)
# Snake
snake = [(100, 80)]
direction = (BLOCK, 0)

# Food
food = (
    random.randrange(20, WIDTH-20, BLOCK),
    random.randrange(80, 240, BLOCK)
)

score = 0
total_score=0
#To read the high score text file
with open("highscore.txt", "r") as file:
    high_score = int(file.read())
    
level=1
last_level = 1
lives=3
paused=False
running = True
new_high_score=False

settings_open = False
sound_on = True
theme=0

settings_btn = pygame.Rect(485, 275, 90, 90)
sound_btn = pygame.Rect(180, 120, 240, 45)
resume_btn = pygame.Rect(180, 180, 240, 50)
exit_game_btn = pygame.Rect(180, 245, 240, 50)

# Draw mobile buttons
def draw_buttons():
    global up_btn, down_btn, left_btn, right_btn

    btn_width = 60
    btn_height = 55

    left_btn = pygame.Rect(30, 310, btn_width, 60)
    right_btn = pygame.Rect(170, 310, btn_width, 60)
    up_btn = pygame.Rect(100, 255, btn_width, btn_height-2)
    down_btn = pygame.Rect(100, 315, btn_width, btn_height)

    pygame.draw.rect(screen, (100,100,100), left_btn)
    pygame.draw.rect(screen, (100,100,100), right_btn)
    pygame.draw.rect(screen, (100,100,100), up_btn)
    pygame.draw.rect(screen, (100,100,100), down_btn)

    screen.blit(font.render("←", True, BLUE), (50, 320))
    screen.blit(font.render("→", True, BLUE), (190, 320))
    screen.blit(font.render("↑", True, BLUE), (120, 260))
    screen.blit(font.render("↓", True, BLUE), (120, 320))
    
    #draw a  setting button
    
    global settings_btn
    
    # Settings button
    
    settings_btn = pygame.Rect(485, 275, 90, 90)
    pygame.draw.rect(screen, (100, 100, 100), settings_btn)

    gear = font.render("Setting", True, PINK)
    screen.blit(gear, gear.get_rect(center=settings_btn.center))
    
    
    
# ---------- START MENU ----------

play_btn = pygame.Rect(180, 160, 240, 50)

menu_settings_btn = pygame.Rect(180, 220, 240, 50)

exit_btn = pygame.Rect(180, 280, 240, 50)

menu = True
menu_settings = False

while menu:
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (BLOCK, BLOCK, WIDTH, GAME_HEIGHT), 3)

    title = title_font.render("SNAKE GAME", True, GREEN)
    title_rect= title.get_rect(center=(WIDTH //2,55))
    screen.blit(title, title_rect)
    high_label = font.render("HIGH SCORE", True, WHITE)
    high_label_rect = high_label.get_rect(center=(WIDTH // 2, 105))
    screen.blit(high_label, high_label_rect)
    
    high_value = font.render(str(high_score), True, RED)
    high_value_rect = high_value.get_rect(center=(WIDTH // 2, 140))
    screen.blit(high_value, high_value_rect)

    # PLAY BUTTON
    pygame.draw.rect(screen, (100,100,100), play_btn)
    play_text = font.render("PLAY", True, WHITE)
    screen.blit(play_text, play_text.get_rect(center=play_btn.center))

    # SETTINGS BUTTON
    pygame.draw.rect(screen, (100,100,100), menu_settings_btn)
    settings_text = font.render("SETTINGS", True, WHITE)
    screen.blit(settings_text,
            settings_text.get_rect(center=menu_settings_btn.center))

    # EXIT BUTTON
    pygame.draw.rect(screen, (100,100,100), exit_btn)
    exit_text = font.render("EXIT", True, WHITE)
    screen.blit(exit_text, exit_text.get_rect(center=exit_btn.center))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not menu_settings and play_btn.collidepoint(event.pos):
                menu = False

                # Countdown
                for text in ["3", "2", "1", "GO!"]:
                    screen.fill(BLACK)
                    pygame.draw.rect(screen, WHITE, (10, 10, WIDTH-20, GAME_HEIGHT-10), 3)
                    countdown = countdown_font.render(text, True, ORANGE)
                    countdown_rect = countdown.get_rect(center=(WIDTH//2-20, GAME_HEIGHT//2))
                    screen.blit(countdown, countdown_rect)
                    pygame.display.flip()
                    pygame.time.wait(1000)

            elif not menu_settings and menu_settings_btn.collidepoint(event.pos):
                menu_settings = True

            elif menu_settings and theme_btn.collidepoint(event.pos):
                theme = (theme + 1) % 4
            
            elif menu_settings and sound_menu_btn.collidepoint(event.pos):
                sound_on = not sound_on
            
            elif menu_settings and reset_btn.collidepoint(event.pos):
                high_score = 0

                with open("highscore.txt", "w") as file:
                    file.write("0")
            elif menu_settings and back_btn.collidepoint(event.pos):
                menu_settings = False

            elif exit_btn.collidepoint(event.pos):
                pygame.quit()
                quit()
        # ---------- MAIN MENU SETTINGS PANEL ----------
        if menu_settings:
            # Dark transparent background
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            # Settings panel
            pygame.draw.rect(screen, WHITE, (100, 40, 400, 300))
            pygame.draw.rect(screen, RED, (100, 40, 400, 300), 4)

            title = title_font.render("SETTINGS", True, BLACK)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))
    
            # Theme button
            theme_btn = pygame.Rect(180, 100, 240, 40)
            pygame.draw.rect(screen, (100,100,100), theme_btn)
            if theme == 0:
                theme_name = "Classic"
            elif theme == 1:
                theme_name = "Ocean"
            elif theme == 2:
                theme_name = "Forest"
            else:
                theme_name = "Night"

            theme_text = font.render("Theme : " + theme_name, True, WHITE)
            screen.blit(theme_text, theme_text.get_rect(center=theme_btn.center))

            # Sound button
            sound_menu_btn = pygame.Rect(180, 150, 240, 40)
            pygame.draw.rect(screen, (100,100,100), sound_menu_btn)

            if sound_on:
                sound_text = font.render("Sound : ON", True, GREEN)
            else:
                sound_text = font.render("Sound : OFF", True, RED)

            screen.blit(sound_text, sound_text.get_rect(center=sound_menu_btn.center))

            # Reset High Score
            reset_btn = pygame.Rect(180, 200, 240, 40)
            pygame.draw.rect(screen, (100,100,100), reset_btn)

            reset_text = font.render("Reset High Score", True, YELLOW)
            screen.blit(reset_text, reset_text.get_rect(center=reset_btn.center))

            # Back button
            back_btn = pygame.Rect(180, 260, 240, 40)
            pygame.draw.rect(screen, (100,100,100), back_btn)

            back_text = font.render("BACK", True, ORANGE)
            screen.blit(back_text, back_text.get_rect(center=back_btn.center))
        
        pygame.display.flip()
    
while running:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, BLOCK):
                direction = (0, -BLOCK)

            elif event.key == pygame.K_DOWN and direction != (0, -BLOCK):
                direction = (0, BLOCK)

            elif event.key == pygame.K_LEFT and direction != (BLOCK, 0):
                direction = (-BLOCK, 0)

            elif event.key == pygame.K_RIGHT and direction != (-BLOCK, 0):
                direction = (BLOCK, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if settings_btn.collidepoint(x, y):
                settings_open = True
                paused = True
            elif settings_open and sound_btn.collidepoint(x, y):
                 sound_on = not sound_on

            elif settings_open and resume_btn.collidepoint(x, y):
                 settings_open = False
                 paused = False

            elif settings_open and exit_game_btn.collidepoint(x, y):
                pygame.quit()
                quit()
            
            
            elif up_btn.collidepoint(x, y) and direction != (0, BLOCK):
                direction = (0, -BLOCK)

            elif down_btn.collidepoint(x, y) and direction != (0, -BLOCK):
                direction = (0, BLOCK)

            elif left_btn.collidepoint(x, y) and direction != (BLOCK, 0):
                 direction = (-BLOCK, 0)

            elif right_btn.collidepoint(x, y) and direction != (-BLOCK, 0):
                 direction = (BLOCK, 0)
# Move snake
    # Move snake
    if not paused:
        head_x = snake[-1][0] + direction[0]
        head_y = snake[-1][1] + direction[1]
        new_head = (head_x, head_y)

        # Wall collision
        if (
          head_x <= 10 or
          head_x >= WIDTH - 10 - BLOCK or
          head_y <= 55 or
          head_y>=250 - BLOCK
          ):
          lives -= 1

          if lives == 0:
              break

          #score = 0
          snake = [(100, 80)]
          direction = (BLOCK, 0)
          continue
        # Self collision
        if new_head in snake:
            break

        snake.append(new_head)

        # Food collision
        if new_head == food:
            if sound_on:
                eat_sound.play()
            score += 1
            total_score+=1
            if total_score > high_score:
                high_score = total_score
                new_high_score=True

                with open("highscore.txt", "w") as file:
                    file.write(str(high_score))
            level=total_score//10+1
            
            if level > last_level:
              #  screen.fill(BLACK)
           #     pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, GAME_HEIGHT), 3)
                
                level_up = font.render("LEVEL UP!", True, GREEN)
                level_rect = level_up.get_rect(center=(WIDTH // 2, 105))
                screen.blit(level_up, level_rect)
                
                pygame.display.flip()
                pygame.time.wait(1000)
                
                last_level = level
                #food creating inside the while loop
            while True:
                food = (
                random.randrange(20, WIDTH - 20, BLOCK),
                random.randrange(80, 240, BLOCK)
                )
                if food not in snake:
                    break
        else:
            snake.pop(0)
   

    # Draw
    # Theme Background
    if theme == 0:
        bg_color = BLACK
    elif theme == 1:
        bg_color = (0, 70, 120)      # Ocean
    elif theme == 2:
        bg_color = (20, 90, 20)      # Forest
    else:
        bg_color = (40, 0, 70)       # Night

    pygame.draw.rect(
    screen,
    bg_color,
    (10, 10, WIDTH - 20, GAME_HEIGHT - 10)
)
    
    if theme == 3:
        border_color = YELLOW
    else:
        border_color = WHITE

    pygame.draw.rect(screen, border_color, (10, 10, WIDTH-20, GAME_HEIGHT-10), 3)
    pygame.draw.line(screen, WHITE, (10, 55), (WIDTH - 10, 55), 3)
    pygame.draw.line(screen, WHITE, (10, 250), (WIDTH - 10, 250), 3)
    pygame.draw.line(screen, WHITE, (450, 250), (450, HEIGHT - 10), 3)
    # Food color by theme
    if theme == 0:
        food_color = RED
    elif theme == 1:
        food_color = YELLOW
    elif theme == 2:
        food_color = MAGENTA
    else:
        food_color = CYAN

    pygame.draw.rect(screen, food_color, (*food, BLOCK, BLOCK))

    # Snake color by theme
    if theme == 0:
        snake_color = GREEN
    elif theme == 1:
        snake_color = CYAN
    elif theme == 2:
        snake_color = LIME
    else:
        snake_color = PINK

    for i, segment in enumerate(snake):

        if i == len(snake) - 1:
            pygame.draw.rect(screen, WHITE, (*segment, BLOCK, BLOCK))

            pygame.draw.circle(screen, BLACK, (segment[0] + 6, segment[1] + 6), 2)
            pygame.draw.circle(screen, BLACK, (segment[0] + 14, segment[1] + 6), 2)

        else:
            pygame.draw.rect(screen, snake_color, (*segment, BLOCK, BLOCK))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (25, 18))
    level_text = font.render(f"Level:{level}",True,WHITE)
    screen.blit(level_text, (180, 18))
    high_score_text = font.render(f"High: {high_score}", True, WHITE)
    screen.blit(high_score_text, (360, 18))
    heart = font.render("♥️", True, RED)
    for i in range(lives):
        screen.blit(heart, (500+i*25,15 ))
    draw_buttons()
    if settings_open:
        # Dark background
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Settings box
        pygame.draw.rect(screen, WHITE, (100, 40, 400, 270))
        pygame.draw.rect(screen, RED, (100, 40, 400, 270), 3)

        title = title_font.render("SETTINGS", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 90)))  
        # Sound button
        sound_btn = pygame.Rect(180, 120, 240, 45)
        pygame.draw.rect(screen, (100,100,100), sound_btn)

        if sound_on:
           sound_text = font.render("Sound : ON", True, GREEN)
        else:
           sound_text = font.render("Sound : OFF", True, RED)

        screen.blit(sound_text, sound_text.get_rect(center=sound_btn.center))

        # Resume button
        resume_btn = pygame.Rect(180, 180, 240, 50)
        pygame.draw.rect(screen, (100,100,100), resume_btn)

        resume_text = font.render("RESUME", True, ORANGE)
        screen.blit(resume_text, resume_text.get_rect(center=resume_btn.center))

        # Exit button
        exit_game_btn = pygame.Rect(180, 245, 240, 50)
        pygame.draw.rect(screen, (100,100,100), exit_game_btn)

        exit_text = font.render("EXIT", True, YELLOW)
        screen.blit(exit_text, exit_text.get_rect(center=exit_game_btn.center))
                                
    pygame.display.flip()
    clock.tick(5+(level-1))

# Game Over
screen.fill(BLACK)
# Restart Button
restart_btn = pygame.Rect(180, 260, 240, 50)

pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, GAME_HEIGHT), 3)
game_over = title_font.render("GAME OVER", True, RED)
final_score = font.render(f"Final Score: {score}", True, WHITE)
#New High score if  it beats the High score
if new_high_score:
    high_score_text = font.render(f"NEW HIGH SCORE: {high_score}", True, GREEN)
else:
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    
game_over_rect = game_over.get_rect(center=(WIDTH // 2, 90))
screen.blit(game_over, game_over_rect)

final_score_rect = final_score.get_rect(center=(WIDTH // 2, 160))
screen.blit(final_score, final_score_rect)

high_score_rect = high_score_text.get_rect(center=(WIDTH // 2,200))
screen.blit(high_score_text, high_score_rect)
pygame.draw.rect(screen, (100,100,100), restart_btn)

restart_text = font.render("RESTART", True, GREEN)

screen.blit(
    restart_text,
    restart_text.get_rect(center=restart_btn.center)
)
pygame.display.flip()

waiting = True

# Start timer
start_time = pygame.time.get_ticks()

while waiting:

    # Auto restart after 5 seconds
    if pygame.time.get_ticks() - start_time >= 4000:

        waiting = False

        # Restart Game
        snake = [(100, 80)]
        direction = (BLOCK, 0)

        score = 0
        total_score = 0
        level = 1
        last_level = 1
        lives = 3

        food = (
            random.randrange(20, WIDTH-20, BLOCK),
            random.randrange(80, 240, BLOCK)
        )

        paused = False
        running = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if restart_btn.collidepoint(event.pos):

                waiting = False

                # Restart Game
                snake = [(100, 80)]
                direction = (BLOCK, 0)

                score = 0
                total_score = 0
                level = 1
                last_level = 1
                lives = 3

                food = (
                    random.randrange(20, WIDTH-20, BLOCK),
                    random.randrange(80, 240, BLOCK)
                )

                paused = False
                running = True