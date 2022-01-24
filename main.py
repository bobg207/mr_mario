import pygame as pg
from settings import *
import sprites


pg.init()

pg.display.set_caption("New Game")

# bg_image = pg.image.load("images/Full-background.png")
# bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

layout = sprites.Layout(LAYOUT, TILE_SIZE)
layout_list = layout.get_layout()
player = sprites.Player(100, DISPLAY_HEIGHT-3*TILE_SIZE, TILE_SIZE, layout_list)

clock = pg.time.Clock()

running = True

while running:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
    SCREEN.fill(GREY)

    layout.draw(SCREEN)
    player.update(SCREEN)

    pg.display.flip()

    clock.tick(FPS)

pg.quit()
