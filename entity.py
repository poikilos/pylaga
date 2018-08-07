"""Entity system for pylaga

The All Important Entity class, and its manager Swarm
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


class Swarm(pygame.sprite.Group):
    def __init__(self, world_rect, shoot_odds=None):
        """Constructor

        Sequential arguments:
        world_rect -- used by Entity constructor

        Keyword arguments:
        shoot_odds -- if not None, then assume AI should be done
        """
        super(Swarm, self).__init__()  # initialize spritegroup
        self.shoot_odds = shoot_odds
        self.world_rect = world_rect.copy()
        self.tock = 0
        self.transition_speed = 5
        self.transition_time = 150 / self.transition_speed
        self.current_transition = 0

    def shoot(self, image, bullet_spritegroup):
        if self.shoot_odds is not None:
            self.tock = random.randint(0, self.shoot_odds)
            if self.tock < len(self):
                self.sprites()[self.tock].shoot(image,
                                                bullet_spritegroup)

    def update(self):  # only call this for enemy swarms
        # TODO: check ai_enabled
        if self.current_transition < self.transition_time:
            for e in self:
                e.motivate(self.transition_speed)
            self.current_transition += 1
        else:
            for e in self:
                e.motivate(0)
        for e in self:
            e.update()


# made into class as of "pylaga" fork
# combined from Bullet, EnemyBullet, Enemy, and PlayerUnit aka Player
# as of poikilos fork
class Entity(pygame.sprite.Sprite):
    # self.world_rect.right
    #   # # come in very handy when there
    # is more than 1 enemy
    # swarm.world_rect.left
    #   # # yeah what the first one said.^^

    def __init__(self, app, what, images, speed, angle, spritegroup,
                 health, explosion_images, particles,
                 offscreen_remove=False, ai_enable=False,
                 anim_done_remove=False, value=1,
                 rotate_surf_enable=True, temper_sound=None,
                 ex_sound=None):
        """Constructor

        Sequential arguments:
        app -- the app passed must at least have the following members:
               self.settings['sounds'] boolean
        images -- surface list: frame 0 normal, others are temper anim
        speed -- pixels per frame
        angle -- cartesian angle (will be flipped to account for screen)
        spritegroup -- doesn't auto add, but removes later when explodes
        explosion_images -- plays when state is 0 or greater

        Keyword arguments:
        offscreen_remove -- terminate if not intersecting world_rect
        """
        super(Entity, self).__init__()  # initialize sprite
        # self.dirty = 2  # 2 is always draw; only for DirtySprite
        self.shoot_sound = None
        self.anim_done_remove = anim_done_remove
        self.parent_what = ''
        self.vector = (0, 0)
        self.angle = angle
        self.temper_delay = 2  # wait this many frames until advancing
                               # hurt animation (self.images frame > 0)
        self.state_delay = 1.5
        self.temper = 0
        self.temper_len = 10  # how long mad after hurt
        self.state = -1
        self.generate_ex = True
        self.desired_vel_x = 0
        self.thrust = 0.0
        self.app = app
        self.what = what
        self.images = images
        self.speed = speed
        self.invisible_i = None
        self.visible = True
        self.removed = False
        self.spritegroup = spritegroup
        self.world_rect = self.spritegroup.world_rect.copy()
            # TODO:? by world_rect ref not copy
        self.health = health
        self.explosion_images = explosion_images
        self.particles = particles
        self.offscreen_remove = offscreen_remove
        self.value = value
        self.ai_enable = ai_enable
        temper_frame = int(self.temper / self.temper_delay)
        self.temper_sound_frame_i = 0
        self.rotate_surf_enable = rotate_surf_enable
        self.temper_sound = temper_sound
        self.ex_sound = ex_sound
        self.play_temper_sound_enable = True
        if self.images is not None:
            self.temper_sound_frame_i = len(self.images) - 1
            if self.rotate_surf_enable:
                self.image = pygame.transform.rotate(
                    self.images[temper_frame],
                    self.angle
                )
            else:
                self.image = self.images[temper_frame]
            self.temper_len = len(self.images)
        else:
            if self.explosion_images is not None:
                self.image = self.explosion_images[0]
                print("WARNING in Entity __init__: silenty degrading " +
                      "to explosion sprite for " + self.what)
            else:
                print("ERROR in Entity __init__: no image for " +
                      self.what)
        if self.image is not None:
            self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def get_v(self):
        if self.value <= 0:
            print("WARNING: value " + str(self.value) + " for " +
                  self.what + " (maybe you already did take_value)")
        return self.value

    def take_value(self):
        ret = 0
        if self.health <= 0:
            ret = self.value
            self.value = 0
        return ret

    def get_is_alive(self):
        return self.health > 0

    def set_visible(self, visible):
        if self.visible is not visible:
            self._update_visibility()
        self.visible = visible

    def _update_visibility(self):
        frame = 0
        if self.state >= 0:
            frame = self.state
        if not self.visible:
            if ((self.invisible_i is None) or
                (self.invisible_i != frame)):
                self.invisible_i = frame
                self.image = pygame.Surface(self.image.get_size(),
                             pygame.SRCALPHA, 32)
                self.image.fill((0,0,0,0))

    def __str__(self):
        return self.what

    def get_dest_rect(self):  # not used for enemy
        return self.rect

    def set_xy(self, x, y):  # not used for enemy
        self.rect.topleft = (x, y)

    def get_pos(self):
        return self.rect.topleft

    def move_one(self, direction, world_rect):  # only used by player
        if direction > 0:
            self.rect.move_ip(self.speed, 0)
            if not self.in_range(world_rect):
                self.rect.move_ip((-1)*self.speed, 0)
        elif direction == 0:
            print("WARNING in move_one: nothing done since value is " +
                  str(direction))
        else:
            self.rect.move_ip((-1)*self.speed, 0)
            if not self.in_range(world_rect):
                self.rect.move_ip(self.speed, 0)

    def in_range(self, range_rect):  # only used by player
        if range_rect.contains(self.rect):
            return True
        return False

    def move_by(self, x, y):
        self.rect.move_ip(x, y)

    # Reduces health and runs non-death-related damage events
    # (see next_state for death). heals if damage is < 0
    def set_hit(self, damage):
        if self.temper < 1:
            self.health -= damage
        self.temper = 1

    def set_health(self, health):
        self.health = health

    def update(self):
        prev_state = self.state
        if self.health <= 0:
            if self.state < 0:
                self.set_state(0)
        if self.temper > 0:
            temper_frame = int(self.temper/self.temper_delay)
            if temper_frame == self.temper_sound_frame_i:
                if self.play_temper_sound_enable:
                    self.play_temper_sound_enable = False
                    if self.temper_sound is not None:
                        if self.app.settings['sounds']:
                            print("playing temper sound " +
                                  str(self.temper_sound))
                            pygame.mixer.Sound.play(self.temper_sound)
            if temper_frame >= len(self.images):
                if self.anim_done_remove:
                    self.spritegroup.remove(self)
                else:
                    self.temper = 0
                    temper_frame = 0
                    if self.images is not None:
                        if self.rotate_surf_enable:
                            self.image = pygame.transform.rotate(
                                self.images[temper_frame],
                                self.angle
                            )
                        else:
                            self.image = self.images[temper_frame]
            else:
                if self.images is not None:
                    if self.rotate_surf_enable:
                        self.image = pygame.transform.rotate(
                            self.images[temper_frame],
                            self.angle
                        )
                    else:
                        self.image = self.images[temper_frame]
                self.temper += 1
        if (self.vector[0] != 0.0) or (self.vector[1] != 0.0):
            # *-1 since vector is cartesian
            self.move_by(int(round(self.vector[0])),
                         -1*int(round(self.vector[1])))
        if (self.offscreen_remove and
            (not self.rect.colliderect(self.world_rect))):
            self.spritegroup.remove(self)
        else:
            self.next_state()
        self._update_visibility()

    def normalized_angle(self, angle):
        ret = math.fmod(angle, 360)
        if ret > 180.0:
            ret = -1 * (360 - ret)
        elif ret < -180.0:
            ret = -1 * (-360 - ret)
        return ret


    def get_cardinal(self, angle):
        ret = 'e'
        angle = math.fmod(angle, 360)
        if angle < 0.0:
            angle = -1 * (-360 - angle)
        if angle < 45.0:
            ret = 'e'
        elif angle < 135.0:
            ret = 'n'
        elif angle < 225.0:
            ret = 'w'
        elif angle < 315:
            ret = 's'
        return ret

    def shoot(self, image, bullet_spritegroup, bullet_speed=10,
              bullet_health=1):
        # not used by player
        if self.shoot_sound is not None:
            if self.app.settings['sounds']:
                pygame.mixer.Sound.play(self.shoot_sound)
        new_bullet = Entity(self.app,
                            self.what+'.bullet', [image],
                            bullet_speed, self.angle,
                            bullet_spritegroup, bullet_health,
                            None, self.particles,
                            offscreen_remove=True)
        x = None
        y = None
        cardinal = self.get_cardinal(self.angle)
        if (cardinal == 'n') or (cardinal == 's'):
            x = (self.rect.left + self.rect.width / 2 -
                 new_bullet.rect.width / 2)
            if cardinal == 'n':
                y = self.rect.top + new_bullet.rect.height
            else:  #'s'
                y = self.rect.bottom
        if (cardinal == 'e') or (cardinal == 'w'):
            y = (self.rect.top + self.rect.height / 2 -
                 new_bullet.rect.height / 2)
            if cardinal == 'e':
                x = self.rect.right
            else:  # cardinal == 'w':
                x = self.rect.left - new_bullet.rect.width

        new_bullet.set_xy(x, y)
        new_bullet.set_desired_thrust(1.0)
        bullet_spritegroup.add(new_bullet)

    # def shoot_from(self, image, bullet_spritegroup, x, y, angle,
                   # bullet_health=1):
        # # not used by enemy
        # new_bullet = Entity(self.app, self.what+'.bullet', [image],
                            # init_enemy_speed, self.angle,
                            # bullet_spritegroup, bullet_health,
                            # None, self.particles,
                            # offscreen_remove=True)
        # new_bullet.set_xy(x, y)
        # new_bullet.set_desired_thrust(1.0)
        # bullet_spritegroup.add(new_bullet)

    def set_desired_thrust(self, thrust):
        self.thrust = thrust
        self.set_angle(self.angle)  # updates vector

    def set_angle(self, angle):
        self.angle = angle
        r = float(self.thrust * self.speed)
        self.vector = (r * math.cos(math.radians(self.angle)),
                       r * math.sin(math.radians(self.angle)))
        if (self.vector[0] is None) or (self.vector[1] is None):
            print("WARNING in Entity set_angle: undefined component" +
                  " in vector:" + str(self.vector))
            self.vector = (0, 0)

    def set_speed(self, speed):  # not used by player
        self.speed = speed

    def set_range(self, xmin, xmax):  # not used by player
        self.world_rect = pygame.Rect(xmin,
                                      self.world_rect.top,
                                      xmax - xmin,
                                      self.world_rect.bottom)

    def get_range(self):  # not used by player
        return self.world_rect.left, self.world_rect.right

    # -1 is normal, 0 is exploding, up to len(self.explosion_images) - 1
    # are explosion frames
    def set_state(self, state):
        self.state = state

    def next_state(self):
        if self.state >= 0:
            if self.explosion_images is None:
                self.state = 1
                self.spritegroup.remove(self)
                print('removed a ' + self.what + 'WITHOUT explosion')
                return
            if self.generate_ex:
                self.generate_ex = False
                if self.particles is not None:
                    exp_what = self.what + '.explosion'
                    new_exp = Entity(self.app, exp_what,
                                     self.explosion_images,
                                     0, self.angle,
                                     self.particles,
                                     1,
                                     None,
                                     None,
                                     offscreen_remove=True,
                                     anim_done_remove=True,
                                     temper_sound=self.ex_sound)
                    new_exp.temper = 1  # begin particle decay
                    new_exp.parent_what = self.what
                    x, y = self.rect.center
                    w, h = self.explosion_images[0].get_size()
                    x -= w / 2
                    y -= h / 2
                    new_exp.set_xy(x, y)
                    self.particles.add(new_exp)
                    if self.what == 'explosion':
                        print("  generated explosion from " + self.what)
                # else must be a particle  # TODO: secondary particles

            state_frame = int(self.state/self.state_delay)
            # NOTE: nothing is actually shown -- just use the length
            # of the animation for how long to decay
            if state_frame < len(self.explosion_images):
                # self.image = self.explosion_images[state_frame]
                # if self.state >= 1:
                     # # TODO: remove after flash covers ship
                     # # but don't remove from spritegroup!
                     # # otherwise decay will not continue.
                     # self.spritegroup.remove(self)
                if self.state > 1:
                    self.set_visible(False)
                # self.dirty = 0  # DirtySprite feature fails
                # self.visible = 0  # DirtySprite feature fails
                self.state += 1
            else:
                if not self.removed:
                    self.spritegroup.remove(self)
                    self.removed = True
                    if self.what != "particle":
                        print('removed ' + self.what + ' (decayed)')

    def get_state(self):
        return self.state

    def get_is_decayed(self):
        return self.state >= self._get_final_state()

    def _get_final_state(self):
        ret = 1
        if self.explosion_images is not None:
            last_state = ((len(self.explosion_images) - 1) *
                          self.state_delay)
            if last_state > ret:
                ret = last_state
        return ret

    def motivate(self, transition_speed):
        if self.ai_enable:
            # AI, not used for player-controlled p_unit
            if self.desired_vel_x == 0:
                self.desired_vel_x = 1
            # this is actually surgy's code but i adapted it to my own
            # and rewrote it so it uses < and > not == and !=
            if transition_speed > 0:
                self.rect.bottom += transition_speed
            elif self.desired_vel_x < 0:
                if self.rect.left < self.world_rect.right:
                    self.rect.right += self.speed
                elif self.rect.left >= self.world_rect.right:
                    self.desired_vel_x = 1
            else:
                if self.rect.left > self.world_rect.left:
                    self.rect.right += ((-1) * self.speed)
                elif self.rect.left <= self.world_rect.left:
                    self.desired_vel_x = -1
