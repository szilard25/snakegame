import pygame
pygame.init()

x = 400
y = 500
screen = pygame.display.set_mode((x, y))
running = True

input_text = ""
font = pygame.font.Font(None, 36)
textsurface = font.render(input_text, True, (255, 255, 255))
szinvaltas = font.render("SZÍNVÁLTÁS", True, (255, 255, 255))
printing = True
current_color = (0, 0, 0)  # Start with black background

while running:
    screen.fill(current_color)
    textsurface = font.render(input_text, True, (255, 255, 255))
    inputrect = textsurface.get_rect()
    inputrect.center = (x/2, y/2)
    
    # Display the "SZÍNVÁLTÁS" text at the top
    szinvaltas_rect = szinvaltas.get_rect()
    szinvaltas_rect.center = (x/2, 50)
    screen.blit(szinvaltas, szinvaltas_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                input_text = ""
                printing = True
                current_color = (0, 0, 0)  # Reset to black
                
            elif event.key == pygame.K_RETURN:
                # Try to parse the color
                try:
                    # Remove any extra whitespace
                    color_input = input_text.strip().lower()
                    
                    # Handle common color names
                    color_map = {
                        'red': (255, 0, 0),
                        'green': (0, 255, 0),
                        'blue': (0, 0, 255),
                        'white': (255, 255, 255),
                        'black': (0, 0, 0),
                        'yellow': (255, 255, 0),
                        'cyan': (0, 255, 255),
                        'magenta': (255, 0, 255),
                        'orange': (255, 165, 0),
                        'purple': (128, 0, 128),
                        'pink': (255, 192, 203),
                        'gray': (128, 128, 128),
                        'grey': (128, 128, 128)
                    }
                    
                    if color_input in color_map:
                        current_color = color_map[color_input]
                        input_text = ""
                        printing = False
                    else:
                        # Try to parse RGB values (format: "r,g,b")
                        if ',' in color_input:
                            rgb_values = color_input.split(',')
                            if len(rgb_values) == 3:
                                r = int(rgb_values[0].strip())
                                g = int(rgb_values[1].strip())
                                b = int(rgb_values[2].strip())
                                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                                    current_color = (r, g, b)
                                    input_text = ""
                                    printing = False
                                else:
                                    input_text = "ERROR --> RGB values must be 0-255"
                            else:
                                input_text = "ERROR --> Use format: r,g,b"
                        else:
                            input_text = "ERROR --> Invalid color name or format"
                            
                except ValueError:
                    input_text = "ERROR --> Invalid color format"
                    
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
                printing = True
            else:
                input_text += event.unicode
                printing = True

        if printing:
            print(input_text)
            
    screen.blit(textsurface, inputrect)
    pygame.display.flip()

pygame.quit() 