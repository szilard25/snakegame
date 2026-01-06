import pygame, sys
pygame.init()

x = 1200
y = 700
screen = pygame.display.set_mode((x, y))

text = ""
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))  # Black background
    
    # Render the text
    text_surface = font.render(text, True, (255, 255, 255))  # White text
    text_rect = text_surface.get_rect()
    text_rect.center = (x/2, y/2)
    screen.blit(text_surface, text_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            elif event.key == pygame.K_RETURN:
                print("Entered text:", text)
                text = ""  # Clear text after Enter
            elif event.key == pygame.K_ESCAPE:
                running = False
            else:
                # Add the character to the text
                text += event.unicode
    
    print(text)
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit() 