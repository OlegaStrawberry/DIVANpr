#Создай собственный Шутер!

from pygame import *
from random import randint
max_lost = 10
score = 0
lost = 0
W_w = 700
W_h = 500
display.set_caption("Shooter")
window = display.set_mode((W_w, W_h))
background = transform.scale(image.load("heaven.jpg"), (W_w, W_h))
mixer.init()
mixer.music.load('tt.wav')
mixer.music.play()
fs = mixer.Sound('fire.ogg')
font.init()
font2 = font.SysFont('Arial', 40)
mls =  font2.render("ПОКА", 10, (14, 59, 24))
goal = 12
#clock

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

jnjr = GameSprite('az.jpg', 200, 200, 240, 270, 0)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < W_w - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("vvv.png", self.rect.centerx, self.rect.top, 55, 40, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > W_h:
            self.rect.x = randint(80, W_w - 80)
            self.rect.y = 0
            self.speed = randint(1, 7)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()


ship = Player("crow.jpg", 5, W_h - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("met.jpg", randint(80, W_w - 80), - 40, 80, 50, randint(1, 7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy("mich.jpg", randint(80, W_w - 80), - 40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)


run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fs.play()
                ship.fire()
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Счёт:" + str(score), 1, (41, 71, 87))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (133, 8, 8))
        window.blit(text_lose, (10, 60))

        ship.update()
        monsters.update()
        ship.reset()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("met.jpg", randint(80, W_w - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(mls, (200, 200))
        if sprite.spritecollide(ship, asteroids, False):
            finish = True
            window.blit(mls, (200, 200))
        if score >= goal:
            finish = True
            jnjr.reset()

        display.update()
        
    time.delay(50)