import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

# Player character
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = game.player_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH -32, HEIGHT - 32)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.image_original = self.image
        self.rot = 0
        self.direction = 'north'
        # set a mask for collision
        self.mask = pg.mask.from_surface(self.image)


    def update(self):
        # Check which keys are down to apply rotation to the sprite

        self.acc = vec(0, 0)
        # movement left and right
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            if self.rot < 90 or self.rot >= 270:
                self.rot += 10
                if self.rot >= 360:
                    self.rot = 0
            elif self.rot > 90 and self.rot < 270:
                self.rot -= 10
            
            if self.rot == 85 or self.rot == 95:
                self.rot = 90

            self.rotate()
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            if self.rot < 270 and self.rot >= 90:
                self.rot += 10
            elif self.rot > 270 or self.rot < 90:
                self.rot -= 10
                if self.rot < 0:
                    self.rot = 360
            
            if self.rot == 265 or self.rot == 275:
                self.rot = 270
            
            self.rotate()
        # movement up and down
        if keys[pg.K_w]:
            self.acc.y = -PLAYER_ACC
            if self.rot <= 180 and self.rot > 0:
                self.rot -= 10
            elif self.rot > 180:
                self.rot += 10
                if self.rot > 360:
                    self.rot = 0
            
            if self.rot == 5 or self.rot == -5:
                self.rot = 0
                
            self.rotate()
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
            if self.rot < 180:
                self.rot += 10
            elif self.rot > 180:
                self.rot -= 10
            
            if self.rot == 175 or self.rot == 185:
                self.rot = 180
                
            self.rotate()

        # check for diagonal rotation
        if keys[pg.K_a] and keys[pg.K_w]:
            if self.rot < 45:
                self.rot += 10
            elif self.rot > 45:
                self.rot -= 10
            
            if self.rot == 40 or self.rot == 50:
                self.rot = 45

            self.rotate()
        if keys[pg.K_a] and keys[pg.K_s]:
            if self.rot < 135:
                self.rot += 10
            elif self.rot > 135:
                self.rot -= 10
            
            if self.rot == 130 or self.rot == 140:
                self.rot = 135
                
            self.rotate()
        if keys[pg.K_s] and keys[pg.K_d]:
            if self.rot < 215:
                self.rot += 10
            elif self.rot > 215:
                self.rot -= 10
            
            if self.rot == 210 or self.rot == 220:
                self.rot = 215
            
            self.rotate()
        if keys[pg.K_d] and keys[pg.K_w]:
            if self.rot < 315 and self.rot >= 135:
                self.rot += 10
            elif self.rot > 315:
                self.rot -= 10
            elif self.rot < 135:
                self.rot -= 10
                if self.rot <= 0:
                    self.rot = 360
            
            if self.rot == 320 or self.rot == 310:
                self.rot = 315
            
            self.rotate()
        
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        #if abs(self.vel.x) < 0.1:
        #    self.vel.x = 0
        self.pos += (self.vel + 0.5 * self.acc)

        # hit borders of the screen
        if self.pos.x + (self.rect.width / 2) > WIDTH:
            self.pos.x = WIDTH - (self.rect.width / 2)
        if self.pos.x - (self.rect.width / 2) < 0:
            self.pos.x = 0 + (self.rect.width / 2)
        if self.pos.y + (self.rect.height / 2) > HEIGHT:
            self.pos.y = HEIGHT - (self.rect.width / 2)
        if self.pos.y - (self.rect.height /2) < 0:
            self.pos.y = 0 + (self.rect.width / 2)

        self.rect.center = self.pos

        self.mask = pg.mask.from_surface(self.image)
   
    def rotate(self):
        new_image = pg.transform.rotate(self.image_original, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.mask = pg.mask.from_surface(self.image)

class Island(pg.sprite.Sprite):
    def __init__(self, game, island_counter):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        if island_counter == 0:
            self.image = game.large_island_image.convert()
            self.image.set_colorkey(BLUE)
        elif island_counter == 1 or island_counter == 2:
            self.image = game.medium_island_image.convert()
            self.image.set_colorkey(BLUE)
        elif island_counter > 2:
            self.image = game.small_island_image.convert()
            self.image.set_colorkey(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - 200)
        self.rect.y = random.randrange(0, HEIGHT - 200)
        self.mask = pg.mask.from_surface(self.image)
    
class Treasure(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10,10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, WIDTH - 30)
        self.rect.centery = random.randrange(0, HEIGHT - 30)

class Arrow(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg.sprite.Sprite.__init__(self)
        self.image = game.arrow_image.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image_original = self.image
        self.state = 'hidden'
        self.last_spawn = 0

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_spawn > 1000:
            self.state = 'hidden'

    def rotate(self, degs):
        new_image = pg.transform.rotate(self.image_original, degs)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.mask = pg.mask.from_surface(self.image)
