# Fantasy Captain

import pygame as pg
import random
import math
from settings import *
from sprites import *
from os import *

class Game:
    def __init__(self):
        # initalize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(CAPTION)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.distance = 0
        self.last_arrow_spawn = 0

    def load_data(self):
        # load all the data for the game before it starts
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        snd_dir = path.join(self.dir, 'snd')

        # load the images
        self.player_image = pg.image.load(path.join(img_dir, PLAYER_IMAGE)).convert()
        self.small_island_image = pg.image.load(path.join(img_dir, SMALL_ISLAND_IMAGE)).convert()
        self.medium_island_image = pg.image.load(path.join(img_dir, MEDIUM_ISLAND_IMAGE)).convert()
        self.large_island_image = pg.image.load(path.join(img_dir, LARGE_ISLAND_IMAGE)).convert()
        self.arrow_image = pg.image.load(path.join(img_dir, ARROW_IMAGE))

        # load the font
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game / reset everything
        self.all_sprites = pg.sprite.Group()
        self.islands = pg.sprite.Group()
        self.treasures = pg.sprite.Group()
        self.arrows = pg.sprite.Group()

        # create the player character
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # create the islands
        island_counter = 0
        while island_counter < NUMBER_OF_ISLANDS:
            i = Island(self, island_counter)
            hits = pg.sprite.spritecollide(i, self.islands, False)
            if not hits:
                self.islands.add(i)
                self.all_sprites.add(i)
                island_counter += 1
            else:
                i.kill()
        
        # create the treasure
        self.treasure = Treasure(self)
        while pg.sprite.spritecollide(self.treasure, self.islands, True):
            self.treasure = Treasure(self)
        self.all_sprites.add(self.treasure)
        self.treasures.add(self.treasure)

        # create the arrow
        self.arrow = Arrow(self)
        self.arrows.add(self.arrow)

        self.run()

    def run(self):
        # game loop

        self.playing = True
        while self.playing:
            # Keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)
            self.events()
            # Update everything
            self.update()
            # Draws everything after updating
            self.draw()

    def update(self):
        # game loop update
        self.all_sprites.update()
        self.arrows.update()

        # check for collision between player and islands
        if pg.sprite.spritecollide(self.player, self.islands, False):
            mask_hits = pg.sprite.spritecollide(self.player, self.islands, False, pg.sprite.collide_mask)
            if mask_hits:
                self.playing = False

    def events(self):
        # game loop events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    if not pg.sprite.spritecollide(self.player, self.treasures, False):
                        # set the arrow to visible
                        self.arrow.state = 'visible'
                        self.arrow.last_spawn = pg.time.get_ticks()
                        # get the angle between the arrow and the treasure
                        self.arrow.rect.x = self.player.rect.x
                        self.arrow.rect.y = self.player.rect.y
                        angle = math.atan2(self.arrow.rect.centerx - self.treasure.rect.centerx, self.arrow.rect.centery - self.treasure.rect.centery)
                        angle %= 2*math.pi
                        angle = math.degrees(angle)
                        # add the variance to the angle based on distance
                        self.distance = math.sqrt((self.player.rect.centerx - self.treasure.rect.centerx)**2 + (self.player.rect.centery - self.treasure.rect.centery)**2)
                        if self.distance > 300:
                            arrow_variance_min = -45
                            arrow_variance_max = 45
                        elif self.distance <= 300 and self.distance > 100:
                            arrow_variance_min = -20
                            arrow_variance_max = 20
                        elif self.distance <= 100:
                            arrow_variance_min = -1
                            arrow_variance_max = 1
                        final_angle = angle + random.randrange(arrow_variance_min, arrow_variance_max)
                        # rotate the arrow to point at the treasure
                        self.arrow.rotate(final_angle)
                    else:
                        self.playing = False


    def draw(self):
        # game loop draw
        # Draw / render
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        current_time = pg.time.get_ticks()
        if self.arrow.state == 'visible':
            self.arrows.draw(self.screen)
        #self.draw_text(str(self.treasure.rect.centerx) + " " + str(self.treasure.rect.centery), 48, WHITE, WIDTH / 2, 24)
        #self.draw_text(str(self.hits[2]), 48, WHITE, WIDTH / 2, HEIGHT - 48)
        #self.draw_text(str(degs), 48, WHITE, WIDTH / 2, 24)
        self.draw_text(str(self.distance), 48, WHITE, WIDTH / 2, 24)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # show splash/start screen
        pass
    
    def show_go_screen(self):
        # show game over/continue screen
        pass

    def draw_text(self, text, size, color, x, y):
            font = pg.font.Font(self.font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.centerx = x
            text_rect.centery = y
            self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
