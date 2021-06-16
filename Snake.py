import pygame
import random
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

BG = pygame.image.load(os.path.join('Snake', 'Assets', 'Background.png'))
Apple = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Apple.png'))
Snake_Segment = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Segment.png'))

Eat_Sound = pygame.mixer.Sound(os.path.join('Snake', 'Assets', 'Apple_Eat.mp3'))

Apple_Coords = []
Snake_Segments = [[200, 450, 1], [250, 450, 1]]
player_score = 0

WIDTH = 750
HEIGHT = 850

BG_COLOR = (248, 233, 205)
FONT_COLOR = (0, 0, 0)
window = pygame.display.set_mode([WIDTH, HEIGHT])

clock = pygame.time.Clock()
score_font = pygame.font.SysFont('Comic Sans MS', 40)

lose = pygame.USEREVENT + 1

def GENERATE_APPLE():
    running = True
    iterations = 0
    x = random.randint(0, 14)
    y = random.randint(2, 16)
    while running:
        for segment in Snake_Segments:
            if x * 50 == segment[0] and y * 50 == segment[1]:
                iterations = 0
                x = random.randint(0, 14)
                y = random.randint(2, 16)
            else:
                iterations += 1
            if iterations >= len(Snake_Segments):
                running = False
    Apple_Coords.append([x * 50, y * 50])
    
def HANDLE_APPLE_COLLISION():
    global player_score
    for apple in Apple_Coords:
        if Snake_Segments[0][0] == apple[0] and Snake_Segments[0][1] == apple[1]:
            Apple_Coords.remove(apple)
            x = Snake_Segments[-1][0]
            y = Snake_Segments[-1][1]
            if Snake_Segments[0][2] == 0:
                Snake_Segments.append([x, y + 50, 0])
            elif Snake_Segments[0][2] == 1:
                Snake_Segments.append([x - 50, y, 1])
            elif Snake_Segments[0][2] == 2:
                Snake_Segments.append([x, y - 50, 2])
            elif Snake_Segments[0][2] == 3:
                Snake_Segments.append([x + 50, y, 3])
            player_score += 1
            Eat_Sound.play()
            GENERATE_APPLE()

def HANDLE_SNAKE_COLLISION():
    segment_one = Snake_Segments[0]
    for segment in Snake_Segments[1:]:
        if segment[0] == segment_one[0] and segment[1] == segment_one[1]:
            pygame.event.post(pygame.event.Event(lose))

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

def set_dir(dir, can_move):
    if can_move:
        for segment in Snake_Segments:
            segment[2] = dir

def HANDLE_MOVEMENT():
    del Snake_Segments[-1]
    x, y = Snake_Segments[0][0], Snake_Segments[0][1]
    if Snake_Segments[0][2] == 0:
        Snake_Segments.insert(0, [x, y - 50, 0])
    elif Snake_Segments[0][2] == 1:
        Snake_Segments.insert(0, [x + 50, y, 1])
    elif Snake_Segments[0][2] == 2:
        Snake_Segments.insert(0, [x, y + 50, 2])
    elif Snake_Segments[0][2] == 3:
        Snake_Segments.insert(0, [x - 50, y, 3])
    
def DRAW_WINDOW():
    window.fill(BG_COLOR)
    window.blit(BG, (0, 100))

    score = score_font.render(str(player_score), True, FONT_COLOR)
    window.blit(Apple, (25, 25))
    window.blit(score, (100, 25))

    for apple in Apple_Coords:
        window.blit(Apple, (apple[0], apple[1]))

    for segment in Snake_Segments:
        window.blit(Snake_Segment, (segment[0], segment[1]))

    pygame.display.update()


def main():
    can_move = True
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
            
            if event.type == lose:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and Snake_Segments[0][2] != 2 or event.key == pygame.K_UP and Snake_Segments[0][2] != 2:
                    set_dir(0, can_move)
                    can_move = False
                if event.key == pygame.K_d and Snake_Segments[0][2] != 3 or event.key == pygame.K_RIGHT and Snake_Segments[0][2] != 3:
                    set_dir(1, can_move)
                    can_move = False
                if event.key == pygame.K_s and Snake_Segments[0][2] != 0 or event.key == pygame.K_DOWN and Snake_Segments[0][2] != 0:
                    set_dir(2, can_move)
                    can_move = False
                if event.key == pygame.K_a and Snake_Segments[0][2] != 1 or event.key == pygame.K_LEFT and Snake_Segments[0][2] != 1:
                    set_dir(3, can_move)
                    can_move = False

                if event.key == pygame.K_ESCAPE:
                    running = False

        if time % 15 == 0:
            HANDLE_MOVEMENT()
            can_move = True
        if time > 60:
            HANDLE_SNAKE_COLLISION()
        HANDLE_BOUNDARIES()
        HANDLE_APPLE_COLLISION()
        DRAW_WINDOW()

if __name__ == '__main__':
    main()