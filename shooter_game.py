from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
 
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('i1.jpg', self.rect.centerx, self.rect.top, 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            global missed
            missed += 1
            self.rect.y = 0
            self.rect.x = randint(0, win_width)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
#Игровая сцена:
win_width = 1000
win_height = 700
window = display.set_mode((1000, 700))
display.set_caption("Maze")
background = transform.scale(image.load("1.jpg"), (win_width, win_height))

#Персонажи игры:
player = Player('21.jpg', 5, win_height - 80, 15)

bullets = sprite.Group()

enemies = sprite.Group()
for i in range(5):
    e1 = Enemy('8.jpg', randint(0, win_width), 0, randint(1, 4))
    enemies.add(e1)
game = True
finish = False
clock = time.Clock()
FPS = 60
missed = 0 
clear = 0
patrons = 20
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial',30)
win_txt = font1.render('YOU WIN!', True, (184, 98, 1))
lose_txt = font1.render('YOU LOSE!', True, (1, 98, 184))
while game:
    window.blit(background,(0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and patrons >= 1:
            if e.key == K_SPACE:
                player.fire()
                fire_sound.play()
                patrons -= 1
    if finish != True:

   
        text_clear = font1.render(
            'Убито:' + str(clear), True, (255, 255, 88)
        )

        text_missed = font1.render(
            'Пропущенно:' + str(missed), True, (255, 255, 88)
        )
        text_patr = font1.render(
            'Патроны:' + str(patrons), True, (255, 255, 88)
        )
        sprite_list = sprite.groupcollide(
            enemies, bullets, True, True
        )
        sprite_list_e1_player = sprite.spritecollide(
            player, enemies, False
        )        
        for i in sprite_list:
            clear += 1
            e1 = Enemy('8.jpg', randint(0, win_width), 0, randint(1, 4))
            enemies.add(e1)

        window.blit(text_missed, (50, 50))
        window.blit(text_clear, (50, 80))
        window.blit(text_patr, (50, 110))        
        bullets.update()
        bullets.draw(window)
        player.reset()
        player.update()
        enemies.update()
        enemies.draw(window)
        if sprite.spritecollide(player, enemies, False) or missed >= 3:
            finish = True
            window.blit(lose_txt, (win_width/2, win_height/2))
        if clear >= 10:
            finish = True 
            window.blit(win_txt, (win_width/2,win_height/2))
        display.update()
        clock.tick(FPS)

