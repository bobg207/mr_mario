import pygame as pg
from settings import *
import sprites

pg.init()

screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption("New Game")

# bg_image = pg.image.load("images/Full-background.png")
# bg_image = pg.transform.scale(bg_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

hero = sprites.SpriteSheet("images/OpenGunnerHeroVer2.png")
player = sprites.Player(100, DISPLAY_HEIGHT-2*TILE_SIZE)

tile_sheet = sprites.SpriteSheet("images/tile-set.png")
brick_block = tile_sheet.image_at((96, 48, 16, 16))
brick_block = pg.transform.scale(brick_block, (TILE_SIZE, TILE_SIZE))


# ace_hearts = hero.image_at((8, 2, 44, 59))

# print(ace_hearts)

clock = pg.time.Clock()

running = True

while running:
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
    screen.fill(SKY_BLUE)

    # screen.blit(bg_image, (0, 0))
    for i, row in enumerate(LAYOUT):
        for j, col in enumerate(row):
            x_val = j * TILE_SIZE
            y_val = i * TILE_SIZE

            if col == "1":
                screen.blit(brick_block, (x_val, y_val))
    player.update(screen)

    # for i in range(1, DISPLAY_WIDTH // TILE_SIZE):
    #     pg.draw.rect(screen, WHITE, (i*TILE_SIZE, 0, 3, DISPLAY_HEIGHT))
    #
    # for i in range(1, DISPLAY_HEIGHT // TILE_SIZE):
    #     pg.draw.rect(screen, WHITE, (0, i*TILE_SIZE, DISPLAY_WIDTH, 3))

    pg.display.flip()



    clock.tick(FPS)

pg.quit()
