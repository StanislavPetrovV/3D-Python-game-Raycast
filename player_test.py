import pygame
import math
import SETTINGS


class TestPlayer():

    def __init__(self, flat_map):
        self.flat_map = flat_map
        self.speed = SETTINGS.player_speed
        self.angle = SETTINGS.player_angle
        self.delta_angle = SETTINGS.angle_between_rays
        self.pos = self.real_x, self.real_y = SETTINGS.player_pos
        self.quater = ''
        self.sin_a, self.cos_a = 0, 0

    def movement(self, player_angle, coords):
        self.cos_a = math.cos(self.angle)
        self.sin_a = math.sin(self.angle)
        direction = {'W': (self.cos_a, self.sin_a), 'S': (-self.cos_a, -self.sin_a),
                     'A': (self.sin_a, -self.cos_a), 'D': (-self.sin_a, self.cos_a)}
        self.angle = player_angle
        self.real_x, self.real_y = coords

        self.angle %= 2 * math.pi
        self.player_coords = (self.real_x, self.real_y)
