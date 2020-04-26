import pygame
import math
import SETTINGS


class Player():

    def __init__(self, npc, clock, flat_map):
        self.npc = npc
        self.clock = clock
        self.flat_map = flat_map
        self.speed = SETTINGS.player_speed
        self.angle = SETTINGS.player_angle
        self.angle_inf = SETTINGS.player_angle
        self.delta_angle = SETTINGS.angle_between_rays
        self.player_coords = self.real_x, self.real_y = SETTINGS.player_pos
        self.quater = ''
        self.mouse_coeff = math.pi / SETTINGS.WIDTH * SETTINGS.norm_pj
        self.sin_a, self.cos_a = 0, 0
        '''colliding wall settings'''
        self.player_size = 50
        self.quarter = 'I'
        self.collider = {
            'left': {
                'I': {'W': (1, 1), 'S': (0, 1), 'A': (1, 1), 'D': (0, 1)},
                'II': {'W': (0, 1), 'S': (1, 1), 'A': (1, 1), 'D': (0, 1)},
                'III': {'W': (0, 1), 'S': (1, 1), 'A': (0, 1), 'D': (1, 1)},
                'IV': {'W': (1, 1), 'S': (0, 1), 'A': (0, 1), 'D': (1, 1)},
            },
            'top': {
                'I': {'W': (1, 1), 'S': (1, 0), 'A': (1, 0), 'D': (1, 1)},
                'II': {'W': (1, 1), 'S': (1, 0), 'A': (1, 1), 'D': (1, 0)},
                'III': {'W': (1, 0), 'S': (1, 1), 'A': (1, 1), 'D': (1, 0)},
                'IV': {'W': (1, 0), 'S': (1, 1), 'A': (1, 0), 'D': (1, 1)},
            },
            'right': {
                'I': {'W': (0, 1), 'S': (1, 1), 'A': (0, 1), 'D': (1, 1)},
                'II': {'W': (1, 1), 'S': (0, 1), 'A': (0, 1), 'D': (1, 1)},
                'III': {'W': (1, 1), 'S': (0, 1), 'A': (1, 1), 'D': (0, 1)},
                'IV': {'W': (0, 1), 'S': (1, 1), 'A': (1, 1), 'D': (0, 1)},
            },
            'bottom': {
                'I': {'W': (1, 0), 'S': (1, 1), 'A': (1, 1), 'D': (1, 0)},
                'II': {'W': (1, 0), 'S': (1, 1), 'A': (1, 0), 'D': (1, 1)},
                'III': {'W': (1, 1), 'S': (1, 0), 'A': (1, 0), 'D': (1, 1)},
                'IV': {'W': (1, 1), 'S': (1, 0), 'A': (1, 1), 'D': (1, 0)},
            },
            'lefttop': {
                'I': {'W': (1, 1), 'S': (0, 0), 'A': (1, 0), 'D': (0, 1)},
                'II': {'W': (0, 1), 'S': (1, 0), 'A': (1, 1), 'D': (0, 0)},
                'III': {'W': (0, 0), 'S': (1, 1), 'A': (0, 1), 'D': (1, 0)},
                'IV': {'W': (1, 0), 'S': (0, 1), 'A': (0, 0), 'D': (1, 1)},
            },
            'righttop': {
                'I': {'W': (0, 1), 'S': (1, 0), 'A': (0, 0), 'D': (1, 1)},
                'II': {'W': (1, 1), 'S': (0, 0), 'A': (0, 1), 'D': (1, 0)},
                'III': {'W': (1, 0), 'S': (0, 1), 'A': (1, 1), 'D': (0, 0)},
                'IV': {'W': (0, 0), 'S': (1, 1), 'A': (1, 0), 'D': (0, 1)},
            },
            'bottomright': {
                'I': {'W': (0, 0), 'S': (1, 1), 'A': (0, 1), 'D': (1, 0)},
                'II': {'W': (1, 0), 'S': (0, 1), 'A': (0, 0), 'D': (1, 1)},
                'III': {'W': (1, 1), 'S': (0, 0), 'A': (1, 0), 'D': (0, 1)},
                'IV': {'W': (0, 1), 'S': (1, 0), 'A': (1, 1), 'D': (0, 0)},
            },
            'bottomleft': {
                'I': {'W': (1, 0), 'S': (0, 1), 'A': (1, 1), 'D': (0, 0)},
                'II': {'W': (0, 0), 'S': (1, 1), 'A': (1, 0), 'D': (0, 1)},
                'III': {'W': (0, 1), 'S': (1, 0), 'A': (0, 0), 'D': (1, 1)},
                'IV': {'W': (1, 1), 'S': (0, 0), 'A': (0, 1), 'D': (1, 0)},
            },
            'left_top_corner': {
                'I': {'W': (1, 1), 'S': (1, 0), 'A': (0, 1), 'D': (1, 1)},
                'II': {'W': (1, 1), 'S': (0, 1), 'A': (1, 1), 'D': (1, 0)},
                'III': {'W': (1, 0), 'S': (1, 1), 'A': (1, 1), 'D': (0, 1)},
                'IV': {'W': (0, 1), 'S': (1, 1), 'A': (1, 0), 'D': (1, 1)},
            },
            'right_top_corner': {
                'I': {'W': (1, 0), 'S': (1, 1), 'A': (0, 1), 'D': (1, 1)},
                'II': {'W': (1, 1), 'S': (0, 1), 'A': (1, 0), 'D': (1, 1)},
                'III': {'W': (1, 1), 'S': (1, 0), 'A': (1, 1), 'D': (0, 1)},
                'IV': {'W': (0, 1), 'S': (1, 1), 'A': (1, 1), 'D': (1, 0)},
            },
            'bottom_right_corner': {
                'I': {'W': (1, 0), 'S': (1, 1), 'A': (1, 1), 'D': (0, 1)},
                'II': {'W': (0, 1), 'S': (1, 1), 'A': (1, 0), 'D': (1, 1)},
                'III': {'W': (1, 1), 'S': (1, 0), 'A': (0, 1), 'D': (1, 1)},
                'IV': {'W': (1, 1), 'S': (0, 1), 'A': (1, 1), 'D': (1, 0)},
            },
            'bottom_left_corner': {
                'I': {'W': (1, 1), 'S': (1, 0), 'A': (1, 1), 'D': (0, 1)},
                'II': {'W': (0, 1), 'S': (1, 1), 'A': (1, 1), 'D': (1, 0)},
                'III': {'W': (1, 0), 'S': (1, 1), 'A': (0, 1), 'D': (1, 1)},
                'IV': {'W': (1, 1), 'S': (0, 1), 'A': (1, 0), 'D': (1, 1)},
            },
        }
        self.corner_names = {'left_top_corner', 'right_top_corner', 'bottom_right_corner', 'bottom_left_corner'}
        self.side_names = {'left', 'top', 'right', 'bottom'}

    def is_collide(self):
        self.real_x = int(self.real_x)
        self.real_y = int(self.real_y)
        '''coliding wall sides'''
        center_x = self.real_x // SETTINGS.tile_size
        center_y = self.real_y // SETTINGS.tile_size
        left_x = (self.real_x - self.player_size) // SETTINGS.tile_size
        right_x = (self.real_x + self.player_size) // SETTINGS.tile_size
        top_y = (self.real_y - self.player_size) // SETTINGS.tile_size
        bottom_y = (self.real_y + self.player_size) // SETTINGS.tile_size

        '''coliding wall corners'''
        left_top = (left_x, top_y)
        right_top = (right_x, top_y)
        bottom_right = (right_x, bottom_y)
        bottom_left = (left_x, bottom_y)

        collide_dict = {
            left_top: 'left_top_corner',
            right_top: 'right_top_corner',
            bottom_right: 'bottom_right_corner',
            bottom_left: 'bottom_left_corner',
            (left_x, center_y): 'left',
            (center_x, top_y): 'top',
            (right_x, center_y): 'right',
            (center_x, bottom_y): 'bottom'
        }
        collide_set = {(left_x, center_y), (center_x, top_y), (right_x, center_y), (center_x, bottom_y), left_top,
                       right_top, bottom_right, bottom_left}

        collidings = sorted([collide_dict[i] for i in (self.flat_map & collide_set)])

        sides, corners = '', ''
        for colliding in collidings:
            if colliding in self.side_names:
                sides += colliding
            else:
                corners += colliding

        if sides:
            deg_angle = int(math.degrees(self.angle) % 360)
            for qtr in SETTINGS.quaters:
                if deg_angle in qtr:
                    self.quarter = SETTINGS.quaters[qtr]
                    return self.collider[sides][self.quarter]
        elif corners:
            deg_angle = int(math.degrees(self.angle) % 360)
            for qtr in SETTINGS.spec_quaters:
                if deg_angle in qtr:
                    self.quarter = SETTINGS.spec_quaters[qtr]
                    return self.collider[corners][self.quarter]
        return False

    def movement(self):
        self.cos_a = math.cos(self.angle)
        self.sin_a = math.sin(self.angle)
        direction = {'W': (self.cos_a, self.sin_a), 'S': (-self.cos_a, -self.sin_a),
                     'A': (self.sin_a, -self.cos_a), 'D': (-self.sin_a, self.cos_a)}


        keys = pygame.key.get_pressed()

        collide = self.is_collide()

        if collide:
            if keys[pygame.K_w]:
                self.real_x += collide['W'][0] * (self.speed * direction['W'][0])
                self.real_y += collide['W'][1] * (self.speed * direction['W'][1])

            if keys[pygame.K_s]:
                self.real_x += collide['S'][0] * (self.speed * direction['S'][0])
                self.real_y += collide['S'][1] * (self.speed * direction['S'][1])

            if keys[pygame.K_a]:
                self.real_x += collide['A'][0] * (self.speed * direction['A'][0])
                self.real_y += collide['A'][1] * (self.speed * direction['A'][1])

            if keys[pygame.K_d]:
                self.real_x += collide['D'][0] * (self.speed * direction['D'][0])
                self.real_y += collide['D'][1] * (self.speed * direction['D'][1])
        else:
            if keys[pygame.K_w]:
                self.real_x += (self.speed * direction['W'][0])
                self.real_y += (self.speed * direction['W'][1])

            if keys[pygame.K_s]:
                self.real_x += (self.speed * direction['S'][0])
                self.real_y += (self.speed * direction['S'][1])

            if keys[pygame.K_a]:
                self.real_x += (self.speed * direction['A'][0])
                self.real_y += (self.speed * direction['A'][1])

            if keys[pygame.K_d]:
                self.real_x += (self.speed * direction['D'][0])
                self.real_y += (self.speed * direction['D'][1])

        '''Changing player angle'''
        # if keys[pygame.K_LEFT]:
        #     self.angle -= math.pi / 10000
        # if keys[pygame.K_RIGHT]:
        #     self.angle += math.pi / 10000

        # rel = pygame.mouse.get_rel()
        # pos = pygame.mouse.get_pos()
        rel_0, pos_0 = pygame.mouse.get_rel()[0], pygame.mouse.get_pos()[0]
        delta_mouse = rel_0 * self.mouse_coeff
        self.angle += delta_mouse
        self.angle_inf += delta_mouse
        if abs(rel_0) > 100:
            self.angle -= delta_mouse
            self.angle_inf -= delta_mouse
        if pos_0 < 200 or pos_0 > SETTINGS.shift_coeff:
            pygame.mouse.set_pos(SETTINGS.h_WIDTH, SETTINGS.h_HEIGHT)

        '''For test npc'''
        if keys[pygame.K_z]:
            self.npc.angle = 1
        if keys[pygame.K_x]:
            self.npc.angle = -1
        if keys[pygame.K_c]:
            self.npc.elevation += 2
        if keys[pygame.K_v]:
            self.npc.elevation -= 2

        self.angle %= SETTINGS.double_pi
        self.player_coords = (self.real_x, self.real_y)
        # print(self.real_x, self.real_y)

        seconds = self.clock.tick() / 1000
        self.speed = SETTINGS.player_speed * seconds
