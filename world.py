#!/usr/bin/env python
"""This is the game World for pylaga

Arguably the most important class, this is the game object--
it *is* the game...in an object.
world.py (formerly game.py)
"""

__author__ = ("2007-02-20 Derek Mcdonald (original),"
              " 2007-04-1 RJ Marsan,"
              " 2018 poikilos (Jake Gustafson)")
__version__ = '0.2.1'
__all__ = []

import pygame
import os
import sys
import math
import random
import time
from pygame.locals import*
from background import BackgroundManager
from entity import Entity, Swarm
from stage import Stage
from hud import Blip, Hud
from menu import Menu
from menus import Menus
#    import ecollision

if not pygame.font:
    print('Warning, fonts disabled')

try:
    input = raw_input
except:
    pass  # python3


# Now for the actual game class
class World:
    # This is the __init__
    # its important.
    def __init__(self, app, screen):
        # tock started out random, but now is an important variable.
        # It is a frames count, used for periodic updates on certain
        # frames.
        self.p_max_health = 5
        self.won = False
        self.won_msg = "WINNER!"
        self.particle_ban = False
        self.wait_stop_count = -1  # -1 means do not count
        self.wait_stop_max = 120  # wait this many frames after decay
                                  # before showing menu
        self.tock = 0
        self.stage_e_bullet_odds = 15
        self.mouse_rect = None
        self.temp_rect = None
        self.app = app
        self.screen = screen
        self.app.music_name = "intro.ogg"
        # self.app.continue_music()
        if self.app.settings['music']:
            # self.app.music_loaded = self.app.music_name
            # pygame.mixer.music.load(self.app.resource_find(
            #     self.music_name))
            # pygame.mixer.music.play()  # plays once PLUS repeats param
            pass
        left_border = 50
        right_border = 50
        w, h = screen.get_size()
        self.world_rect = pygame.Rect(left_border, 0,
                                      w-right_border-left_border, h)
        self.bg = BackgroundManager(self.world_rect)

        # Yay spritegroups! They make the world go round, and iterate.
        # Basically each visible game object resides in its own special
        # spritegroup & then all one needs to do is go through these &
        # call functions & stuff.
        # It makes sense in here *points to brain*
        self.p_swarm = Swarm(self.world_rect)
        self.particles = Swarm(self.world_rect)

        self.explosion_images = self.app.load_seq('ex-medium')
        self.shield_hit_images = self.app.load_seq('shield_hit-tiny')
        self.damage_images = self.app.load_seq('ex-tiny')

        # Load player sprite as image list.
        self.p_unit_images = self.app.load_seq('pship')
        # self.p_unit_images = []
        # self.p_unit_images.append(self.load_file('pship.png'))
        # self.p_unit_images.append(self.load_file('pship1.png'))
        # self.p_unit_images.append(self.load_file('pship2.png'))
        # self.p_unit_images.append(self.load_file('pship3.png'))

        # Load enemy ship image.
        self.e_ship_image = self.load_file('eship.png')
        if self.app.settings['sounds']:
            self.p_shoot_sound = self.app.load_file('p-weapon0.wav',
                                                    file_type='sound')
            self.p_shoot_sound.set_volume(.3)
            self.e_ex_sound = self.app.load_file('e-ex.wav',
                                                 file_type='sound')
            self.p_ex_sound = self.app.load_file('p-ex.wav',
                                                 file_type='sound')
            self.e_damage_sound = self.app.load_file('e-damage.wav',
                                                     file_type='sound')
            self.e_shield_sound = self.app.load_file('e-shield.wav',
                                                     file_type='sound')
            self.p_shield_sound = self.app.load_file('p-shield.wav',
                                                     file_type='sound')
            self.p_damage_sound = self.app.load_file('p-damage.wav',
                                                     file_type='sound')
            print("loaded sounds...")
        self.menus = None
        self.tock = 0
        self.lagcount = 0
        self.leftkeydown = 0
        self.rightkeydown = 0
        # self.enemylist = []  # list of dirty rects
        self.swarm = Swarm(self.world_rect,
                           shoot_odds=self.stage_e_bullet_odds)
        self.stage = Stage(self.swarm, self.p_swarm)

        self.p_shot_image = self.load_file('p-laser.png')
        self.e_shot_image = self.load_file('e-laser.png')

        self.p_bullet_swarm = Swarm(self.world_rect)
        self.e_bullet_swarm = Swarm(self.world_rect)
        # self.bullet_width = 10
        self.hud_rect = pygame.Rect(0, 0, 5, 150)
        self.hud = Hud()
        self.hud.generate_blip('player.score', 100,
                               fg_color=(255,243,207),
                               text_color=(192,180,180),
                               caption="SCORE")
        self.hud.generate_blip('player.health', self.p_max_health,
                               fg_color=(0,255,42),
                               text_color=(192,180,180),
                               caption="SHIELD")
        self.statcounter = self.hud.get_blip('player.score')

    def load_file(self, name):
        return self.app.load_file(name)

    def on_exit(self):
        print("on_exit...")

    # Clears all the variables
    def clear_vars(self):
        # print("clear_vars: world_rect: " + str(self.world_rect))
        self.p_start_x = self.world_rect.width / 2
        self.p_start_y = self.world_rect.height - 60
        self.bend_y = float(self.p_start_y)
        # print("clear_vars: p_start_y: " + str(self.p_start_y))
        self.bend_rate = 0.02
        self.leftkeydown = 0
        self.rightkeydown = 0
        if self.p_unit is not None:
            self.hud.set_blip_value('player.health', self.p_unit.health)
        else:
            print("WARNING: clear_vars failed to set bar since no" +
                  " player unit exists")
        self.statcounter.set_val(0)
        self.stage.set_stage_number(-1)  # hax
        self.stage_e_bullet_odds = 100
        self.swarm.empty()
        self.p_bullet_swarm.empty()
        self.p_swarm.empty()
        self.particles.empty()
        self.e_bullet_swarm.empty()

    # Define function to draw player ship on X, Y plane
    def draw_player_units(self):
        self.p_swarm.draw(self.screen)

    # Define function to move the enemy ship
    def emove(self):
        self.swarm.draw(self.screen)  # use spritegroup draw method

    # Draws all the enemys you ask it
    def generate_enemies(self):
        print("generating enemies...")
        # Some recursive loops:
        xmin = self.world_rect.left
        xmax = self.world_rect.right
        ymin = self.world_rect.top
        stage_data = self.stage.get_data()
        self.e_ship_image = self.app.load_file(stage_data['e']+".png")
        enemy_width, enemy_height = self.e_ship_image.get_size()
        enemy_spacing_x = 15
        enemy_spacing_y = 10
        init_enemy_speed = 3
        angle = -90  # cartesian

        self.app.music_name = stage_data['music']
        # if self.app.music_name == 'intro.ogg':
            # self.app.continue_music()  # force song change
        e_max_health = stage_data['e_h']
        for enemycol in range(stage_data['x_e_count']):
            # Now for the rows
            for enemyrow in range(stage_data['y_e_count']):
                # Make a new enemy object:
                new_enemy = Entity(self.app,
                                  'eship', [self.e_ship_image],
                                  init_enemy_speed, angle,
                                  self.swarm, e_max_health,
                                  self.explosion_images, self.particles,
                                  ai_enable=True,
                                  value=stage_data['e_h'],
                                  ex_sound=self.e_ex_sound)
                new_enemy.set_xy(
                    xmin +
                    enemycol * (enemy_width +
                                enemy_spacing_x),
                    ymin +
                    enemyrow * (enemy_height +
                                enemy_spacing_y) - 150
                )
                new_enemy.set_range(
                    xmin +
                    enemycol * (enemy_width +
                                enemy_spacing_x),
                    xmax -
                    (stage_data['x_e_count'] - enemycol) *
                    (enemy_height +
                     enemy_spacing_x)
                )

                # Now add the temp enemy to the array and we're good to
                # go
                self.swarm.add(new_enemy)

    # So I'm trying out having the program check for collisions, instead
    # of the enemy objects i think i might switch to the objects, but
    # still keep this function just hand the computing to the object
    def test_collision(self):
        part_speed = 1
        part_angle = -90
        part_health = 1
        e_hit = pygame.sprite.groupcollide(self.swarm,
                                           self.p_bullet_swarm,
                                           0, 0)
        for sprite, bullets in e_hit.items():
            # print("removed " + str(bullet)
            for bullet in bullets:
                was_alive = sprite.get_is_alive()
                prev_health = sprite.health
                if sprite.get_is_alive():
                    sprite.set_hit(1)
                damage = prev_health - sprite.health
                poof = self.shield_hit_images
                temper_sound = self.e_shield_sound
                if damage > 0:
                    poof = self.damage_images
                    temper_sound = self.e_damage_sound
                if not was_alive:
                    break
                point = pygame.sprite.collide_mask(sprite,
                                                   bullet)
                if ((point is not None) and
                        (not self.particle_ban)):
                    particle = Entity(self.app, 'particle',
                                      poof,
                                      part_speed,
                                      part_angle, self.particles,
                                      part_health,
                                      None,
                                      None,
                                      anim_done_remove=True,
                                      temper_sound=temper_sound)
                    particle.temper = 1  # start particle death
                    x1, y1 = sprite.get_pos()  # top left
                    x = x1 + point[0] - particle.rect.width / 2
                    y = y1 + point[1] - particle.rect.height / 2
                    particle.set_xy(x, y)
                    self.particles.add(particle)
            if not sprite.get_is_alive():
                points = sprite.take_value()  # only once & if health 0
                if points > 0:
                    self.statcounter.add_value(points)
            self.p_bullet_swarm.remove(bullets)



        p_hit = pygame.sprite.groupcollide(self.p_swarm,
                                           self.e_bullet_swarm,
                                           0, 0)
        for sprite, bullets in p_hit.items():
            for bullet in bullets:
                was_alive = sprite.get_is_alive()
                prev_health = sprite.health
                if sprite.get_is_alive():
                    sprite.set_hit(1)
                damage = prev_health - sprite.health
                poof = self.shield_hit_images
                temper_sound = self.p_shield_sound
                if damage > 0:
                    poof = self.damage_images
                    temper_sound = self.p_damage_sound
                    self.hud.set_blip_value('player.health',
                                            self.p_unit.health)
                # New in pygame 1.8.0:
                point = pygame.sprite.collide_mask(sprite, bullet)
                if not was_alive:
                    break
                if (point is not None) and (not self.particle_ban):
                    particle = Entity(self.app, 'particle',
                                      poof,
                                      part_speed,
                                      part_angle, self.particles,
                                      part_health,
                                      None,
                                      None,
                                      anim_done_remove=True,
                                      temper_sound=temper_sound)
                    particle.temper = 1  # start particle death
                    x1, y1 = sprite.get_pos()  # top left
                    x = x1 + point[0] - particle.rect.width / 2
                    y = y1 + point[1] - particle.rect.height / 2
                    particle.set_xy(x, y)
                    self.particles.add(particle)

        # if pygame.sprite.spritecollideany(self.p_unit,
                                          # self.e_bullet_swarm):
            # self.p_unit.set_hit(1)
            # self.hud.set_blip_value('player.health',
            #                         self.p_unit.health)

    # if there are no enemys left, go to the next stage
    def check_done(self):
        if not self.swarm:
            if self.stage.is_last_stage():
                if not self.won:
                    self.won = True  # TODO: make ending screen
                    # self.app.music_name = 'victory.ogg'
                    # if self.app.music_name == 'intro.ogg':
                        # self.app.continue_music()  # force song change
                    self.app.music_name = None  # stop repeating
                    self.app.check_music() # apply None to loop
                    self.app.queue_music('victory.ogg', 1)
            if not self.won:
                self.stage.next_stage()
                if self.stage_e_bullet_odds > 15:
                    self.stage_e_bullet_odds -= 15
                self.generate_enemies()

    # checks to see if we can expand the ranges of the bots so its nice
    # and.... umm... nice.
    def check_rows(self):
        if self.tock % 20 == 0:
            # simple sorting algorithm to find the highest values
            xmin = self.world_rect.left
            xmax = self.world_rect.right
            highest = xmin
            lowest = xmax
            for enemy in self.swarm:
                if enemy.get_range()[1] > highest:
                    highest = enemy.get_range()[1]
                if enemy.get_range()[0] < lowest:
                    lowest = enemy.get_range()[0]
            highest = xmax - highest
            lowest = lowest - xmin
            if highest != 0 or lowest != 0:
                    # makes things |--| this much more efficient
                for enemy in self.swarm:
                    erange = enemy.get_range()
                    enemy.set_range(erange[0]-lowest,
                                    erange[1]+highest)

    # major hack just to get this thing playable..... sorry
    def again(self):
        if self.hud.get_blip_value('player.health') <= 0:
            self.particle_ban = True
        if self.p_unit.get_is_decayed():
            self.particle_ban = True
            # also wait for particles to finish for prettier ending
            if len(self.particles) < 1:
                if self.wait_stop_count < 0:
                    print("player unit decayed, counting down to menu")
                    self.wait_stop_count = 0
                # return False
        if self.wait_stop_count >= 0:
            self.wait_stop_count += 1
            if self.wait_stop_count > self.wait_stop_max:
                return False
        if self.won:
            if self.wait_stop_count < 0:
                print("won game, counting down to menu")
                self.wait_stop_count = 0
        return True

    # this is called if the player initiates shooting
    def pshoot(self):
        # sx = self.p_unit.rect.centerx -
        #      self.p_shot_image.rect.width / 2
        # sy = self.p_unit.rect.top +
        #      self.p_shot_image.rect.height * .75
        if self.p_unit.get_is_alive():
            self.p_unit.shoot(self.p_shot_image,
                              self.p_bullet_swarm)
            # self.p_unit.shoot_from(self.p_shot_image,
            #                        self.p_bullet_swarm,
            #                        sx, sy, self.p_unit.angle)

    def draw_bullets(self):
        self.p_bullet_swarm.draw(self.screen)
        self.e_bullet_swarm.draw(self.screen)

    def draw_hud(self):
        if self.tock % 5 == 0:
            self.hud.update()
        self.hud.draw(self.screen)

    # Goes through all the objects and makes each of them move as
    # necessary
    def tick(self):
        self.bend_y += self.bend_rate
        bend_max = 5.0
        if self.bend_rate < 0.0:
            self.bend_rate -= .02
        else:
            self.bend_rate += .02
        if ((self.bend_y > self.p_start_y + bend_max) or
            (self.bend_y < self.p_start_y)):
            if self.bend_rate < 0.0:
                self.bend_rate = .02
                self.bend_y = float(self.p_start_y)
            else:
                self.bend_rate = -.02
                self.bend_y = float(self.p_start_y) + bend_max
        self.p_unit.set_xy(self.p_unit.get_pos()[0],
                           int(self.bend_y+.5))
        self.p_bullet_swarm.update()
        self.swarm.update()
        self.e_bullet_swarm.update()

    ######################
    # Here are a bunch of metafunctions.
    # I break it up so its really easy to add new features,
    # like if we ant a counter? add something to check() and draw().
    # All of these are called once per frame.
    def check(self):
        self.check_done()
        self.test_collision()
        self.check_rows()
        self.bg.update()
        if self.p_unit.get_is_alive():
            self.swarm.shoot(self.e_shot_image, self.e_bullet_swarm)
        self.p_unit.update()
        for particle in self.particles:
            particle.update()

    def draw(self):
        self.screen.fill(self.bg.bg_color)
        # if self.world_rect is not None:
            # self.screen.fill((64, 64, 64), self.world_rect)
        self.bg.draw(self.screen)
        self.draw_bullets()
        self.draw_player_units()
        self.emove()
        self.particles.draw(self.screen)
        self.draw_hud()
        # if self.p_unit is not None:
            # if self.p_unit.rect is not None:
                # self.screen.fill((128, 128, 128), self.p_unit.rect)
        # if self.mouse_rect is not None:
            # self.screen.fill((255, 255, 255), self.mouse_rect)
        # if self.temp_rect is not None:
            # self.screen.fill((128, 0, 0), self.temp_rect)


    # does just what it sounds like.....
    def clear_screen(self):
        self.screen.fill(self.bg.bg_color)
        # pygame.display.flip()

    # for debugging info mostly
    def dispvars(self):
        print("The Enemy SpriteGroup size is:" +
              str(len(self.swarm.sprites())))
        print("The Player Bullet Array size is:" +
              str(len(self.p_bullet_swarm.sprites())))
        print("The Enemy Bullet Array size is:" +
              str(len(self.e_bullet_swarm.sprites())))

    # does lots and lots of stuff, it really needs to be cleaned up
    def process_events(self, events):
        # print("input: self.p_unit.rect: " + str(self.p_unit.rect))
        xmin = self.world_rect.left
        xmax = self.world_rect.right
        smooth_scroll_var1 = 10
        smooth_scroll_var2 = 2
        pygame.event.pump()  # redraw Window so OS knows not frozen
        self.app.check_music()
        pause_menu_strings = ["RESUME", "ABOUT", "HELP", "EXIT"]
        if self.won:
            pause_menu_strings.insert(0, self.won_msg)
        for event in events:
            if event.type == QUIT:
                self.on_exit()
                sys.exit(0)

            if event.type == pygame.MOUSEMOTION:
                pygame.event.get()
                prev_pos = self.p_unit.get_pos()
                tempx = (pygame.mouse.get_pos()[0] -
                         self.p_unit.rect.width / 2)
                # *Just to make sure we don't get the ship way out:
                if tempx + self.p_unit.rect.width > xmax:
                    # if its outside the world,
                    # just stick it as far as possible
                    self.p_unit.set_xy(xmax - self.p_unit.rect.width,
                                       prev_pos[1])
                elif tempx < xmin:
                    self.p_unit.set_xy(xmin, prev_pos[1])
                elif abs(tempx-self.p_start_x) > \
                        smooth_scroll_var1:
                    # smooth scrolling if the mouse gets far
                    # from the ship
                    self.p_unit.set_xy(
                        prev_pos[0] +
                        (tempx-prev_pos[0]) /
                        smooth_scroll_var2,
                        prev_pos[1])
                else:
                    # if it gets down to this point,
                    # we've passed all sanity checks so just move it
                    self.p_unit.set_xy(tempx, prev_pos[1])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.pshoot()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.menus.show_dialog(pause_menu_strings)
                if event.key == pygame.K_p:
                    self.menus.show_dialog(pause_menu_strings)
                if event.key == pygame.K_ESCAPE:
                    self.menus.show_dialog(pause_menu_strings)
                # keyboard controls
                if event.key == pygame.K_LEFT:
                    self.leftkeydown = 1
                if event.key == pygame.K_RIGHT:
                    self.rightkeydown = 1
                if event.key == pygame.K_SPACE:
                    self.pshoot()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.leftkeydown = 0
                if event.key == pygame.K_RIGHT:
                    self.rightkeydown = 0
            elif event.type == pygame.USEREVENT:
                if event.code == pygame.USEREVENT_DROPFILE:
                    print("Tried to open file on MacOS (this should" +
                          " never happen:")
                    print("  " + str(event))
                else:  # should be event.code 0
                    self.app.continue_music()
                    print("music queue ended in game:")
                    if event.code != 0:
                        print("unknown USEREVENT event.code: " +
                              str(event.code))

        if self.leftkeydown:
            self.p_unit.move_one(-1, self.world_rect)
        if self.rightkeydown:
            self.p_unit.move_one(1, self.world_rect)

        pygame.event.clear()

    ####################################################################

    def start(self, menus):
        self.won = False
        self.particle_ban = False
        self.wait_stop_count = -1  # -1 means do not count down to menu
        self.menus = menus
        p_speed = 10
        self.p_unit = Entity(self.app, 'pship', self.p_unit_images,
                             p_speed, 90.0,
                             self.p_swarm, self.p_max_health,
                             self.explosion_images,
                             self.particles,
                             ex_sound = self.p_ex_sound)
        self.p_unit.shoot_sound = self.p_shoot_sound
        print("Clearing vars...")
        self.clear_vars()  # does reset player unit (p_unit) position
        self.p_swarm.add(self.p_unit)
        self.p_unit.set_xy(self.p_start_x, self.p_start_y)
        print("Starting main event loop...")
        self.loop()

    # Yeah see this one does all of the work
    def loop(self):
        # Start loop
        REFRESH_TIME = self.app.get_fps() * 3
        while (not self.menus.get_bool('exit')) and (self.again()):
            # Refresh screen periodically
            if self.tock >= REFRESH_TIME:
                # self.clear_screen()
                self.tock = 0
            self.tock += 1

            # Check everythign and see if changes need to be made
            self.check()

            # Draw bullets
            self.draw()

            # Move everything
            self.tick()

            # Initiate input function
            self.process_events(pygame.event.get())

            # applies the smart screen updating
            pygame.display.update()
            # TODO: ? pygame.display.update(self.enemylist)
            # self.enemylist = []

            # Pauses and waits
            timeittook = self.app.clock.tick(self.app.get_fps())
            # if timeittook > 1000/self.app.get_fps():
            #   # print("LAG:" + str(self.lagcount) + " at " +
            #         # str(timeittook) + "ms")
            #   # self.dispvars()
            #   # self.lagcount += 1
            # print self.app.clock.get_fps()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    msg = "run main.py instead."
    print(msg)
    font = pygame.font.Font("freesansbold.ttf", 40)
    msg_img = font.render(msg, True, (192, 192, 192))
    msg_rect = msg_img.get_rect()
    msg_rect.move_ip(10, 5)
    msg_img.set_alpha(10)
    screen.blit(msg_img, (msg_rect.x, msg_rect.y))
    pygame.display.flip()
    run = False
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                # self.on_exit()
                run = False
    time.sleep(2)
