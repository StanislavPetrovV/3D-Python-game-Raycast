


if __name__ == '__main__':

    avg_fps = []
    for i in range(3):

        from multiprocessing import Pool
        import pygame
        import tkinter as tk
        import sys
        import os
        import time
        import map
        import SETTINGS
        import player_test
        import raycast_mp
        import render
        import npc
        import test_128

        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{(tk.Tk().winfo_screenwidth() - SETTINGS.WIDTH) // 2},' \
                                             f'{(tk.Tk().winfo_screenheight() - SETTINGS.HEIGHT) // 4}'
        pygame.init()
        pygame.display.set_caption('Ray casting')

        sc = pygame.display.set_mode(SETTINGS.SIZE)
        sc_map = pygame.Surface(SETTINGS.map_size)

        clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        map = map.Map()
        player = player_test.TestPlayer(map.flat_map)
        render = render.Render(sc, sc_map)

        npc_0 = npc.NPC(sc, (4062, 1270), 'bruda')
        npc_1 = npc.NPC(sc, (3936, 570), 'bruda_1')
        npc_2 = npc.NPC(sc, (4417, 554), 'bruda_2')
        npc_3 = npc.NPC(sc, (721, 841), 'bruda_3')
        npc_4 = npc.NPC(sc, (719, 595), 'bruda_4')

        ray_cast = raycast_mp.RayCast(map.map)

        with Pool(processes=4) as pool:

            fps = []

            t = time.time()
            for i, v in enumerate(test_128.test_list, 0):

                sc.fill(SETTINGS.BLACK)
                render.draw_background(player.angle, player.real_x, player.real_y)
                player.movement(v[0], v[1])

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

                if render.fps > 5:
                    fps.append(render.fps)

                # pygame.display.update()
                pygame.display.flip()
                clock.tick(SETTINGS.FPS)

            min_fps = min(fps)
            fps = sum(fps) / len(fps)

            print(f'Time: {time.time() - t}, Avg. FPS: {fps}, min FPS: {min_fps}')
            pygame.quit()
        avg_fps.append(fps)

    print(f'Avarage FPS: {sum(avg_fps) / len(avg_fps)}')
    sys.exit()