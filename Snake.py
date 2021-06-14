import pygame
import random
import os

pygame.init()
pygame.font.init()

BG = pygame.image.load(os.path.join('Snake', 'Assets', 'Background.png'))
Apple = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Apple.png'))
Snake_Segment = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Segment.png'))

Apple_Coords = []
Snake_Segments = [[150, 450]]
player_score = 0

WIDTH = 750
HEIGHT = 850

BG_COLOR = (248, 233, 205)
FONT_COLOR = (0, 0, 0)
window = pygame.display.set_mode([WIDTH, HEIGHT])

clock = pygame.time.Clock()
score_font = pygame.font.SysFont('Comic Sans MS', 40)

def GENERATE_APPLE():
    x = random.randint(0, 14)
    y = random.randint(2, 16)
    Apple_Coords.append([x * 50, y * 50])

def MOVE(direction):
    for segment in Snake_Segments:
        if direction == 0:
            segment[1] -= 50
        elif direction == 1:
            segment[0] += 50
        elif direction == 2:
            segment[1] += 50
        elif direction == 3:
            segment[0] -= 50
        else:
            print("Something went wrong")

def HANDLE_APPLE_COLLISION(direction):
    global player_score
    for apple in Apple_Coords:
        if Snake_Segments[0][0] == apple[0] and Snake_Segments[0][1] == apple[1]:
            Apple_Coords.remove(apple)
            x = Snake_Segments[-1][0]
            y = Snake_Segments[-1][1]
            if direction == 0:
                Snake_Segments.append([x, y + 50])
            elif direction == 1:
                Snake_Segments.append([x - 50, y])
            elif direction == 2:
                Snake_Segments.append([x, y - 50])
            elif direction == 3:
                Snake_Segments.append([x + 50, y])
            player_score += 1
            GENERATE_APPLE()

def HANDLE_BOUNDARIES():
    for segment in Snake_Segments:
        if segment[0] > WIDTH:
            segment[0] = 0
        elif segment[0] < 0:
            segment[0] = WIDTH
        elif segment[1] > HEIGHT:
            segment[1] = 100
        elif segment[1] < 100:
            segment[1] = HEIGHT            

def DRAW_WINDOW():
    window.fill(BG_COLOR)
    window.blit(BG, (0, 100))

    # Score
    score = score_font.render(str(player_score), True, FONT_COLOR)
    window.blit(Apple, (25, 25))
    window.blit(score, (100, 25))

    for apple in Apple_Coords:
        window.blit(Apple, (apple[0], apple[1]))

    for segment in Snake_Segments:
        window.blit(Snake_Segment, (segment[0], segment[1]))

    pygame.display.update()

def main():
    running = True
    direction = 1
    time = 0
    GENERATE_APPLE()
    while running:
        clock.tick(60)
        time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    print(Apple_Coords)
                    print(Snake_Segments)
                if event.key == pygame.K_c:
                    print(player_score)
                if event.key == pygame.K_w:
                    direction = 0
                if event.key == pygame.K_d:
                    direction = 1
                if event.key == pygame.K_s:
                    direction = 2
                if event.key == pygame.K_a:
                    direction = 3

                if event.key == pygame.K_ESCAPE:
                    running = False

        if time % 15 == 0:
            MOVE(direction)
        HANDLE_BOUNDARIES()
        HANDLE_APPLE_COLLISION(direction)
        DRAW_WINDOW()

if __name__ == '__main__':
    main()