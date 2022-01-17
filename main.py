import pygame as pg
from settings import *
import sprites


pg.init()


def draw_layout():
    for i, row in enumerate(LAYOUT):
        for j, col in enumerate(row):
            x_val = j * TILE_SIZE
            y_val = i * TILE_SIZE

            if col == "1":
                SCREEN.blit(BROWN_BLOCK, (x_val, y_val))
            elif col == "2":
                SCREEN.blit(YELLOW_BRICK, (x_val, y_val))
            elif col == "3":
                SCREEN.blit(BROWN_BOX, (x_val, y_val))
            elif col == "4":
                SCREEN.blit(SPIKES, (x_val, y_val))
            elif col == "5":
                SCREEN.blit(DOORS[0], (x_val, y_val))
            elif col == "6":
                SCREEN.blit(YELLOW_BRICK, (x_val, y_val))
            elif col == "7":
                SCREEN.blit(PLATFORM, (x_val, y_val))
            elif col == "8":
                SCREEN.blit(LADDER, (x_val, y_val))
            elif col == "9":
                SCREEN.blit(KEY, (x_val, y_val))
            elif col == "a":
                pass


pg.display.set_caption("New Game")

# bg_image = pg.image.load("images/Full-background.png")
# bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# hero = sprites.SpriteSheet("images/OpenGunnerHeroVer2.png")
# player = sprites.Player(100, DISPLAY_HEIGHT-2*TILE_SIZE)

layout = sprites.Layout(LAYOUT, TILE_SIZE)
clock = pg.time.Clock()

running = True

while running:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
    SCREEN.fill(GREY)

    # screen.blit(brick_block, (100, 100))
    # player.update(screen)
    # draw_layout()
    layout.draw(SCREEN)
    # for i in range(1, DISPLAY_WIDTH // TILE_SIZE):
    #     pg.draw.rect(screen, WHITE, (i*TILE_SIZE, 0, 3, DISPLAY_HEIGHT))
    #
    # for i in range(1, DISPLAY_HEIGHT // TILE_SIZE):
    #     pg.draw.rect(screen, WHITE, (0, i*TILE_SIZE, DISPLAY_WIDTH, 3))

    pg.display.flip()

    clock.tick(FPS)

pg.quit()
