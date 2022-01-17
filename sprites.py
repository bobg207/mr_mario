# This class handles sprite sheets
# https://www.pygame.org/wiki/Spritesheet
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame as pg
from settings import *

pg.init()


class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pg.image.load(filename).convert()
        except pg.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, color_key=None):
        """Load a specific image from a specific rectangle.
        rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pg.RLEACCEL)
        return image

    def images_at(self, rects, color_key=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, color_key) for rect in rects]

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
                         y_margin=0, y_padding=0, width=None, height=None, color_key=None):
        """Load a grid of images.
        y_margin is the space between the top of the sheet and top of the first
        row. y_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for x. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        if width and height:
            x_sprite_size = width
            y_sprite_size = height
        else:
            # To calculate the size of each sprite, subtract the two margins,
            #   and the padding between each row, then divide by num_cols.
            # Same reasoning for y.
            x_sprite_size = (sheet_width - 2 * x_margin
                             - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                             - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, color_key)


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.run_rt_list, self.run_lft_list = self.load_images()
        self.image = self.run_rt_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def load_images(self):
        x_margin = 24
        y_margin = 315
        x_pad = 1
        y_pad = 0
        width = 50
        height = 50
        hero = SpriteSheet("images/OpenGunnerHeroVer2.png")
        run_rt_list = hero.load_grid_images(1, 8, x_margin, x_pad, y_margin, y_pad, width, height, -1)
        for image in run_rt_list:
            pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        run_lft_list = [pg.transform.flip(player, True, False) for player in self.run_rt_list]

        return run_rt_list, run_lft_list


class Walls:
    def __init__(self, x, y):
        pass


class Platform(pg.sprite.Sprite):
    def __init__(self, move, x, y):
        pg.sprite.Sprite.__init__(self)
        self.move = move


class Layout:
    def __init__(self, level_layout, tile_size):
        tile_sheet = SpriteSheet("images/layout3.png")
        key = tile_sheet.image_at((282, 152, 30, 14))
        key = pg.transform.scale(key, (tile_size, tile_size))
        ladder = tile_sheet.image_at((432, 23, 25, 86))
        ladder = pg.transform.scale(ladder, (tile_size, 3 * tile_size))
        platform = tile_sheet.image_at((316, 8, 121, 11))
        platform = pg.transform.scale(platform, (2 * tile_size, .5 * tile_size))
        brown_block = tile_sheet.image_at((22, 24, 36, 36))
        brown_block = pg.transform.scale(brown_block, (tile_size, tile_size))
        yellow_brick = tile_sheet.image_at((22, 294, 36, 36))
        yellow_brick = pg.transform.scale(yellow_brick, (tile_size, tile_size))
        brown_box = tile_sheet.image_at((340, 25, 36, 36))
        brown_box = pg.transform.scale(brown_box, (tile_size, tile_size))
        spikes = tile_sheet.image_at((400, 116, 46, 29), -1)
        spikes = pg.transform.scale(spikes, (tile_size, tile_size))
        doors = []
        door1 = tile_sheet.image_at((172, 340, 30, 44))
        door1 = pg.transform.scale(door1, (2 * tile_size, 2 * tile_size))
        doors.append(door1)
        door2 = tile_sheet.image_at((215, 340, 30, 44))
        door2 = pg.transform.scale(door2, (2 * tile_size, 2 * tile_size))
        doors.append(door2)
        door3 = tile_sheet.image_at((263, 340, 30, 44))
        door3 = pg.transform.scale(door3, (2 * tile_size, 2 * tile_size))
        doors.append(door3)
        door4 = tile_sheet.image_at((310, 340, 30, 44))
        door4 = pg.transform.scale(door4, (2 * tile_size, 2 * tile_size))
        doors.append(door4)
        door5 = tile_sheet.image_at((357, 340, 30, 44))
        door5 = pg.transform.scale(door5, (2 * tile_size, 2 * tile_size))
        doors.append(door5)
        door6 = tile_sheet.image_at((404, 340, 30, 44))
        door6 = pg.transform.scale(door6, (2 * tile_size, 2 * tile_size))
        doors.append(door6)

        self.tile_list = []

        for i, row in enumerate(level_layout):
            for j, col in enumerate(row):
                x_val = j * tile_size
                y_val = i * tile_size

                if col == "1":
                    img_rect = brown_block.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (brown_block, img_rect)
                    self.tile_list.append(tile)
                elif col == "2":
                    img_rect = yellow_brick.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (yellow_brick, img_rect)
                    self.tile_list.append(tile)
                elif col == "3":
                    img_rect = brown_box.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (brown_box, img_rect)
                    self.tile_list.append(tile)
                elif col == "5":
                    img_rect = doors[0].get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (doors[0], img_rect)
                    self.tile_list.append(tile)
                elif col == "7":
                    img_rect = platform.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (platform, img_rect)
                    self.tile_list.append(tile)
                elif col == "8":
                    img_rect = ladder.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (ladder, img_rect)
                    self.tile_list.append(tile)
                elif col == "9":
                    img_rect = key.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (key, img_rect)
                    self.tile_list.append(tile)
                elif col == "a":
                    pass

    def draw(self, display):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])
