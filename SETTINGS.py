import math
from text_map import *

'''Game settings'''
FPS = 200
SIZE = WIDTH, HEIGHT = (1280, 768)
RES = RES_W, RES_H = 320, 192
h_RES_W, h_RES_H = RES_W // 2, RES_H // 2
h_WIDTH = WIDTH // 2
h_HEIGHT = HEIGHT // 2

'''Mouse'''
shift_coeff = WIDTH - 200

'''Tile settings'''
# tile_size = 64
tile_size = 128
# tile_size = 256

'''Map'''
map_size = (WIDTH//4.54, HEIGHT//4.5)
map_rows = len(text_map)
map_cols = len(text_map[0])

new_width, new_height = tile_size * map_cols, tile_size * map_rows
scale_map = (tile_size // (tile_size * map_cols / map_size[0]))
scale_map_player = (map_size[0] / (tile_size * map_cols))
map_position = (0, HEIGHT - map_size[1])


'''Raycasting settings'''
projection_plane = 320
h_projection_plane = projection_plane // 2
norm_pj = projection_plane // 320
fov = 1.28
half_fov = fov / 2
angle_between_rays = fov / projection_plane

quaters = {
    frozenset(range(0, 90)):   'I',
    frozenset(range(90, 180)): 'II',
    frozenset(range(180, 270)):'III',
    frozenset(range(270, 360)):'IV'
}
spec_quaters = {
    frozenset({i for i in range(315, 360)} | {i for i in range(0, 45)}):   'I',
    frozenset(range(45, 135)): 'II',
    frozenset(range(135, 225)):'III',
    frozenset(range(225, 315)):'IV'
}



'''Player settings'''
scale_player_coords = tile_size * map_cols // WIDTH
player_angle = 1.57
player_speed = 200 * norm_pj
player_pos = (4350, 2556) # 128px
player_h = tile_size // 2

'''Render settings'''
distance_to_projection = int(projection_plane / math.tan(half_fov))
coeff_projected_obj = tile_size * distance_to_projection * 2.5 / norm_pj
coeff_floor_cast = distance_to_projection * player_h / 1.5
center_ray = projection_plane // 2 - 1
step_screen = WIDTH // projection_plane
h_step_screen = step_screen * 2
h_scale_screen = step_screen // 2
fps_coords = (WIDTH - 30, HEIGHT//100)
floor_list = [['' for i in range(RES_H)] for j in range(RES_W)]

'''Floor'''
coeff_for_D = distance_to_projection * player_h

'''Colours'''
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BLUE_SKY = (0, 189, 255)
BROWN = (140, 50, 20)
DARKGRAY = (50, 50, 50)
DARKBLUE = (0, 0, 70)
DGRAY = (30, 30, 30)
DARKRED = (80, 0, 0)
DARKGREEN = (6, 51, 9)
DARKYELLOW = (155, 135, 12)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
LIGHTBLUE = (100, 100, 225)
LIGHTGRAY = (150, 150, 150)
LIGHTGREEN = (100, 255, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

'''NPC'''
npc_angles = [frozenset({i for i in range(0, 11)}) | frozenset({i for i in range(348, 360)}),
			 frozenset(range(11, 33)),
			 frozenset(range(33, 56)),
			 frozenset(range(56, 78)),
			 frozenset(range(78, 101)),
			 frozenset(range(101, 123)),
			 frozenset(range(123, 146)),
			 frozenset(range(146, 168)),
			 frozenset(range(168, 191)),
			 frozenset(range(191, 213)),
			 frozenset(range(213, 236)),
			 frozenset(range(236, 258)),
			 frozenset(range(258, 281)),
			 frozenset(range(281, 303)),
			 frozenset(range(303, 326)),
			 frozenset(range(326, 348))
			 ]

'''Textures'''
sprite_arr_size = 4

'''Angles'''
pi = math.pi
double_pi = 2 * pi
half_pi = pi / 2
one_half_pi = 1.5 * pi

'''Optimisations'''
table_scale_screen = {ray: ray * step_screen for ray in range(projection_plane + 1)}
table_scale_screen_height = {ray: int(ray * HEIGHT / RES_H) for ray in range(projection_plane + 1)}
floor_optim_x = int(scale_map * map_cols // step_screen)
floor_optim_y = int(scale_map * map_rows // step_screen)

start_angle_process_2 = half_fov - 80 * angle_between_rays
start_angle_process_3 = half_fov - 160 * angle_between_rays
start_angle_process_4 = half_fov - 240 * angle_between_rays

