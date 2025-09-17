import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The se7enth code")
font = pygame.font.SysFont(None, 60)

# Colors
RED = (255, 0, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Menu options
menu_items = ["Continue", "New Game", "Setting", "Quit"]
yes_no_options = ["Yes", "No"]
selected_index = 0

def draw_menu():
    screen.fill(BLACK)
    for i, item in enumerate(menu_items):
        color = WHITE if i == selected_index else GRAY
        text = font.render(item, True, color)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
        screen.blit(text, rect)
    pygame.display.update()

def main_menu():
    global selected_index
    while True:
        screen.fill(BLACK)
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if menu_items[selected_index] == " Continue":
                        pass
                    elif menu_items[selected_index] == "New Game":
                        game_loop()
                    elif menu_items[selected_index] == "Setting":
                        pass
                    elif menu_items[selected_index] == "Quit":
                        pygame.quit()
                        sys.exit()
def confirm():
    global selected_index
    selected_index = 0
    while True:
        screen.fill(BLACK)
        question = font.render("Are you sure?", True, WHITE)
        rect = question.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70))
        screen.blit(question, rect)

        for i, option in enumerate(yes_no_options):
            color = WHITE if i == selected_index else GRAY
            text = font.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2 + (i - 0.5) * 200, HEIGHT // 2 + 50))
            screen.blit(text, rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(yes_no_options)
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(yes_no_options)
                elif event.key == pygame.K_RETURN:
                    if yes_no_options[selected_index] == "Yes":
                        return True
                    else:
                        return False

def game_loop():
    player = pygame.Rect(375, 275, 50, 50)
    player_size = 50
    speed = 10
    running = True

    while running:
        clock = pygame.time.Clock()
        clock.tick(90)  # Limits to 90 FPS   
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed
        if keys[pygame.K_UP]:
            player.y -= speed
        if keys[pygame.K_DOWN]:
            player.y += speed
        if keys[pygame.K_ESCAPE]:
            if confirm():
                running = False

        if player.x - 10 < 0:
            player.x  = 0 + 10
        if player.x + player_size + 10 > WIDTH:
            player.x = WIDTH - player_size - 10
        if player.y - 10 < 0:
            player.y = 0 + 10
        if player.y + player_size + 10 > HEIGHT:
            player.y = HEIGHT - player_size - 10

        pygame.draw.rect(screen, CYAN, player)
        hitbox = player.inflate(20, 20)
        pygame.draw.rect(screen, RED, hitbox, 2)
        pygame.display.update()

    main_menu()

main_menu()