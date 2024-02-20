#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer  

font.init()
font1 = font.SysFont('Arial', 36)
w = 700
h = 500
window = display.set_mode((w, h))
display.set_caption('Shooter')
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('galaxy_space.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
     
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()       
            
player = Player('rocket.png', 5, 400,80, 100, 10)

life = 3
lost = 0
score = 0
clock = time.Clock()
FPS = 60
game = True
finish = False

asteroids = sprite.Group()
for w in range(3):
    asteroid = Enemy('asteroid.png', randint(30, 620), -40, 80, 50, randint(1,3))
    asteroids.add(asteroid)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -40,80, 50, randint(1,3))
    monsters.add(monster)

rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    mixer.Sound('fire.ogg').play() 
                if num_fire >= 5 and rel_time == False:
                    next_time = timer()
                    rel_time = True
                    
    if not finish:
        text_lose = font1.render('Пропущенно:' + str(lost), 1, (255, 255, 255))
        text_score = font1.render('Счёт:' + str(score), 1, (255, 255, 255))
        text_life = font1.render('Жизни:' + str(life), 1, (255, 255, 255))
        window.blit(bg, (0, 0))
        window.blit(text_lose, (10, 50))
        window.blit(text_score, (10, 20))
        window.blit(text_life, (500, 200))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        player.reset()
        sprt_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        for t in sprt_list:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -40,80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1
        if life == 0 or lost >= 5:
            finish = True
            window.blit(font1.render('YOU LOSE', True, (196, 30, 58)), (250, 250))
        if score >= 10:
            finish = True 
            window.blit(font1.render('YOU WIN', True, (255, 250, 0)), (250, 250))
        if rel_time == True:
            new_time = timer()
            if new_time - next_time < 3:
                window.blit(font1.render('Wait, reloading...', True, (255, 250, 0)), (250, 350))
            else:
                num_fire = 0
                rel_time = False 
        display.update()
    clock.tick(FPS)