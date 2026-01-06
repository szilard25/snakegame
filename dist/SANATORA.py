import pygame
import random
pygame.init()

SZELES = 1200
MAGAS =700

screen = pygame.display.set_mode((SZELES,MAGAS))
running = True

#Játékos(logo) adatai
logo = pygame.image.load("snake.png")
logorect = logo.get_rect()

#Alma adatai
almaposx = random.randint(0,1100)
almaposy = random.randint(0, 630)
alma = pygame.image.load("alma.png")
almarect = alma.get_rect()
almarect.topleft = almaposx, almaposy


#Pontszámláló és cél
points = 0
font = pygame.font.Font(None, 72)
endfont = pygame.font.Font(None, 200)
resszoveg = pygame.font.Font(None, 36)
winszoveg = font.render("CÉL:10", True, (255,255,255))


#FPS szabályozás
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000
seb_x = 0
seb_y = 0

#Játék loopja
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#Mozgás
    dt = clock.tick(60) / 1000
    seb_x = 0
    seb_y = 0    
    keys=pygame.key.get_pressed()
    if keys[pygame.K_a]:
        logorect.x -= seb_x + dt * 800
    if keys[pygame.K_w]:
        logorect.y -= seb_y + dt * 800
    if keys[pygame.K_s]:
        logorect.y += seb_y + dt * 800
    if keys[pygame.K_d]:
        logorect.x += seb_x + dt * 800
#A képernyőn belül maradás
    if logorect.left < 0:
        logorect.left = 0
    if logorect.top < 0:
        logorect.top = 0
    if logorect.right > 1200:
        logorect.right = 1200
    if logorect.bottom > 700:
        logorect.bottom = 700
#Az alma megevése(ütkozés/collide)
    if logorect.colliderect(almarect):
        almaposx = random.randint(0,1100)
        almaposy = random.randint(0, 630)
        almarect.topleft = almaposx, almaposy
        points += 1
    
#Játék megnyerése/vége          és         újraindítás ciklus
    if points >= 1:
        gameend = endfont.render("WINNER!", True, (255,255,255))
        screen.blit(gameend,(320,150))
        restartszoveg = resszoveg.render("RESTART [R]      |     QUIT [ESC]", True, (255,255,255))
        screen.blit(restartszoveg,(450,350))
        pygame.display.flip()
        restart = True
        while restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        points = 0
                        logorect.topleft = (0,0)
                        almaposx = random.randint(0,1100)
                        almaposy = random.randint(0, 630)
                        almarect.topleft = (almaposx,almaposy)
                        restart = False

    szoveg = font.render(f"Points:{points}",True,(255,255,254))
    clock.tick(60)
    screen.fill(( 53, 95, 30 ))
    screen.blit(alma,almarect)
    screen.blit(logo,logorect)
    screen.blit(szoveg,(550,0))
    screen.blit(winszoveg,(30,620))
    pygame.display.set_caption("SANATORA")
    pygame.display.set_icon(logo)
    pygame.display.flip()

        
    