# Tower defense game
import random
from os import path, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import math

# Defining variables + image/sound paths
WIDTH = 1400
HEIGHT = 820
FPS = 40
img_dir = path.join(path.dirname(__file__), '1img_zb')
snd_dir = path.join(path.dirname(__file__), '1snd_zb')

# Defining colors
# Colors: https://gyazo.com/203fc10b2fd6f4fb10f1c43a89c4a872
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY = (150, 255, 255)


# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tower Defense')
clock = pygame.time.Clock()

# Used for drawing on the screen
def draw_block(surface, x, y, img):
    img.set_colorkey(BLACK)
    img_rect = img.get_rect()
    img_rect.centerx = x
    img_rect.centery = y
    surface.blit(img, img_rect)


# Creating new mobs
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Initializing a random variable for clouds
        self.grosseur = random.choice([(50,25), (100,30), (30,15), (40, 20)])
        self.image = pygame.transform.scale(CLOUD_IMAGES[random.randrange(0,3)], self.grosseur)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-200, WIDTH)
        self.rect.y = random.randrange(50, 240)
        # Speed timer
        self.time_move = pygame.time.get_ticks()
        self.time_timer = 75
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.time_move > self.time_timer:
            self.rect.x += 1
            self.time_move = now

        if self.rect.x >= WIDTH + 100:
            self.rect.x = -100

