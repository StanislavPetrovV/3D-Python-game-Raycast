import math
import SETTINGS


class RayCast:

    def __init__(self, map):
        self.map = map
        self.fov = SETTINGS.fov
        self.world = {}
        self.walls, self.floor = {}, {}
        self.texture_h, self.texture_v = '1', '1'
        self.floor_coords, self.floor_area = 0, 0
        self.mod = 300
        self.quaters = SETTINGS.quaters
        self.half_fov = SETTINGS.half_fov
        self.tile_size = SETTINGS.tile_size
        self.set_quater_III_IV = {'III', 'IV'}
        self.quater = 'IV'
        self.map_rows = SETTINGS.map_rows
        self.map_cols = SETTINGS.map_cols
        self.coeff_texture_offset = self.tile_size - 1
        self.hor_ver_coeff = {
            'I': {
                'nearest_Y': self.tile_size,
                'delta_Y': self.tile_size,
                'nearest_X': self.tile_size,
                'delta_X': self.tile_size
            },
            'II': {
                'nearest_Y': self.tile_size,
                'delta_Y': self.tile_size,
                'nearest_X': -1,
                'delta_X': -self.tile_size
            },
            'III': {
                'nearest_Y': -1,
                'delta_Y': -self.tile_size,
                'nearest_X': -1,
                'delta_X': -self.tile_size
            },
            'IV': {
                'nearest_Y': -1,
                'delta_Y': -self.tile_size,
                'nearest_X': self.tile_size,
                'delta_X': self.tile_size
            },
        }

    def raycasting(self, player_angle, player_x, player_y, process):
        ''''Main core, casting walls, casting floor'''

        # if not process:
        #     self.walls = {}
        #     self.floor = {i:[] for i in range(SETTINGS.h_projection_plane)}
        #     n_ray = 0
        #     self.angle_ray = player_angle - self.half_fov
        # else:
        #     self.walls = {}
        #     self.floor = {i: [] for i in range(SETTINGS.h_projection_plane, SETTINGS.projection_plane)}
        #     n_ray = SETTINGS.h_projection_plane
        #     self.angle_ray = player_angle + SETTINGS.angle_between_rays

        player_angle += 0.0001
        if process == 0:
            n_ray = 0
            self.floor = {i: [] for i in range(80)}
            self.angle_ray = player_angle - self.half_fov
        elif process == 1:
            n_ray = 80
            self.floor = {i: [] for i in range(80, 160)}
            self.angle_ray = player_angle - SETTINGS.start_angle_process_2
        elif process == 2:
            n_ray = 160
            self.floor = {i: [] for i in range(160, 240)}
            self.angle_ray = player_angle - SETTINGS.start_angle_process_3
        else:
            n_ray = 240
            self.floor = {i: [] for i in range(240, 320)}
            self.angle_ray = player_angle - SETTINGS.start_angle_process_4


        '''Casting walls'''
        # self.angle_ray = player_angle - self.half_fov
        for ray in range(80):
            # n_ray = 0
            # angle_ray = player_angle
            deg_angle_ray = int(math.degrees(self.angle_ray) % 360) # <---------

            for qtr in self.quaters:
                if deg_angle_ray in qtr:
                    self.quater = self.quaters[qtr]
                    break

            # if 0 <= deg_angle_ray < 90:
            #     self.quater = 'I'
            # elif 90 <= deg_angle_ray < 180:
            #     self.quater = 'II'
            # elif 180 <= deg_angle_ray < 270:
            #     self.quater = 'III'
            # else:
            #     self.quater = 'IV'

            self.coeffs_dict = self.hor_ver_coeff[self.quater]

            tan_angle_ray = math.tan(self.angle_ray)  # + 0.0001)  # <---------

            if self.quater in self.set_quater_III_IV:
                tan_angle_ray = -tan_angle_ray

            delta_X = self.tile_size / tan_angle_ray
            nearest_Y = self.mapping(player_y) + self.coeffs_dict['nearest_Y']
            X_vertical = player_x + (abs(player_y - nearest_Y) / tan_angle_ray)

            flat_nearest_Y = nearest_Y // self.tile_size
            steps = [flat_nearest_Y, self.map_rows - flat_nearest_Y][self.coeffs_dict['nearest_Y'] > 0]
            for step in range(steps):
                tile_v = (int(X_vertical) // self.tile_size, nearest_Y // self.tile_size)

                if tile_v in self.map:
                    self.texture_v = self.map[tile_v]
                    break
                X_vertical += delta_X
                nearest_Y += self.coeffs_dict['delta_Y']

            tan_angle_ray = abs(tan_angle_ray)
            if self.quater in self.set_quater_III_IV:
                tan_angle_ray = -tan_angle_ray

            delta_Y = self.tile_size * tan_angle_ray
            nearest_X = self.mapping(player_x) + self.coeffs_dict['nearest_X']
            Y_horizontal = player_y + (abs(player_x - nearest_X) * tan_angle_ray)

            flat_nearest_X = nearest_X // self.tile_size
            steps = [flat_nearest_X, self.map_cols - flat_nearest_X][self.coeffs_dict['nearest_X'] > 0]
            for step in range(steps):
                tile_h = (nearest_X // self.tile_size, int(Y_horizontal) // self.tile_size)

                if tile_h in self.map:
                    self.texture_h = self.map[tile_h]
                    break
                nearest_X += self.coeffs_dict['delta_X']
                Y_horizontal += delta_Y

            dist_vertical = math.sqrt((player_x - X_vertical) ** 2 + (player_y - nearest_Y) ** 2)
            dist_horizontal = math.sqrt((player_x - nearest_X) ** 2 + (player_y - Y_horizontal) ** 2)

            '''Remove aqua efect'''
            self.remove_aqua_effect = math.cos(player_angle - self.angle_ray)  # <---------

            '''Choose nearest dot'''
            if dist_vertical < dist_horizontal:
                self.dist = dist_vertical * self.remove_aqua_effect
                texture = self.texture_v
                if self.coeffs_dict['delta_Y'] > 0:
                    texture_offset = self.coeff_texture_offset - int(X_vertical) % self.tile_size
                else:
                    texture_offset = int(X_vertical) % self.tile_size
            else:
                texture = self.texture_h
                self.dist = dist_horizontal * self.remove_aqua_effect
                if self.coeffs_dict['delta_X'] < 0:
                    texture_offset = self.coeff_texture_offset - int(Y_horizontal) % self.tile_size
                else:
                    texture_offset = int(Y_horizontal) % self.tile_size

            '''Projected column height'''
            projected_height = int(SETTINGS.coeff_projected_obj / self.dist)

            '''Arr of walls'''
            # self.world[n_ray] = [self.dist, projected_height, texture_offset, texture, []]
            # self.walls[n_ray] = (self.dist, projected_height, texture_offset, texture)
            self.walls[n_ray] = (self.dist, projected_height, texture_offset, texture)

            '''Casting floor'''
            sin_a = math.sin(self.angle_ray)  # <---------
            cos_a = math.cos(self.angle_ray)  # <---------
            bottom_wall = SETTINGS.h_RES_H + projected_height // SETTINGS.h_step_screen

            if  SETTINGS.h_RES_H + 6 < bottom_wall < SETTINGS.RES_H:
                
                if n_ray < SETTINGS.floor_optim_x:
                    for row in range(bottom_wall, SETTINGS.RES_H - SETTINGS.floor_optim_y, 3):
                        straight_distance = SETTINGS.coeff_floor_cast / (row - SETTINGS.h_RES_H)
                        correct_straight_distance = straight_distance / self.remove_aqua_effect

                        floor_x = int(player_x + correct_straight_distance * cos_a) % self.mod
                        floor_y = int(player_y + correct_straight_distance * sin_a) % self.mod

                        floor_coords = (SETTINGS.table_scale_screen[n_ray], SETTINGS.table_scale_screen_height[row])
                        floor_area = (floor_x, floor_y, SETTINGS.step_screen, 12)

                        self.floor[n_ray].append((floor_coords, floor_area))
                        # self.world[n_ray][4].append((floor_coords, floor_area))
                else:
                    for row in range(bottom_wall, SETTINGS.RES_H, 3):

                        straight_distance = SETTINGS.coeff_floor_cast / (row - SETTINGS.h_RES_H)
                        correct_straight_distance = straight_distance / self.remove_aqua_effect

                        floor_x = int(player_x + correct_straight_distance * cos_a) % self.mod
                        floor_y = int(player_y + correct_straight_distance * sin_a) % self.mod

                        floor_coords = (SETTINGS.table_scale_screen[n_ray], SETTINGS.table_scale_screen_height[row])
                        floor_area =(floor_x, floor_y, SETTINGS.step_screen , 12)

                        self.floor[n_ray].append((floor_coords, floor_area))
                        # self.world[n_ray][4].append((floor_coords, floor_area))

            n_ray += 1
            self.angle_ray += SETTINGS.angle_between_rays
        return self.walls, self.floor

    def mapping(self, coord):
        return int(coord // self.tile_size) * self.tile_size

    def optimal_amt(self, nearest, map_rows_cols):
        if map_rows_cols == self.map_rows:
            return [nearest // self.tile_size,
                    self.map_rows - nearest // self.tile_size][self.coeffs_dict['nearest_Y'] > 0]
        else:
            return [nearest // self.tile_size,
                    self.map_cols - nearest // self.tile_size][self.coeffs_dict['nearest_X'] > 0]

    def find_dist(self, dot1, dot2):
        return math.sqrt((dot1[0] - dot2[0]) ** 2 + (dot1[1] - dot2[1]) ** 2)
