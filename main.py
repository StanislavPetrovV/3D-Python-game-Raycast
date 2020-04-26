from multiprocessing import Pool
import pygame
import tkinter as tk
import sys
import os
import map
import SETTINGS
import player
import raycast_mp
import render
import npc


if __name__ == '__main__':

    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{(tk.Tk().winfo_screenwidth() - SETTINGS.WIDTH) // 2},' \
                                         f'{(tk.Tk().winfo_screenheight() - SETTINGS.HEIGHT) // 4}'
    pygame.init()
    pygame.display.set_caption('Ray casting')

    sc = pygame.display.set_mode(SETTINGS.SIZE)
    sc_map = pygame.Surface(SETTINGS.map_size)

    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    map = map.Map()
    render = render.Render(sc, sc_map)

    npc_0 = npc.NPC(sc, (4062, 1270), 'bruda')
    npc_1 = npc.NPC(sc, (3936, 570), 'bruda_1')
    npc_2 = npc.NPC(sc, (4417, 554), 'bruda_2')
    npc_3 = npc.NPC(sc, (721, 841), 'bruda_3')
    npc_4 = npc.NPC(sc, (719, 595), 'bruda_4')

    player = player.Player(npc, clock, map.flat_map)
    ray_cast = raycast_mp.RayCast(map.map)  # , sc, render)

    with Pool(processes=4) as pool:

        game = True
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = False

            player.movement()
            sc.fill(SETTINGS.BLACK)
            render.draw_background(player.angle_inf, player.real_x, player.real_y)

            res_1 = pool.apply_async(ray_cast.raycasting, (player.angle, player.real_x, player.real_y, 0))
            res_2 = pool.apply_async(ray_cast.raycasting, (player.angle, player.real_x, player.real_y, 1))
            res_3 = pool.apply_async(ray_cast.raycasting, (player.angle, player.real_x, player.real_y, 2))
            res_4 = pool.apply_async(ray_cast.raycasting, (player.angle, player.real_x, player.real_y, 3))

            walls_1, floor_1 = res_1.get()
            walls_2, floor_2 = res_2.get()
            walls_3, floor_3 = res_3.get()
            walls_4, floor_4 = res_4.get()

            walls_1.update(walls_2); floor_1.update(floor_2)
            walls_1.update(walls_3); floor_1.update(floor_3)
            walls_1.update(walls_4); floor_1.update(floor_4)

            render.draw_world(walls_1, floor_1)


            npc_1.draw(player.angle, player.player_coords, walls_1, True)
            npc_2.draw(player.angle, player.player_coords, walls_1, True)
            npc_3.draw(player.angle, player.player_coords, walls_1, True)
            npc_4.draw(player.angle, player.player_coords, walls_1, True)
            npc_0.draw(player.angle, player.player_coords, walls_1, False)
            
            render.draw_map(map.map_of_tiles, player.real_x, player.real_y, player.sin_a, player.cos_a)
            render.display_fps(clock)

            # pygame.display.update()
            pygame.display.flip()
            # clock.tick()
    pygame.quit()
    sys.exit()
