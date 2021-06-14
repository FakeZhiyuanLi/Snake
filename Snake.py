import pygame
import random
import os

pygame.init()

BG = pygame.image.load(os.path.join('Snake', 'Assets', 'Background.png'))
Apple = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Apple.png'))
Snake_Segment = pygame.image.load(os.path.join('Snake', 'Assets', 'Snake_Segment.png'))

Apple_Coords = []
Snake_Segments = []

WIDTH = 750
HEIGHT = 850

BG_COLOR = (248, 233, 205)
window = pygame.display.set_mode([WIDTH, HEIGHT])

clock = pygame.time.Clock()

def GENERATE_APPLE():
    x = random.randint(0, 14)
    y = random.randint(2, 16)
    Apple_Coords.append([x * 50, y * 50])

def DRAW_WINDOW():
    window.fill(BG_COLOR)
    window.blit(BG, (0, 100))

    for apple in Apple_Coords:
        window.blit(Apple, (apple[0], apple[1]))

    pygame.display.update()

def main():
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    GENERATE_APPLE()

        DRAW_WINDOW()

if __name__ == '__main__':
    main()