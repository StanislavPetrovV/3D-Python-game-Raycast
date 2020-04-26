import math
import pygame
import SETTINGS
from collections import deque


class NPC:

    def __init__(self, surface, coords, path):
        self.sc = surface
        self.path = path
        self.ray = SETTINGS.center_ray
        self.args = self.angle, self.coords = 0, coords
        self.x, self.y = self.coords
        self.npc_tile = self.npc_tile_x, self.npc_tile_y = (
            self.x // SETTINGS.tile_size, self.y // SETTINGS.tile_size)  # (10, 16)
        self.sprites = self.load_sprites()
        self.sprite_numbers = deque([str(i) + str(j) for i in range(4) for j in range(4)])
        self.sprite_positions = self.create_sprite_positions()
        self.elevation = 6

    def load_sprites(self):
        return [[pygame.image.load(
            f'img/sprites/{self.path}/{str(row) + str(col)}.png').convert_alpha()
                 for col in range(SETTINGS.sprite_arr_size)] for row in range(SETTINGS.sprite_arr_size)]

    def create_sprite_positions(self):
        return {angle: pos for angle, pos in zip(SETTINGS.npc_angles, self.sprite_numbers)}

    def draw(self, player_angle, player_coords, walls, rotate):
        '''Find where to locate npc, on what ray'''
        delta_y = player_coords[1] - self.y
        delta_x = player_coords[0] - self.x

        D = self.find_dist(self.coords, player_coords)
        if rotate and D < 300:
            self.angle = 1
            self.rotate()
        alpha = player_angle - SETTINGS.pi
        if delta_x > 0:
            gamma = math.asin(delta_y / D) - alpha
        else:
            if delta_y > 0:
                if 0 <= math.degrees(player_angle) <= 180:
                    gamma = math.acos(delta_x / D) - alpha - SETTINGS.double_pi
                else:
                    gamma = math.acos(delta_x / D) - alpha
            else:
                if 180 <= math.degrees(player_angle) <= 360:
                    gamma = -math.acos(delta_x / D) - alpha + SETTINGS.double_pi
                else:
                    gamma = -math.acos(delta_x / D) - alpha

        delta_rays = int(gamma / SETTINGS.angle_between_rays)
        current_npc_x = SETTINGS.center_ray + delta_rays
        D *= math.cos(SETTINGS.half_fov - current_npc_x * SETTINGS.angle_between_rays)

        '''Angle between npc, player'''
        theta = math.atan2(delta_y, delta_x)
        if theta < 0:
            theta += SETTINGS.double_pi
        elif theta > SETTINGS.double_pi:
            theta -= SETTINGS.double_pi
        theta_deg = 359 - int(math.degrees(theta))

        '''Is rotate npc'''
        self.rotate()

        '''Is visible npc now'''
        if 0 <= current_npc_x <= 319:
            dist_player_npc = D
            dist_player_wall = walls[current_npc_x][0]

            if dist_player_npc < dist_player_wall:
                '''Drawing'''
                for angles in self.sprite_positions:
                    if theta_deg in angles:
                        i, j = self.sprite_positions[angles]
                        sprite = self.sprites[int(i)][int(j)]
                        projected_height = int(SETTINGS.coeff_projected_obj / D)

                        img = pygame.transform.scale(sprite, (projected_height, projected_height))
                        self.sc.blit(img, (
                            current_npc_x * SETTINGS.step_screen - projected_height // 2,
                            SETTINGS.h_HEIGHT + self.elevation - projected_height // 6))
                        break

    def rotate(self):
        if self.angle == 1:
            self.angle = 0
            self.sprite_numbers.rotate(1)
        elif self.angle == -1:
            self.angle = 0
            self.sprite_numbers.rotate(-1)
        self.sprite_positions = self.create_sprite_positions()

    def find_dist(self, dot1, dot2):
        return math.sqrt((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2)
