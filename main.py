# Copyright (C) 2018 Marien Raat <marienraat@riseup.net>

# Author: Marien Raat <marienraat@riseup.net>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import os, sys
import pygame
import math
from pygame.locals import *
import random

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def draw_score():
    #change highscore color if same as current score
    if highscore == score:
        highscore_color = (255,255,128)
    else:
        highscore_color = (150,150,150)
    score_text = score_font.render(str(score),1,(245,245,245))
    multiplier_text = multiplier_font.render( "x" + str(score_multiplier)
                                            , 1 , (150,150,150))
    highscore_text = multiplier_font.render( "Highscore: " + str(highscore)
                                      , 1, highscore_color)
    screen.blit(score_text,(0, 0))
    screen.blit(highscore_text,(0 , 50))
    lifes_text = multiplier_font.render("Lifes: " + str(lifes),1,(0, 255, 0))
    screen.blit(lifes_text, (330, 0))

def spawn_food(food, food_group):
    t = random.randrange(0, 3)
    newfood = pygame.sprite.Sprite()
    newfood.image = pygame.Surface([50, 50])
    newfood.t = t
    if t == 0:
        newfood.image.fill((255, 0, 0))
    elif t == 1:
        newfood.image.fill((0, 255, 0))
    else:
        newfood.image.fill((255, 255, 0))
    newfood.rect = newfood.image.get_rect()
    newfood.rect.x = random.randrange(0, 350)
    newfood.rect.y = 0
    newfood.y = 0.0
    newfood.dead = False
    food.append(newfood)
    food_group.add(newfood)
    
    
while True:
    pygame.init()
    screen_width = 400
    screen_height = 800
    
    score = 0
    score_multiplier = 1
    score_font = pygame.font.Font("Munro.ttf", 48)
    multiplier_font = pygame.font.Font("Munro.ttf", 24)

    # Get the highscore
    highscore_fname = ".highscore"
    if os.path.isfile(highscore_fname):
        highscore_file = open(highscore_fname, 'r')
        highscore = int(highscore_file.read())
        highscore_file.close()
    else:
        highscore = 0
        highscore_file = open(highscore_fname, 'w')
        highscore_file.write("0")
        highscore_file.close()
    
    screen = pygame.display.set_mode([screen_width,screen_height])
    pygame.display.set_caption('stoplicht')
    background = pygame.Surface(screen.get_size())
    background = background.convert();
    background.fill((0,0,0))

    moving_sprites = pygame.sprite.Group()
    gate_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()

    # Hit flash sprite
    hit_flash = pygame.sprite.Sprite()
    hit_flash.image = pygame.Surface([screen_width,screen_height])
    hit_flash.image.set_alpha(0)
    hit_flash.image.fill((255,100,100))
    hit_flash.rect = hit_flash.image.get_rect()
    hit_flash_opacity = 0

    flash_group = pygame.sprite.Group()
    moving_sprites.add(hit_flash)
    flash_group.add(hit_flash)

    # gate
    gate = pygame.sprite.Sprite()
    gate.image = pygame.Surface([400, 200])
    gate.image.fill((255, 255, 0))
    gate.rect = gate.image.get_rect()
    gate.rect.x = 0
    gate.rect.y = 600
    gate_group.add(gate)

    # food
    food = []
    food_counter = 0

    # state
    yes = False
    no = False
    lifes = 3

    # variables
    movement_speed = 250
    drop_time = 0.8

    clock = pygame.time.Clock()

    done = False
    
    while not done and lifes > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()

            #Input handling
            if event.type == pygame.KEYDOWN and event.key == K_a:
                yes = True
            if event.type == pygame.KEYUP and event.key == K_a:
                yes = False
            if event.type == pygame.KEYDOWN and event.key == K_s:
                no = True
            if event.type == pygame.KEYUP and event.key == K_s:
                no = False
    
        screen.fill((0,0,0))

        if score > highscore:
            highscore = score

        # Gate
        if yes and not no:
            gate.image.fill((0, 255, 0))
        elif no and not yes:
            gate.image.fill((255, 0, 0))
        else:
            gate.image.fill((255, 255, 0))

        # Food
        food_counter += 1 / 60
        if food_counter > drop_time:
            spawn_food(food, food_group)
            food_counter -= drop_time
        for f in food:
            f.y += movement_speed / 60.0
            f.rect.y = int(f.y)
            if f.rect.y > 600:
                g = (f.t == 0 and not yes and no) or (f.t == 1 and yes and not no) or (f.t == 2 and not yes and not no)
                if g:
                    score += 100
                    f.dead = True
                else:
                    lifes -= 1
                    f.dead = True

        food = [f for f in food if not f.dead]
        
        # Draw
        food_group.draw(screen)
        gate_group.draw(screen)
        draw_score()

        if hit_flash_opacity > 0:
            hit_flash_opacity = hit_flash_opacity - 5

        hit_flash.image.set_alpha(hit_flash_opacity)
        flash_group.draw(screen)
    
        pygame.display.flip()
        clock.tick(60)
