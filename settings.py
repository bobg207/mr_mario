import pygame as pg
import sprites

pg.init()

WHITE = (255, 255, 255)
RED = (87, 9, 9)
GREEN = (12, 148, 37)
BLUE = (2, 0, 94)
BLACK = (0, 0, 0)
SKY_BLUE = (66, 203, 245)
GREY = (63, 50, 51)

# width by height
FPS = 60
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
SCREEN = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

GROUND_LEVEL = 485
TILE_SIZE = 25

LAYOUT = [
    '11111111111111111111111111111111',
    '10000000000000000000000000000050',
    '10000000000000000000000000000000',
    '10000000000000000000000000011111',
    '10000007000000000000700000000001',
    '10000000000000700000000000000001',
    '19000000000000000000000000000001',
    '11110000000000000000000000000001',
    '10000000000000000000000000000001',
    '10000000000000000000000000000a01',
    '10000000000000000000000000001111',
    '18111000700000000000000000000001',
    '10000000000000000000000000000001',
    '10000000000000000000000000000001',
    '11800000000000000000000000000001',
    '10000000000100007000000700000001',
    '10000000011000000000000000000001',
    '11111000000000000000000000000111',
    '10000000000000000000000000000001',
    '10000000000000000000000000000001',
    '10000000000000300003330000330001',
    '10000000000003300003330000330001',
    '10000000000033300003330000330001',
    '22222222222222200002220000222222']

# tile_sheet = sprites.SpriteSheet("images/layout3.png")
# KEY = tile_sheet.image_at((282, 152, 30, 14))
# KEY = pg.transform.scale(KEY, (TILE_SIZE, TILE_SIZE))
# LADDER = tile_sheet.image_at((432, 23, 25, 86))
# LADDER = pg.transform.scale(LADDER, (TILE_SIZE, 3*TILE_SIZE))
# PLATFORM = tile_sheet.image_at((316, 8, 121, 11))
# PLATFORM = pg.transform.scale(PLATFORM, (2*TILE_SIZE, .5*TILE_SIZE))
# BROWN_BLOCK = tile_sheet.image_at((22, 24, 36, 36))
# BROWN_BLOCK = pg.transform.scale(BROWN_BLOCK, (TILE_SIZE, TILE_SIZE))
# YELLOW_BRICK = tile_sheet.image_at((22, 294, 36, 36))
# YELLOW_BRICK = pg.transform.scale(YELLOW_BRICK, (TILE_SIZE, TILE_SIZE))
# BROWN_BOX = tile_sheet.image_at((340, 25, 36, 36))
# BROWN_BOX = pg.transform.scale(BROWN_BOX, (TILE_SIZE, TILE_SIZE))
# SPIKES = tile_sheet.image_at((400, 116, 46, 29), -1)
# SPIKES = pg.transform.scale(SPIKES, (TILE_SIZE, TILE_SIZE))
# DOORS = []
# door1 = tile_sheet.image_at((172, 340, 30, 44))
# door1 = pg.transform.scale(door1, (2*TILE_SIZE, 2*TILE_SIZE))
# DOORS.append(door1)
# door2 = tile_sheet.image_at((215, 340, 30, 44))
# door2 = pg.transform.scale(door2, (2*TILE_SIZE, 2*TILE_SIZE))
# DOORS.append(door2)
# door3 = tile_sheet.image_at((263, 340, 30, 44))
# door3 = pg.transform.scale(door3, (2*TILE_SIZE, 2*TILE_SIZE))
# DOORS.append(door3)
# door4 = tile_sheet.image_at((310, 340, 30, 44))
# door4 = pg.transform.scale(door4, (2*TILE_SIZE, 2*TILE_SIZE))
# DOORS.append(door4)
# door5 = tile_sheet.image_at((357, 340, 30, 44))
# door5 = pg.transform.scale(door5, (2*TILE_SIZE, 2*TILE_SIZE))
# DOORS.append(door5)
# door6 = tile_sheet.image_at((404, 340, 30, 44))
# door6 = pg.transform.scale(door6, (2*TILE_SIZE, 2*TILE_SIZE))
# DOORS.append(door6)
