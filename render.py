import pygame
import SETTINGS
import math


class Render:

    def __init__(self, surface, map_surface):
        self.fps = ''
        self.sc = surface
        self.sc_map = map_surface

        self.texture_kit = {
            '1': [pygame.image.load(
                f'img/textures/128px/var_9/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            '2': [pygame.image.load(
                f'img/textures/128px/var_2/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            '3': [pygame.image.load(
                f'img/textures/128px/var_3/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            '4': [pygame.image.load(
                f'img/textures/128px/var_4/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            '5': [pygame.image.load(
                f'img/textures/128px/var_12/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            '6': [pygame.image.load(
                f'img/textures/128px/var_10/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            '7': [pygame.image.load(
                f'img/textures/128px/var_11/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            '8': [pygame.image.load(
                f'img/textures/128px/var_1/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            'P': [pygame.image.load(
                f'img/textures/128px/var_p/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            'F': pygame.image.load(
                f'img/textures/128px/floor/5.jpg').convert(),
            'C': pygame.image.load(
                f'img/textures/128px/floor/4.jpg').convert(),
            'S': [pygame.image.load(
                f'img/textures/128px/sky/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
            'N': [pygame.image.load(
                f'img/textures/128px/var_n/{i}.png').convert() for i in range(1, SETTINGS.tile_size + 1)],
        }

    def draw_world(self, walls, floor):

        for n_ray in walls:
            '''Drawin floor'''
            if floor[n_ray]:
                for coords, area in floor[n_ray]:
                    self.sc.blit(self.texture_kit['F'], coords, area)
                    # self.sc.blit(self.texture_kit['C'], (coords[0], SETTINGS.HEIGHT - 12 - coords[1]), area)

            '''Drawing wall'''
            # _, projected_height, texture_offset, texture = walls[n_ray]
            projected_height = walls[n_ray][1]
            texture_offset = walls[n_ray][2]
            texture = walls[n_ray][3]
            img = pygame.transform.scale(self.texture_kit[texture][texture_offset],
                                         (SETTINGS.step_screen, projected_height))
            self.sc.blit(img, (SETTINGS.table_scale_screen[n_ray], SETTINGS.h_HEIGHT - projected_height // 2))

    def draw_map(self, map, player_x, player_y, sin_a, cos_a):

        self.sc_map.fill(SETTINGS.BLACK)
        '''Draw minimap'''
        [pygame.draw.rect(self.sc_map, SETTINGS.DARKGRAY, obj, 1) for obj in map]

        '''Draw minimap player'''
        scale_player_x = self.scaling_to_map(player_x)
        scale_player_y = self.scaling_to_map(player_y)

        pygame.draw.line(self.sc_map, SETTINGS.DARKYELLOW, (scale_player_x, scale_player_y),
                        (scale_player_x + 14 * cos_a, scale_player_y + 14 * sin_a), 1)
        pygame.draw.circle(self.sc_map, SETTINGS.DARKRED,
                          (scale_player_x, scale_player_y), 4)

        self.sc.blit(self.sc_map, SETTINGS.map_position)
        # pygame.draw.line(self.sc, SETTINGS.WHITE, (0, SETTINGS.h_HEIGHT), (SETTINGS.WIDTH, SETTINGS.h_HEIGHT))
        # pygame.draw.line(self.sc, SETTINGS.WHITE, (0, SETTINGS.h_HEIGHT + 30), (SETTINGS.WIDTH, SETTINGS.h_HEIGHT + 30))

    def draw_background(self, angle, x, y):
        # pygame.draw.rect(self.sc, SETTINGS.BLUE_SKY, (0, 0, SETTINGS.WIDTH, SETTINGS.h_HEIGHT))
        # pygame.draw.rect(self.sc, SETTINGS.DGRAY, (0, SETTINGS.h_HEIGHT, SETTINGS.WIDTH, SETTINGS.h_HEIGHT))
        [self.sc.blit(self.texture_kit['S'][int((math.degrees(angle) + i) % SETTINGS.tile_size)],
                      (i * 10, 0)) for i in range(SETTINGS.tile_size)]

    def display_fps(self, clock):
        font = pygame.font.SysFont("Arial", 28)
        self.fps = clock.get_fps()
        render = font.render(str(int(self.fps)), 0, SETTINGS.RED)
        self.sc.blit(render, SETTINGS.fps_coords)

    def mapping(self, coord):
        return (coord // SETTINGS.tile_size) * SETTINGS.tile_size

    def scaling_to_map(self, coord):
        return int(coord * SETTINGS.scale_map_player)
