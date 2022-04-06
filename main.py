import pygame as pg
from settings import *
import sprites

# initialize all game elements
pg.init()
screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption("New Game")
game_layout = sprites.Layout(LAYOUT, TILE_SIZE)
layout_list = game_layout.get_layout()
player_grp = pg.sprite.Group()
player = sprites.Player(100, DISPLAY_HEIGHT - 3 * TILE_SIZE, TILE_SIZE, layout_list)
player_grp.add(player)


def game_start():
    screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pg.time.Clock()

    start_text1 = 'Press Enter to start playing'
    start_text2 = 'or ESC to quit'
    font = pg.font.SysFont('Courier', 30, True, False)
    text1 = font.render(start_text1, True, BLACK)
    text2 = font.render(start_text2, True, BLACK)

    started = False

    while not started:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                quit()

            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                started = True

        screen.fill(WHITE)

        screen.blit(text1, [100, 100])
        screen.blit(text2, [200, 200])

        pg.display.flip()

        clock.tick(FPS)


def game_over(score):
    pg.font.init()
    go_screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pg.time.Clock()

    start_text1 = f'Your final score is: {score}'
    start_text2 = 'Click on a button to proceed.'
    restart_text = 'Restart'
    quit_text = 'Quit'

    font = pg.font.SysFont('Courier', 30, True, False)
    text1 = font.render(start_text1, True, BLACK)
    text2 = font.render(start_text2, True, BLACK)
    text3 = font.render(restart_text, True, BLACK)
    text4 = font.render(quit_text, True, BLACK)

    started = False

    while not started:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                quit()

        click = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        if click[0] is True and 200 <= mouse_pos[0] <= 350 and 400 <= mouse_pos[1] <= 450:
            started = True

        if click[0] is True and 400 <= mouse_pos[0] <= 550 and 400 <= mouse_pos[1] <= 450:
            quit()

        go_screen.fill(WHITE)

        pg.draw.rect(go_screen, GREEN, (200, 400, 150, 50))
        pg.draw.rect(go_screen, RED, (400, 400, 150, 50))

        go_screen.blit(text1, [150, 100])
        go_screen.blit(text2, [100, 200])
        go_screen.blit(text3, [200, 400])
        go_screen.blit(text4, [420, 400])

        pg.display.flip()

        clock.tick(FPS)

    return True


def reset_level(new_level):
    # need vars too be global so changes can be sent/received
    global player, player_grp, game_layout, layout_list

    # empty any sprite groups, tile list is emptied in "create_layout" method below
    game_layout.platform_grp.empty()
    player_grp.empty()

    # create new level
    game_layout.create_layout(new_level)
    layout_list = game_layout.get_layout()
    player_grp = pg.sprite.Group()
    player = sprites.Player(100, DISPLAY_HEIGHT - 3 * TILE_SIZE, TILE_SIZE, layout_list)
    player_grp.add(player)

    return layout_list


def game_play():
    # need vars too be global so changes can be sent/received
    global player, player_grp, game_layout, screen

    level = 1
    max_level = 2

    # use reset function to load the initial level
    layout_lis = reset_level(level)
    platforms = game_layout.get_sprite_groups()
    screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    clock = pg.time.Clock()

    running = True

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

        # check for collision with "Exit", the tile has length = 3
        for tile in layout_lis:
            if tile[1].colliderect(player.rect.x + 3, player.rect.y,
                                   player.rect.width, player.rect.height) and len(tile) == 3:
                level += 1

                # make sure there are enough levels to go to
                if level <= max_level:

                    # call reset function for next level AND get returned layout list
                    layout_lis = reset_level(level)

                # if no more levels end the "game_play" and go to "game_over"
                else:
                    running = False

        screen.fill(GREY)

        game_layout.draw(screen)
        player.update(screen)
        platforms.update(screen)

        pg.display.flip()

        clock.tick(FPS)

    pg.quit()


playing = True
game_start()
while playing:
    game_play()
    playing = game_over(5)  # not keeping score yet, so score is hardcoded

pg.quit()
