# Tower defense game
import random
from os import path, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import math

# Defining variables + image/sound paths
WIDTH = 1400
HEIGHT = 820
FPS = 30
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
CANNON_GREY = (188, 194, 170)
WHITE2 = (255, 255, 255, 255)

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tower Defense')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, RED) # True makes it nicer to read
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) 
    surf.blit(text_surface, text_rect)
# Used for drawing on the screen
def draw_block(surface, x, y, img):
    img.set_colorkey(BLACK)
    img_rect = img.get_rect()
    img_rect.centerx = x
    img_rect.centery = y
    surface.blit(img, img_rect)
# Draw score
def draw_score(score_, a, b):
    for chiffre in str(score):
        chif = int(chiffre)
        draw_block(screen, a, b, NOMBRE[chif])
        a += 30
    draw_block(screen, 350, 40, hud)
# Draw coins
def draw_coins(score_, a, b):
    for chiffre in str(coins_total):
        chif = int(chiffre)
        draw_block(screen, a, b, NOMBRE_GOLD[chif])
    draw_block(screen, 540, 40, pygame.transform.scale(COIN[0], (30,40)))
# Draw house life
def draw_house_life(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 10
    fill = (pct / 300) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
# Draw enemy life
def draw_enemy_life(surf, type, mob_type, pct):
    if pct < 0:
        pct = 0
    if mob_type == 'bee':
        BAR_LENGTH = 25
        BAR_HEIGHT = 5
        fill = pct
        outline_rect = pygame.Rect(type.rect.x - 2, type.rect.y - 10, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(type.rect.x - 2, type.rect.y - 10, fill, BAR_HEIGHT)
    if mob_type == 'ghost':
        BAR_LENGTH = 30
        BAR_HEIGHT = 5
        fill = pct
        outline_rect = pygame.Rect(type.rect.x + 2, type.rect.y - 10, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(type.rect.x + 2, type.rect.y - 10, fill, BAR_HEIGHT)
    if mob_type == 'mob':
        BAR_LENGTH = 30
        BAR_HEIGHT = 5
        fill = pct
        if type.grosseur == (35,50):
            outline_rect = pygame.Rect(type.rect.x + 3, type.rect.y - 10, BAR_LENGTH, BAR_HEIGHT)
            fill_rect = pygame.Rect(type.rect.x + 3, type.rect.y - 10, fill, BAR_HEIGHT)
        if type.grosseur == (55,70):
            outline_rect = pygame.Rect(type.rect.x + 13, type.rect.y - 10, BAR_LENGTH, BAR_HEIGHT)
            fill_rect = pygame.Rect(type.rect.x + 13, type.rect.y - 10, fill, BAR_HEIGHT)
        if type.grosseur == (65,80):
            outline_rect = pygame.Rect(type.rect.x + 17, type.rect.y - 10, BAR_LENGTH, BAR_HEIGHT)
            fill_rect = pygame.Rect(type.rect.x + 17, type.rect.y - 10, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)
# Draw wave
def write_wave(compteur):
    draw_text(screen, f'Wave {compteur_waves} starting soon...', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, 'Good luck!', 22, 
                WIDTH/2, HEIGHT/2)
    pygame.display.flip()


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


        self.climb1 = pygame.time.get_ticks()
        self.climb_timer_choose = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed() 
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
            self.image_frame += 1
            if self.image_frame == 11:
                self.image_frame = 0
            self.image = pygame.transform.flip(PLAYER_IMAGES[self.image_frame], True, False)

        if keystate[pygame.K_RIGHT]:
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
        if (keystate[pygame.K_UP]) and (950 <= self.rect.x <= 990) and self.rect.y > 230 :
            self.climb()

        # falling down
        if not (950 <= self.rect.x <= 990) and ((0 < self.rect.y <= 247) or (252 <= self.rect.y <= HEIGHT/2 + 40)):
            self.fall()

        # climbing down
        if (950 <= self.rect.x <= 990) and (keystate[pygame.K_DOWN]):
            self.climbdown()

    def climb(self):
        now = pygame.time.get_ticks()
        if now - self.climb1 >= self.climb_timer:
            self.climb1 = now
            self.frame_climb += 1
            if self.frame_climb == 14:
                self.frame_climb = 12
        self.rect.y -= 2
        self.image = PLAYER_IMAGES[self.frame_climb]

    def climbdown(self):
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
        if 0 < self.rect.y < 252:
            self.rect.y += ((200 + player.rect.y)**2)/20000
        else:
            self.rect.y += ((player.rect.y)**2)/20000

        self.image = PLAYER_IMAGES[14]
        if 245 <= self.rect.y <= 250:
            self.rect.y = 250
            fall.play()
            self.image = PLAYER_IMAGES[15]
        if HEIGHT/2 + 38 <= self.rect.y <= HEIGHT/2 + 50:
            self.rect.y = HEIGHT/2 + 42
            fall.play()
            self.image = PLAYER_IMAGES[15]

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.y_chooser = random.choice((1,2,3))
        self.image = GHOST[0]
        self.rect = self.image.get_rect()
        if self.y_chooser == 1 or self.y_chooser == 2:
            self.rect.y = 440
        else:
            self.rect.y = random.randrange(100, 440)
        self.rect.x = random.randrange(-50,-20)
        self.speedx = random.randrange(2,4)
        self.life = 30
        self.frame = 0
        self.compteur = 0

    def update(self):
        self.rect.x += self.speedx
        self.compteur += 1
        if self.compteur == 40:
            self.frame += 1
            if self.frame == 2:
                self.frame = 0
            self.image = GHOST[self.frame]
            self.compteur = 0
        self.image.set_colorkey(BLACK)
        draw_enemy_life(screen, self, 'ghost', self.life)

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
        self.rect.x = random.randrange(-60, -20)
        self.rect.y = HEIGHT / 2 - self.rect.centery * 2 + 107
        # Walking variables
        self.time_walk = pygame.time.get_ticks()
        self.time_timer = 38
        self.life = 30
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
        draw_enemy_life(screen, self, 'mob', self.life)

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

class Cannon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = CANNON[0]
        self.image.set_colorkey(CANNON_GREY)
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = HEIGHT/2 + 42

        self.shoot_timer = 600
        self.time = pygame.time.get_ticks()

        self.frame_time = pygame.time.get_ticks()
        self.frame_timer = self.shoot_timer * 1/6


    def update(self):
        self.image = CANNON[self.frame]
        self.image.set_colorkey(CANNON_GREY)

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.rect.y -= 5
            if 175 <= self.rect.y <= 180:
                self.rect.y = 178
        if keystate[pygame.K_s]:
            self.rect.y += 5
            if (HEIGHT/2 + 49) <= self.rect.y <= (HEIGHT/2 + 54):
                self.rect.y = HEIGHT/2 + 52

        if keystate[pygame.K_SPACE]:
            self.shoot()
            self.changeframe()
            
        else:
            self.frame = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.time >= self.shoot_timer and self.frame == 3:
            self.time = now
            bullet = Bullet()
            all_sprites.add(bullet)
            bullets.add(bullet)
            boom.play()

    def changeframe(self):
        noww = pygame.time.get_ticks()
        if self.frame == 6:
            self.frame = 0
        else:
            if noww - self.frame_time >= self.frame_timer and self.frame != 6:
                self.frame += 1
                self.frame_time = noww
                self.changeframe()

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(BULLETS[3], (15,12))
        self.rect = self.image.get_rect()
        self.rect.x = 913
        self.rect.y = cannon.rect.centery - 4
        self.speedx = 6

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.x < -20:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = COIN[0]
        self.image.set_colorkey(WHITE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = type.rect.centerx
        self.rect.y = type.rect.centery
        self.compteur = random.randrange(0,50)
        self.frame = 0
        self.time = pygame.time.get_ticks()
        self.timer = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.time >= self.timer:
            self.time = now
            self.frame += 1
            if self.frame == 8:
                self.frame = 0
            
            self.image = COIN[self.frame]
            self.rect.y += 3
            if 495 <= self.rect.y <= HEIGHT:
                self.rect.y = 495
            self.compteur += 1
            if 600 <= self.compteur <= 603 or 605 <= self.compteur <= 608 or 610 <= self.compteur <= 613 or \
                616 <= self.compteur <= 618 or 620 <= self.compteur <= 622 or 624 <= self.compteur <= 625:
                self.image = empty
                self.image.set_colorkey(WHITE)
            
            if self.compteur == 627:
                self.kill()

class Bee(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = BEE[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-60, -20)
        self.rect.y = random.randrange(200, 350)
        self.speedx = random.randrange(1,3)
        self.frame = 0

        self.timer = 100
        self.time_now = pygame.time.get_ticks()
        self.life = 25

    def update(self):
        self.rect.y = random.choice([self.rect.y + 1, self.rect.y - 1])
        self.rect.x += self.speedx
        now = pygame.time.get_ticks()
        if now - self.time_now >= self.timer:
            self.time_now = now
            self.frame += 1
            if self.frame == 2:
                self.frame = 0
            self.image = BEE[self.frame]
        if self.rect.x > WIDTH + 65:
            self.kill()
        draw_enemy_life(screen, self, 'bee', self.life)

    def die(self):
        self.rect.y += (self.rect.y**2)/20000
        if HEIGHT/2 + 38 <= self.rect.y <= HEIGHT/2 + 42:
            self.rect.y = HEIGHT/2 + 42

class Gear(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = gear
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 934
        self.rect.y = HEIGHT/2 + 60

    def update(self):
        self.rect.x = cannon.rect.x + 40
        self.rect.y = cannon.rect.y + 40

class Explosion(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(EXPLOSION[0], (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = type.rect.centerx
        self.rect.y = type.rect.centery
        self.frame = 0
        self.time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.time > 100:
            self.time = now
            self.frame += 1
            if self.frame == 11:
                self.kill()
            self.image = EXPLOSION[self.frame]


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

BULLETS = []
for i in range(4):
    filename = 'bullet{}.png'.format(i)
    bullet = pygame.image.load(path.join(img_dir, filename)).convert()
    bullet.set_colorkey(WHITE)
    bullet.set_colorkey(BLACK)
    bullet = pygame.transform.flip(bullet, True, False)
    bullet = pygame.transform.scale(bullet, (20,10))
    BULLETS.append(bullet)

EXPLOSION = []
for i in range(12):
    filename = 'explosion{}.png'.format(i)
    explosion = pygame.image.load(path.join(img_dir, filename)).convert()
    explosion = pygame.transform.scale(explosion, (30,30))
    explosion.set_colorkey(BLACK)
    EXPLOSION.append(explosion)

CANNON = []
for i in range(6):
    filename = 'cannon_c{}.png'.format(i)
    cannon = pygame.image.load(path.join(img_dir, filename)).convert()
    cannon = pygame.transform.rotate(cannon, (20))
    cannon = pygame.transform.scale(cannon, (70, 60))
    CANNON.append(cannon)

NOMBRE = []
for i in range(10):
    filename = 'hud_{}.png'.format(i)
    nombre = pygame.image.load(path.join(img_dir, filename)).convert()
    nombre.set_colorkey(BLACK)
    nombre.set_colorkey(WHITE)
    NOMBRE.append(nombre)

NOMBRE_GOLD = []
for i in range(10):
    filename = 'hud_{} copy.png'.format(i)
    nombre = pygame.image.load(path.join(img_dir, filename)).convert()
    nombre.set_colorkey(BLACK)
    nombre.set_colorkey(WHITE)
    NOMBRE_GOLD.append(nombre)

COIN = []
for i in range(8):
    filename = 'coin{}.png'.format(i)
    coin = pygame.image.load(path.join(img_dir, filename)).convert()
    coin.set_colorkey(WHITE)
    coin.set_colorkey(BLACK)
    coin = pygame.transform.scale(coin, (20,20))
    COIN.append(coin)

GHOST = []
for i in range(2):
    filename = 'ghost{}.png'.format(i)
    ghost = pygame.image.load(path.join(img_dir, filename)).convert()
    ghost = pygame.transform.scale(ghost, (35,47))
    ghost = pygame.transform.flip(ghost, True, False)
    GHOST.append(ghost)


beefly1 = pygame.image.load(path.join(img_dir, 'bee0.png')).convert()
beefly2 = pygame.image.load(path.join(img_dir, 'bee1.png')).convert()
beefly1 = pygame.transform.scale(beefly1, (25, 20))
beefly2 = pygame.transform.scale(beefly2, (25, 20))
beefly1.set_colorkey(BLACK)
beefly2.set_colorkey(BLACK)
beefly3 = pygame.image.load(path.join(img_dir, 'bee2.png')).convert()
beefly3 = pygame.transform.scale(beefly3, (25, 20))
beefly3.set_colorkey(BLACK)
BEE = [pygame.transform.flip(beefly1, True, False), pygame.transform.flip(beefly2, True, False), pygame.transform.flip(beefly3, True, False)]


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

gear = pygame.image.load(path.join(img_dir, 'gear.png')).convert()
gear = pygame.transform.scale(gear, (30,30))
chain = pygame.image.load(path.join(img_dir, 'chain.png')).convert()
chain = pygame.transform.scale(chain, (10, 40))
chain.set_colorkey(WHITE)
coinGold = pygame.image.load(path.join(img_dir, 'coinGold.png')).convert()
hud = pygame.image.load(path.join(img_dir, 'hud_10.png')).convert()
hud.set_colorkey(WHITE)
hud.set_colorkey(BLACK)
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

boom = pygame.mixer.Sound(path.join(snd_dir, 'gun_fire.wav'))
boom.set_volume(0.05)
coin_get = pygame.mixer.Sound(path.join(snd_dir, 'smw_coin.wav'))
fall = pygame.mixer.Sound(path.join(snd_dir, 'fall.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'Battle Theme1.wav'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1) #loops everytime it reaches the end


# ------------------------------------------------------------------------------------------------------ #
# Creating sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bees = pygame.sprite.Group()
bullets = pygame.sprite.Group()
coins = pygame.sprite.Group()
joueur = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

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
for i in range(10):
    c = Cloud()
    all_sprites.add(c)


gear = Gear()
all_sprites.add(gear)

cannon = Cannon()
all_sprites.add(cannon)


player = Player()
all_sprites.add(player)
joueur.add(player)

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
    draw_block(screen, 1355, HEIGHT/2 + 10, pygame.transform.scale(pygame.transform.flip(sign, True, False), (40, 45)))
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
    for i in range(12):
        draw_block(screen, 1000, 300 + i * 20, pygame.transform.scale(laddermid, (25, 25)))
    # chain
    for i in range(25):
        draw_block(screen, 950, 500 - i * 20, chain)
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
coins_total = 0
score = 0
house_life = 300
gun_strength = 30

time_out_shoot = pygame.time.get_ticks()
time_out_bee = pygame.time.get_ticks()
time_out_mob = pygame.time.get_ticks()
time_out_ghost = pygame.time.get_ticks()

wave_written = False
check_mouse = False
running = True
game_over = True
compteur_waves = 1
compteur_mobs = 2
compteur_mobs_orig = compteur_mobs
spawn = True
while running:
    keystate = pygame.key.get_pressed() 
    # Keep loop runnning at the right speed
    clock.tick(FPS)
    # Process input (Events)
    for event in pygame.event.get(): 
        # Check for closing the window
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                print(pygame.mouse.get_pos())
    if spawn:
        time_in_bee = pygame.time.get_ticks()
        spawn_time_bee = 2000
        luck_bee = 200
        chiffre_bee = random.randrange(0, luck_bee)
        if time_in_bee - time_out_bee >= spawn_time_bee:
            if chiffre_bee == 2:
                if compteur_mobs != 0:
                    b = Bee()
                    all_sprites.add(b)
                    bees.add(b)
                    time_out_bee = time_in_bee

        time_in_mob = pygame.time.get_ticks()
        spawn_time_mob = 2000
        luck_mob = 200
        chiffre_mob = random.randrange(0, luck_mob)
        if time_in_mob - time_out_mob >= spawn_time_mob:
            if chiffre_mob == 2:
                if compteur_mobs != 0:
                    m = Mob()
                    all_sprites.add(m)
                    mobs.add(m)
                    time_out_mob = time_in_mob

        time_in_ghost = pygame.time.get_ticks()
        spawn_time_ghost = 2000
        luck_ghost = 200
        chiffre_ghost = random.randrange(0, luck_ghost)
        if time_in_ghost - time_out_ghost >= spawn_time_ghost:
            if chiffre_ghost == 2:
                if compteur_mobs != 0:
                    g = Ghost()
                    all_sprites.add(g)
                    ghosts.add(g)
                    time_out_ghost = time_in_ghost

    for bee in bees:
        if 1035 <= bee.rect.x <= 1040:
            bee.kill()
            house_life -= 10
            expl = Explosion(bee)
            all_sprites.add(expl)
        hits_bullet_bees = pygame.sprite.spritecollide(bee, bullets, True)
        for hits in hits_bullet_bees:
            bee.life -= gun_strength
            if bee.life <= 0:
                score += random.randrange(12, 15)
                coin_give = random.randrange(0,4)
                if coin_give == 0:
                    coin = Coin(bee)
                    coins.add(coin)
                    all_sprites.add(coin)
                all_sprites.remove(bee)
                bees.remove(bee)
                compteur_mobs -= 1

    for mob in mobs:
        if 1035 <= mob.rect.x <= 1040:
            mob.kill()
            house_life -= 10
            expl = Explosion(mob)
            all_sprites.add(expl)
        hits_bullets_mobs = pygame.sprite.spritecollide(mob, bullets, True)
        for hits in hits_bullets_mobs:
            mob.life -= gun_strength
            if mob.life <= 0:
                score += random.randrange(10, 12)
                coin_give = random.randrange(0,4)
                if coin_give == 0:
                    coin = Coin(mob)
                    coins.add(coin)
                    all_sprites.add(coin)
                all_sprites.remove(mob)
                mobs.remove(mob)
                compteur_mobs -= 1

    for ghost in ghosts:
        if 1035 <= ghost.rect.x <= 1040:
            ghost.kill()
            house_life -= 10
            expl = Explosion(ghost)
            all_sprites.add(expl)
        hits_bullets_ghost = pygame.sprite.spritecollide(ghost, bullets, True)
        for hits in hits_bullets_ghost:
            ghost.life -= gun_strength
            if ghost.life <= 0:
                score += random.randrange(10, 12)
                coin_give = random.randrange(0,4)
                if coin_give == 0:
                    coin = Coin(ghost)
                    coins.add(coin)
                    all_sprites.add(coin)
                all_sprites.remove(ghost)
                ghosts.remove(ghost)
                compteur_mobs -= 1

    for c in coins:
        hits_player_coin = pygame.sprite.spritecollide(c, joueur, False)
        for hits in hits_player_coin:
            coin_get.play()
            c.kill()
            coins_total += 1

    compteur_wait = 0
    if compteur_mobs == 0:
        spawn = False
        wave_written = True
        compteur_waves += 1
        compteur_mobs_orig += random.randrange(1,3)
        all_sprites.remove(bee for bee in bees)
        all_sprites.remove(ghost for ghost in ghosts)
        all_sprites.remove(mob for mob in mobs)
        bees.empty()
        mobs.empty()
        ghosts.empty()
        while wave_written is True:
            compteur_wait += 1
            write_wave(compteur_waves)
            if compteur_wait == 300:
                wave_written = False
                spawn = True
                compteur_wait = 0
                compteur_mobs = compteur_mobs_orig

    screen.fill(SKY)
    house()
    deco()
    all_sprites.update()
    draw_block(screen, 1150, 100, pygame.transform.scale(chimney, (40, 33)))
    # Draw / render
    draw_house_life(screen, 1050, 50, house_life)
    draw_score(score, 400, 40)
    draw_coins(coins_total, 600, 40)
    all_sprites.draw(screen)
    # After drawing everything, flip the display
    pygame.display.flip()
pygame.quit()