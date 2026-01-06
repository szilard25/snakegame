import pygame, random, sys              
pygame.init()               

SZELES = 1200
MAGAS =700

screen = pygame.display.set_mode((SZELES,MAGAS), pygame.RESIZABLE)
running = True
gamestate = "playing"

#Játékos(logo) adatai
logo = pygame.image.load("snake.png")
logorect = logo.get_rect()

#Alma adatai
almaposx = random.randint(0,SZELES-100)
almaposy = random.randint(0, MAGAS-160)
alma = pygame.image.load("alma.png")
almarect = alma.get_rect()
almarect.topleft = almaposx, almaposy

#Pontszámláló és betutipusok
points = 0
font = pygame.font.Font("gameoverfont.ttf", 36)
winfont = pygame.font.Font("gameoverfont.ttf", 100)
resszoveg = pygame.font.Font("gameoverfont.ttf", 36)
gameover = pygame.font.Font("gameoverfont.ttf", 100)
winszoveg = font.render("Win:10", True, (255,255,255))
gameovertext = gameover.render("GAME OVER", True, (255,255,255))
gameoverrect = gameovertext.get_rect()
restartszoveg = resszoveg.render("RESTART [R]   |   QUIT [ESC]", True, (255,255,255))
restartszovegrect = restartszoveg.get_rect()
gameend = winfont.render("WINNER!", True, (255,255,255))
gameendrect = gameend.get_rect()


#Ellenség adatai
enemy = pygame.image.load("enemy.png")
enemyrect = enemy.get_rect()
enemyrect.midtop = (SZELES/2, 10)
xleft = False
xright = True

enemy2 = pygame.image.load("enemy.png")
enemyrect2 = enemy2.get_rect()
enemyrect2.midbottom = (SZELES/2, MAGAS-80)
right = False
left = True

#Lovedek adatai
bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.rotate(bullet, 180)
bulletlist = []
new_bulletlist = []
bulletlist2 = []
lastspawn = 0
lastspawn2 = 0

#FPS szabályozás
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000
seb_x = 0
seb_y = 0

#Mozgás
def mozgas():
    keys=pygame.key.get_pressed()
    if keys[pygame.K_a]:
        logorect.x -= dt * 800
    if keys[pygame.K_w]:
        logorect.y -= dt * 800
    if keys[pygame.K_s]:
        logorect.y += dt * 800
    if keys[pygame.K_d]:
        logorect.x += dt * 800

#Képernyőn belul maradás
def stayinscreen():
    if logorect.top <= 60:
        logorect.top = 60
    if logorect.bottom >= MAGAS-160:
        logorect.bottom = MAGAS-160
    if logorect.left <= 0:
        logorect.left = 0
    if logorect.right >= SZELES:
        logorect.right = SZELES

#Alma megevése (ütkozés / collide)
def appleeating():
    global points
    if logorect.colliderect(almarect):
        almaposx = random.randint(0,SZELES-100)
        almaposy = random.randint(60, MAGAS-160)
        almarect.midbottom = almaposx, almaposy
        points += 1

#Startmenu fuggvenye 
def startmenu():
    global startszovegrect, SZELES, MAGAS, screen
    start = True
    while start:
        screen.fill(( 53, 95, 30 ))
        startszoveg = font.render("START [S]  |  QUIT [ESC]", True,(255,255,255))
        startszovegrect = startszoveg.get_rect()
        startszovegrect.center = (SZELES/2, 400)
        screen.blit(startszoveg, startszovegrect)
        pygame.display.set_caption("SANATORA")
        pygame.display.set_icon(logo)
        almarect.center = SZELES/2, 230
        enemyrect.topleft = 130, 200
        logorect.topleft = SZELES-200, 200
        screen.blit(enemy,enemyrect)
        screen.blit(logo,logorect)
        screen.blit(alma,almarect)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start = False
                    enemyrect.midtop = SZELES/2, 10
                    enemyrect2.midbottom = (SZELES/2, MAGAS-80)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                    SZELES = event.w
                    MAGAS = event.h
                    screen = pygame.display.set_mode((SZELES,MAGAS), pygame.RESIZABLE)
        pygame.display.flip()
#Játék megnyerése / újraindítás ciklus
def checkwin():
    global points,screen,gamestate
    
    if points >= 10:
        gamestate = "win"