class Torch(pygame.sprite.Sprite):
    def __init__(self, *, compteur=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = TORCH[-1]
        self.rect = self.image.get_rect()
        if compteur == 0:
            self.rect.x = 1110
            self.rect.y = HEIGHT/2 + 15
        else:
            self.rect.x = 1245
            self.rect.y = HEIGHT/2 + 15

        self.feu_timer = pygame.time.get_ticks()
        self.timer = 200

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.feu_timer > self.timer:
            self.feu_timer = now
            self.image = random.choice(TORCH)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(PLAYER_IMAGES[0], True, False)
        self.image.set_colorkey(WHITE)
        self.image.set_colorkey(BLACK)
        self.image_frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = HEIGHT/2 + 42
        self.speedx = 0

        self.frame_climb = 12
        self.climb_timer = 150
        self.speedfall1 = 1
        self.speedfall2 = 1.5
        self.speedfall3 = 2

        self.climb1 = pygame.time.get_ticks()
        self.climb_timer_choose = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed() 
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
            self.image_frame += 1
            if self.image_frame == 11:
                self.image_frame = 0
            self.image = pygame.transform.flip(PLAYER_IMAGES[self.image_frame], True, False)

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5
            self.image_frame += 1
            if self.image_frame == 11:
                self.image_frame = 0
            self.image = PLAYER_IMAGES[self.image_frame]
        self.rect.x += self.speedx
        self.image.set_colorkey(WHITE)
        self.image.set_colorkey(BLACK)
        
        if self.rect.x >= 1075 and 245 <= self.rect.y <= 255:
            self.rect.x = 1075
            self.image = PLAYER_IMAGES[0]

        if self.rect.x <= 920 and 245 <= self.rect.y <= 255:
            self.rect.x = 920
            self.image = pygame.transform.flip(PLAYER_IMAGES[0], True, False)

        # climbing up
        if (keystate[pygame.K_UP] or keystate[pygame.K_w]) and (950 <= self.rect.x <= 990) and self.rect.y > 150 :
            self.climb()
        if not (950 <= self.rect.x <= 990) and ((0 < self.rect.y <= 247) or (252 <= self.rect.y <= HEIGHT/2 + 40)):
            self.fall()

        # climbing down
        if (950 <= self.rect.x <= 990) and (keystate[pygame.K_DOWN] or keystate[pygame.K_s]):
            self.climbdown()

    def climb(self):
        g.hide()
        now = pygame.time.get_ticks()
        if now - self.climb1 >= self.climb_timer:
            self.climb1 = now
            self.frame_climb += 1
            if self.frame_climb == 14:
                self.frame_climb = 12
        self.rect.y -= 2
        self.image = PLAYER_IMAGES[self.frame_climb]

    def climbdown(self):
        g.hide()
        now = pygame.time.get_ticks()
        if now - self.climb1 >= self.climb_timer:
            self.climb1 = now
            self.frame_climb += 1
            if self.frame_climb == 14:
                self.frame_climb = 12
        self.rect.y += 2
        if self.rect.y >= HEIGHT/2 + 40:
            self.rect.y = HEIGHT/2 + 40
        self.image = PLAYER_IMAGES[self.frame_climb]

    def fall(self):
        g.hide()
        self.rect.y += 3
        self.image = PLAYER_IMAGES[14]
        if 245 <= self.rect.y <= 250:
            self.rect.y = 250
            fall.play()
            self.image = PLAYER_IMAGES[15]
        if HEIGHT/2 + 38 <= self.rect.y <= HEIGHT/2 + 44:
            self.rect.y = HEIGHT/2 + 42
            fall.play()
            self.image = PLAYER_IMAGES[15]

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Initializing a random variable
        self.grosseurs = [(35,50), (55, 70), (65, 80)]
        self.rand = random.randrange(0,3)
        self.grosseur = self.grosseurs[self.rand]
        # Initalizing the mob
        self.image_frame = 0
        self.image = pygame.transform.scale(ENEMY_IMAGES[self.image_frame], self.grosseur)
        self.rect = self.image.get_rect()
        self.speedx = random.randrange(2, 4)
        self.rect.x = random.randrange(-300, -40)
        self.rect.y = HEIGHT / 2 - self.rect.centery * 2 + 107
        # Walking variables
        self.time_walk = pygame.time.get_ticks()
        self.time_timer = 38

    def update(self):
        # Gets mobs to walk slower
        walk = True
        now = pygame.time.get_ticks()
        if (now - self.time_walk > self.time_timer) and walk:
            self.time_walk = now
            self.rect.x += self.speedx
            self.image_frame += 1
            if self.image_frame == 10:
                self.image_frame = 1
            self.image = pygame.transform.scale(ENEMY_IMAGES[self.image_frame], self.grosseur)

class Smoke(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = SMOKE[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1125, 1135)
        self.rect.y = random.randrange(80, 87)
        self.speedy = random.random() * random.randrange(1,3)
        self.speedx = 1

    def update(self):
        self.frame += 1
        if self.frame == 12:
            self.frame = 0
        self.image = SMOKE[self.frame]
        self.rect.x += self.speedx
        self.rect.y -= self.speedy
        if self.rect.y <= -15 or self.rect.x >= 1215: 
            self.rect.y = random.randrange(50, 60)
            self.rect.x = random.randrange(1125, 1135)
            self.speedy = random.random() * random.randrange(1,3)

class Cactus(pygame.sprite.Sprite):
    def __init__(self, c=0):
        pygame.sprite.Sprite.__init__(self)
        if c == 0:
            self.grosseur = (55,120)
            self.image = pygame.transform.scale(HILL_IMAGES[0], self.grosseur)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = 700
            self.rect.y = HEIGHT / 2 - 10
        else:
            self.grosseur = (45,95)
            self.image = pygame.transform.scale(HILL_IMAGES[0], self.grosseur)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = 765
            self.rect.y = HEIGHT / 2 + 15
        # Change frame timer
        self.timer = random.randrange(7000, 10000)
        self.time_now = pygame.time.get_ticks()
        self.compteur_frame = 0

    def update(self):
        # Cactus blinks
        now = pygame.time.get_ticks()
        if now - self.time_now > self.timer:
            self.compteur_frame += 1
            if self.compteur_frame == 4:
                self.time_now = now
                self.compteur_frame = 0
            self.image = pygame.transform.scale(HILL_IMAGES[self.compteur_frame], self.grosseur)
            self.image.set_colorkey(BLACK)

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pistol
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x - 30
        self.rect.y = player.rect.y + 25
        self.mouse_pos = pygame.mouse.get_pos()
    
    def update(self):
        self.rect.y = player.rect.y + 25
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.rect.x = player.rect.x + 30
            self.image = pygame.transform.flip(pistol, True, False)
        elif keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.image = pistol
            self.rect.x = player.rect.x - 30
            self.rect.y = player.rect.y + 25

        # rotation
        if pygame.mouse.get_pressed()[0]:
            print(self.mouse_pos)
            if self.mouse_pos[0] <= player.rect.x:
                self.rotate()

    def rotate(self):
        self.x_mouse = self.rect.x - self.mouse_pos[0]
        self.y_mouse = self.rect.y - self.mouse_pos[1]
        self.angle_rot = 90 - math.sin(self.x_mouse/(math.sqrt(self.x_mouse**2 + self.y_mouse**2)))
        new_image = pygame.transform.rotate(self.image, self.angle_rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def hide(self):
        self.image = empty

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Bee(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.revers = False
        self.image = BEE[0]
        self.rect = self.image.get_rect()
        self.x_1 = random.randrange(-60, -20)
        self.x_2 = random.randrange(WIDTH + 20, WIDTH + 60)
        self.rect.x = random.choice([self.x_1, self.x_2])
        self.rect.y = random.randrange(50, 280)
        if -100 < self.rect.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.revers = True
        self.speedx = random.randrange(1,3)
        self.frame = 0

        self.timer = 100
        self.time_now = pygame.time.get_ticks()

    def update(self):
        self.rect.y = random.choice([self.rect.y + 1, self.rect.y - 1])
        if self.revers:
            self.rect.x += self.speedx
        if not self.revers:
            self.rect.x -= self.speedx
        now = pygame.time.get_ticks()
        if now - self.time_now >= self.timer:
            self.time_now = now
            self.frame += 1
            if self.frame == 2:
                self.frame = 0
            if self.revers:
                self.image = pygame.transform.flip(BEE[self.frame], True, False)
            else:
                self.image = BEE[self.frame]
        if self.rect.x < -55 or self.rect.x > WIDTH + 65:
            self.kill()


# ------------------------------------------------------------------------------------------------------ #
# Loading game graphics and game sounds
# Grass platforms
HOUSE_BLOCKS = []
for i in range(11):
    filename = 'house{}.png'.format(i)
    house = pygame.image.load(path.join(img_dir, filename)).convert()
    house.set_colorkey(WHITE)
    HOUSE_BLOCKS.append(house)

GRASS_IMAGES = []
for i in range(0, 12):
    filename = 'grass{}.png'.format(i)
    img_orig = pygame.image.load(path.join(img_dir, filename)).convert()
    img = pygame.transform.scale(img_orig, (45, 45))
    img.set_colorkey(WHITE)
    GRASS_IMAGES.append(img)

CLOUD_IMAGES = []
for i in range(1, 4):
    filename = 'cloud{}.png'.format(i)
    cloud = pygame.image.load(path.join(img_dir, filename)).convert()
    cloud.set_colorkey(WHITE)
    cloud.set_colorkey(WHITE)
    CLOUD_IMAGES.append(cloud)

HILL_IMAGES = []
for i in range(-1, 4):
    filename = 'hill_small{}0.png'.format(i)
    hill = pygame.image.load(path.join(img_dir, filename)).convert()
    hill.set_colorkey(WHITE)
    HILL_IMAGES.append(hill)

ENEMY_IMAGES = []
for i in range(1, 11):
    filename = 'p1_walk{}.png'.format(i)
    enemy = pygame.image.load(path.join(img_dir, filename)).convert()
    enemy.set_colorkey(BLACK)
    ENEMY_IMAGES.append(enemy)

PLAYER_IMAGES = []
for i in range(0, 16):
    filename = 'p3_walk0{}.png'.format(i)
    player = pygame.image.load(path.join(img_dir, filename)).convert()
    player = pygame.transform.scale(player, (50,70))
    player.set_colorkey(WHITE)
    player.set_colorkey(BLACK)
    PLAYER_IMAGES.append(player)

FOLIAGE = []
for i in range(1, 63):
    filename = 'foliagePack_0{}.png'.format(i)
    foliage = pygame.image.load(path.join(img_dir, filename)).convert()
    foliage.set_colorkey(BLACK)
    foliage.set_colorkey(WHITE)
    FOLIAGE.append(foliage)

TORCH = []
for i in range(1, 3):
    filename = 'torch{}.png'.format(i)
    torch = pygame.image.load(path.join(img_dir, filename)).convert()
    torch.set_colorkey(BLACK)
    torch = pygame.transform.scale(torch, (50,50))
    TORCH.append(torch)

ROOF = []
for i in range(6):
    filename = 'roof{}.png'.format(i)
    roof = pygame.image.load(path.join(img_dir, filename)).convert()
    roof.set_colorkey(BLACK)
    roof = pygame.transform.scale(roof, (50,50))
    ROOF.append(roof)

SMOKE = []
for i in range(12):
    filename = 'smoke{}.png'.format(i)
    smoke = pygame.image.load(path.join(img_dir, filename)).convert()
    smoke.set_colorkey(BLACK)
    smoke = pygame.transform.scale(smoke, (20,20))
    SMOKE.append(smoke)

beefly1 = pygame.image.load(path.join(img_dir, 'bee0.png')).convert()
beefly2 = pygame.image.load(path.join(img_dir, 'bee1.png')).convert()
beefly1 = pygame.transform.scale(beefly1, (25, 20))
beefly2 = pygame.transform.scale(beefly2, (25, 20))
beefly1.set_colorkey(BLACK)
beefly2.set_colorkey(BLACK)
BEE = [beefly1, beefly2]

pistol = pygame.image.load(path.join(img_dir, 'weapon00.png')).convert()
pistol = pygame.transform.scale(pistol, (50,38))
pistol.set_colorkey(WHITE)

doormid = pygame.image.load(path.join(img_dir, 'door_closed.png')).convert()
doormid.set_colorkey(WHITE)
doortop = pygame.image.load(path.join(img_dir, 'door_closedTop.png')).convert()
doortop.set_colorkey(WHITE)
doors = [doormid, doortop]

fen1 = pygame.image.load(path.join(img_dir, 'fence.png')).convert()
fen1.set_colorkey(WHITE)
fen2 = pygame.image.load(path.join(img_dir, 'fenceBroken.png')).convert()
fen2.set_colorkey(WHITE)
fences = [fen1, fen2]

box = pygame.image.load(path.join(img_dir, 'box.png')).convert()
bush = pygame.image.load(path.join(img_dir, 'bush.png')).convert()
bush.set_colorkey(WHITE)
sun = pygame.image.load(path.join(img_dir, 'sun_shiny.png')).convert()
sign = pygame.image.load(path.join(img_dir, 'signHangingCup.png')).convert()
sign2  = pygame.image.load(path.join(img_dir, 'signCoin.png')).convert()
clock_ = pygame.image.load(path.join(img_dir, 'clock.png')).convert()
redflag = pygame.image.load(path.join(img_dir, 'redFlag.png')).convert()
chimney = pygame.image.load(path.join(img_dir, 'chimney.png')).convert()
bridge = pygame.image.load(path.join(img_dir, 'bridge.png')).convert()
bridge.set_colorkey(WHITE)
ropeA = pygame.image.load(path.join(img_dir, 'ropeAttached.png')).convert()
ropeA = pygame.transform.rotate(ropeA, 250)
laddertop = pygame.image.load(path.join(img_dir, 'ladder_top.png')).convert()
laddertop.set_colorkey(WHITE)
laddermid = pygame.image.load(path.join(img_dir, 'ladder_mid.png')).convert()
laddermid.set_colorkey(WHITE)
empty = pygame.image.load(path.join(img_dir, 'empty.png')).convert()
empty.set_colorkey(WHITE)

windowmid = pygame.image.load(path.join(img_dir, 'windowmid.png')).convert()
windowmid.set_colorkey(WHITE)
windowtop = pygame.image.load(path.join(img_dir, 'windowtop.png')).convert()
windowtop.set_colorkey(WHITE)
window_orig = pygame.image.load(path.join(img_dir, 'windowCheckered.png')).convert()
window_orig.set_colorkey(WHITE)
windows = [windowmid, windowtop, window_orig]

fall = pygame.mixer.Sound(path.join(snd_dir, 'fall.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'Battle Theme 1.mp3'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1) #loops everytime it reaches the end


# ------------------------------------------------------------------------------------------------------ #
# Creating sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()


t1 = Torch(compteur=0)
t2 = Torch(compteur=1)
all_sprites.add(t1)
all_sprites.add(t2)


for i in range(3):
    s = Smoke()
    all_sprites.add(s)

c1 = Cactus(c=0)
c2 = Cactus(c=1)
all_sprites.add(c1)
all_sprites.add(c2)

for i in range(5):
    pass
    # m = Mob()
    # all_sprites.add(m)

for i in range(10):
    c = Cloud()
    all_sprites.add(c)


player = Player()
all_sprites.add(player)

g = Gun()
all_sprites.add(g)

# ------------------------------------------------------------------------------------------------------ #
# Decorations

def house():
    # sides
    for i in range(9):
        draw_block(screen, 1100, HEIGHT/2 + 50 - i * 30, HOUSE_BLOCKS[6])
        draw_block(screen, 1300, HEIGHT/2 + 50 - i * 30, HOUSE_BLOCKS[7])
    # lower left side
    draw_block(screen, 1100, HEIGHT / 2 + 82, HOUSE_BLOCKS[3])
    draw_block(screen, 1300, HEIGHT / 2 + 82, HOUSE_BLOCKS[5])
    # lower middle
    draw_block(screen, 1150, HEIGHT / 2 + 82, HOUSE_BLOCKS[4])
    draw_block(screen, 1250, HEIGHT / 2 + 82, HOUSE_BLOCKS[4])
    for i in range(3):
        draw_block(screen, 1150 + i * 40, HEIGHT / 2 - 100, HOUSE_BLOCKS[0])
        draw_block(screen, 1150 + i * 40, HEIGHT / 2 - 130, HOUSE_BLOCKS[0])
        draw_block(screen, 1150 + i * 40, HEIGHT / 2 - 150, HOUSE_BLOCKS[0])
        draw_block(screen, 1150 + i * 40, HEIGHT / 2 - 170, HOUSE_BLOCKS[0])
    # sides
    for i in range(2):
        for x in range(6):
            draw_block(screen, 1200, HEIGHT / 2 + 82 - x * 38, HOUSE_BLOCKS[0])
            draw_block(screen, 1150 + i * 100, HEIGHT / 2 + 82 - x * 38, HOUSE_BLOCKS[0])
    draw_block(screen, 1150, HEIGHT / 2 + 82, HOUSE_BLOCKS[4])
    draw_block(screen, 1250, HEIGHT / 2 + 82, HOUSE_BLOCKS[4])

    # sign
    draw_block(screen, 1045, HEIGHT/2, pygame.transform.scale(sign, (40, 45)))
    # red flag
    for i in range(6):
        draw_block(screen, 1085 + i * 40, HEIGHT/2 - 30, pygame.transform.scale(redflag, (40, 30)))
    draw_block(screen, 1085 + 220, HEIGHT/2 - 30, pygame.transform.scale(redflag, (40, 30)))
    draw_block(screen, 1085 + 240, HEIGHT/2 - 30, pygame.transform.scale(redflag, (40, 30)))
    # roof
    for x in range(6):
        for i in range(2):
            draw_block(screen, 1075 + x * 50, 180 - i * 50, ROOF[1])
    # windows
    draw_block(screen, 1133, HEIGHT / 2 - 150, pygame.transform.scale(windows[2], (40, 40)))
    draw_block(screen, 1268, HEIGHT / 2 - 150, pygame.transform.scale(windows[2], (40, 40)))
    # platform
    draw_block(screen, 1055, HEIGHT / 2 - 90, pygame.transform.scale(bridge, (40, 9)))
    draw_block(screen, 1020, HEIGHT / 2 - 90, pygame.transform.scale(bridge, (40, 9)))
    draw_block(screen, 1077, HEIGHT / 2 - 75, pygame.transform.scale(ropeA, (100, 100)))
    for i in range(6):
        draw_block(screen, 950 + i * 30, HEIGHT / 2 - 90, pygame.transform.scale(bridge, (40, 9)))
    # ladder
    for i in range(16):
        draw_block(screen, 1000, HEIGHT / 2 - 200 + i * 20, pygame.transform.scale(laddermid, (25, 25)))
def deco():


    TO_DRAW_DECO = [
        screen, 0, 15, pygame.transform.scale(sun, (200, 200)),
        screen, 1200, HEIGHT/2 + 90, pygame.transform.scale(doors[0], (50, 40)),
        screen, 1200, HEIGHT/2 + 50, pygame.transform.scale(doors[1], (50, 40)),
        screen, 210, HEIGHT/2 + 98, pygame.transform.scale(fences[0], (30, 22)),
        screen, 235, HEIGHT/2 + 98, pygame.transform.scale(fences[1], (30, 22)),
        screen, 685, HEIGHT/2 + 99, pygame.transform.scale(box, (20, 20)),
        screen, 340, HEIGHT/2 + 96, pygame.transform.scale(FOLIAGE[18], (65,30)),
        screen, 55, HEIGHT/2 + 99, pygame.transform.scale(box, (20, 20)), 
        screen, 84, HEIGHT/2 + 92, pygame.transform.scale(box, (35, 35)),
        screen, 130, HEIGHT/2 + 58, pygame.transform.scale(FOLIAGE[4], (65,100)),
        screen, 165, HEIGHT/2 + 48, pygame.transform.scale(FOLIAGE[4], (75,120)),
        screen, 600, HEIGHT/2 + 100, pygame.transform.scale(FOLIAGE[50], (80,30)),
        screen, 500, HEIGHT/2 + 95, pygame.transform.scale(FOLIAGE[0], (20,28)),
        screen, 480, HEIGHT/2 + 95, pygame.transform.scale(FOLIAGE[2], (20,34))
        ]
    val1 = 0
    val2 = 1
    val3 = 2
    val4 = 3
    for i in range((len(TO_DRAW_DECO)//4)):
        draw_block(TO_DRAW_DECO[val1], TO_DRAW_DECO[val2], 
                    TO_DRAW_DECO[val3], TO_DRAW_DECO[val4])
        val1 += 4
        val2 += 4
        val3 += 4
        val4 += 4

    for i in range(3):
        draw_block(screen, 290 + i**4, HEIGHT/2 + 98, pygame.transform.scale(FOLIAGE[17], (15,20)))

    # Drawing the dirt
    hauteur = HEIGHT - 47
    longueur = WIDTH - 75
    for times in range(2):
        draw_block(screen, longueur, hauteur, pygame.transform.scale(GRASS_IMAGES[8], (50, 50)))
        hauteur -= 130
    for times in range(1, 7):
        a = 22.5
        b = HEIGHT + 35 - (times * 45)
        for dirt in range(30):
            draw_block(screen, a, b, GRASS_IMAGES[7])
            a += 45
    a = 22.5
    for times in range(30):
        draw_block(screen, a, HEIGHT/2 + 130, GRASS_IMAGES[6])
        a += 45
    c = 22.5

# ------------------------------------------------------------------------------------------------------ #

# Game loop
time_out = pygame.time.get_ticks()
check_mouse = False
running = True
game_over = True
while running:
    # Keep loop runnning at the right speed
    clock.tick(FPS)
    # Process input (Events)
    for event in pygame.event.get(): 
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                print(pygame.mouse.get_pos())
    time_in = pygame.time.get_ticks()
    spawn_time = 2000
    chiffre = random.randrange(0,150)
    if time_in - time_out >= spawn_time:
        if chiffre == 2:
            b = Bee()
            all_sprites.add(b)
            time_out = time_in

    screen.fill(SKY)
    house()
    deco()
    all_sprites.update()
    draw_block(screen, 1150, 100, pygame.transform.scale(chimney, (40, 33)))
    # Draw / render
    
    all_sprites.draw(screen)
    


    # After drawing everything, flip the display
    pygame.display.flip()
pygame.quit()