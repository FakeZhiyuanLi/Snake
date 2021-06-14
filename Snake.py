import pygame
import random
import os

pygame.init()
pygame.font.init()

BG = pygame.image.load(os.path.join('Snake', 'Assets', 'Background.png'))
Apple = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Apple.png'))
Snake_Segment = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Segment.png'))

Apple_Coords = []
Snake_Segments = [[150, 450, 1]]
Turning_Points = []
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
        if segment[2] == 0:
            segment[1] -= 50
        elif segment[2] == 1:
            segment[0] += 50
        elif segment[2] == 2:
            segment[1] += 50
        elif segment[2] == 3:
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
            if Snake_Segments[0][2] == 0:
                Snake_Segments.append([x, y - 50, 0])
            elif Snake_Segments[0][2] == 1:
                Snake_Segments.append([x - 50, y, 1])
            elif Snake_Segments[0][2] == 2:
                Snake_Segments.append([x, y + 50, 2])
            elif Snake_Segments[0][2] == 3:
                Snake_Segments.append([x + 50, y, 3])
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

def set_direction(direction):
    for segment in Snake_Segments:
        segment[2] = direction

def UP():
    x, y = Snake_Segments[0][0], Snake_Segments[0][1]
    Turning_Points.append([x, y, 0])
def RIGHT():
    x, y = Snake_Segments[0][0], Snake_Segments[0][1]
    Turning_Points.append([x, y, 1])
def DOWN():
    x, y = Snake_Segments[0][0], Snake_Segments[0][1]
    Turning_Points.append([x, y, 2])
def LEFT():
    x, y = Snake_Segments[0][0], Snake_Segments[0][1]
    Turning_Points.append([x, y, 3])

def HANDLE_TURNS():
    for turn in Turning_Points:
        for segment in Snake_Segments:
            if Snake_Segments[-1][0] == turn[0] and Snake_Segments[-1][1] == turn[1]:
                Snake_Segments[-1][2] = turn[2]
                Turning_Points.pop()
            if segment[0] == turn[0] and segment[1] == turn[1]:
                segment[2] = turn[2]

                

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
                    print(Turning_Points)
                if event.key == pygame.K_w and Snake_Segments[0][2] != 2:
                    set_direction(0)
                    UP()
                if event.key == pygame.K_d and Snake_Segments[0][2] != 3:
                    set_direction(1)
                    RIGHT()
                if event.key == pygame.K_s and Snake_Segments[0][2] != 0:
                    set_direction(2)
                    DOWN()
                if event.key == pygame.K_a and Snake_Segments[0][2] != 1:
                    set_direction(3)
                    LEFT()

                if event.key == pygame.K_ESCAPE:
                    running = False

        if time % 15 == 0:
            MOVE(Snake_Segments[0][2])
        HANDLE_BOUNDARIES()
        HANDLE_APPLE_COLLISION(direction)
        HANDLE_TURNS()
        DRAW_WINDOW()

if __name__ == '__main__':
    main()