#Allando megjelenitett informaciok es spriteok
def draw():
    global new_bulletlist
    szoveg = font.render(f"Score:{points}",True,(255,255,254))
    screen.fill(( 53, 95, 30 ))
    screen.blit(alma,almarect)
    screen.blit(logo,logorect)
    screen.blit(enemy,enemyrect)
    screen.blit(enemy2,enemyrect2)
    screen.blit(szoveg,(SZELES-250,MAGAS-80))
    screen.blit(winszoveg,(30,MAGAS-80))

    new_bulletlist = []
    for b in bulletlist:
        b.y += 10
        if b.y < MAGAS:
            
            new_bulletlist.append(b)

#Enemy mozgas
def enemymovement():
    global xleft, xright
    global sebesseg
    sebesseg = 600
    if xright:
        enemyrect.x += sebesseg * dt 
    if xleft:
        enemyrect.x -= sebesseg * dt 

    if enemyrect.right >= SZELES:
        enemyrect.right = SZELES
        xright = False
        xleft = True
    if enemyrect.left <= 0:
        enemyrect.left = 0
        xright = True
        xleft = False
#Enemy shooting 
def enemyshooting():
    global currenttime , bulletrect, lastspawn

    spawndelay = 400
    if currenttime - lastspawn >= spawndelay:
        bulletrect = bullet.get_rect(center = enemyrect.center)
        bulletlist.append(bulletrect)
        lastspawn = currenttime

#Lovedek kirajzolas
def draw_bullet():
    for b in bulletlist:
        screen.blit(bullet,b)

#Lovedek kitorles ha kimegy a kepernyobol
def delete_bullet():
    global new_bulletlist
    new_bulletlist = []
    for b in bulletlist:
        b.y += 10
        if b.y <= MAGAS:
            new_bulletlist.append(b)

def enemy2_mozgas():
    global right, left, sebesseg
    sebesseg = 600
    if right:
        enemyrect2.x += sebesseg * dt 
    if left:
        enemyrect2.x -= sebesseg * dt

    if enemyrect2.right >= SZELES:
        enemyrect2.right = SZELES
        right = False
        left = True
    if enemyrect2.left <= 0:
        enemyrect2.left = 0
        right = True
        left = False
def enemy2_shooting():
    global currenttime , bulletrect2, lastspawn2
    spawndelay = 400
    if currenttime - lastspawn2 >= spawndelay:
        bulletrect2 = bullet.get_rect(center = enemyrect2.center)   
        bulletlist2.append(bulletrect2)      
        lastspawn2 = currenttime
def bullet2_drawing():
    for b in bulletlist2:
        screen.blit(bullet,b)
        b.y -= 10
#Gameover ha eltalal
def gameover_():
    global restartszoveg, bulletlist, gamestate, running
    for b in bulletlist or bulletlist2:
        if logorect.colliderect(b):
            gamestate = "gameover"

#Startmenu meghívása a gameloop elott
startmenu()

#Játék loopja
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if gamestate == "win" or gamestate == "gameover":
                if event.key == pygame.K_r:
                    points = 0
                    logorect.center = (SZELES/2,MAGAS/2)
                    almaposx = random.randint(0,SZELES-100)
                    almaposy = random.randint(70, MAGAS-160)
                    almarect.topleft = (almaposx,almaposy)
                    bulletlist.clear()
                    new_bulletlist.clear()
                    gamestate = "playing"
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.VIDEORESIZE:    
                SZELES = event.w
                MAGAS = event.h
                screen = pygame.display.set_mode((SZELES, MAGAS), pygame.RESIZABLE)
                enemyrect2.midbottom = (SZELES/2, MAGAS-80)
                
    dt = clock.tick(60) / 1000
    currenttime = pygame.time.get_ticks()

    if gamestate == "playing": 
        mozgas()
        stayinscreen()
        appleeating()    
        checkwin()
        draw()
        enemymovement()
        enemyshooting()
        delete_bullet()
        draw_bullet()
        gameover_()
        enemy2_mozgas()
        enemy2_shooting()
        bullet2_drawing()
        bulletlist = new_bulletlist
        
    elif gamestate == "win":
        gameendrect.center = (SZELES/2, 250)
        restartszovegrect.center = (SZELES/2, 450)
        draw()
        screen.blit(gameend, gameendrect)
        screen.blit(restartszoveg, restartszovegrect)

    elif gamestate == "gameover":
        gameoverrect.center = (SZELES/2, MAGAS/3)
        restartszovegrect.center = (SZELES/2, 450)
        draw()
        screen.blit(gameovertext, gameoverrect)
        screen.blit(restartszoveg, restartszovegrect)

                     
    pygame.display.set_caption("SANATORA")
    pygame.display.set_icon(logo)
    pygame.display.flip()
    clock.tick(60)