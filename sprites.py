# This class handles sprite sheets
# https://www.pygame.org/wiki/Spritesheet
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame as pg
from settings import *
import random

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
    def __init__(self, x, y, tile_size, tiles):
        pg.sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.tiles = tiles
        self.stand_rt = None
        self.stand_lft = None
        self.run_rt_list = []
        self.run_lft_list = None
        self.load_images()
        self.image = self.stand_rt
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.rect.width = 33
        self.image_delay = 100
        self.last = pg.time.get_ticks()
        self.current_frame = 0
        self.right = True
        self.left = False
        self.jumping = False
        self.falling = False
        self.velo_y = 8
        self.max_height = 30

    def update(self, display):
        # create delta's
        dx = 0
        dy = 0

        # get key presses and update delta's
        keys = pg.key.get_pressed()

        # jumping logic
        if keys[pg.K_SPACE] and not self.jumping and not self.falling:
            self.velo_y = -13
            self.jumping = True
        if not keys[pg.K_SPACE]:
            self.jumping = False

        # left/right movement
        if keys[pg.K_RIGHT]:
            self.left = False
            self.right = True
            dx = 5
            now = pg.time.get_ticks()
            if now - self.last >= self.image_delay:
                self.last = now
                self.current_frame = (self.current_frame+1) % len(self.run_rt_list)
                self.image = self.run_rt_list[self.current_frame]
        if keys[pg.K_LEFT]:
            self.left = True
            self.right = False
            dx = -5
            now = pg.time.get_ticks()
            if now - self.last >= self.image_delay:
                self.last = now
                self.current_frame = (self.current_frame + 1) % len(self.run_lft_list)
                self.image = self.run_lft_list[self.current_frame]
        if not keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.current_frame = 0
            dx = 0
            if self.right:
                self.image = self.stand_rt
            elif self.left:
                self.image = self.stand_lft

        # add gravity
        self.velo_y += 1
        if self.velo_y < 0:
            self.jumping = True
            self.falling = False
        else:
            self.jumping = False
            self.falling = True

        # set terminal velocity
        if self.velo_y > 10:
            self.velo_y = 10
        dy += self.velo_y

        # check for collision
        for tile in self.tiles:
            if tile[1].colliderect(self.rect.x+dx, self.rect.y,
                                   self.rect.width, self.rect.height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y+dy,
                                   self.rect.width, self.rect.height):
                # jumping and collide with bottom of platform
                if self.velo_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.velo_y = 0
                    self.jumping = False
                    self.falling = True
                # falling and collide with ground
                elif self.velo_y > 0:
                    dy = tile[1].top - self.rect.bottom
                    self.velo_y = 0
                    self.falling = False
                    self.jumping = False

        # update position
        self.rect.x += dx
        self.rect.y += dy
        # print(self.rect.width)
        # draw to screen

        pg.draw.rect(display, (0, 0, 0), self.rect)
        display.blit(self.image, self.rect)

        if self.rect.top >= 600:
            self.kill()

    def load_images(self):
        player_size = 2*self.tile_size
        skeletons = SpriteSheet("images/skeleton.png")
        self.stand_rt = skeletons.image_at((22, 719, 33, 44), -1)
        self.stand_rt = pg.transform.scale(self.stand_rt, (player_size, player_size))
        self.stand_lft = pg.transform.flip(self.stand_rt, True, False)
        skel1 = skeletons.image_at((80, 718, 33, 44), -1)
        self.run_rt_list.append(skel1)
        skel2 = skeletons.image_at((143, 718, 33, 44), -1)
        self.run_rt_list.append(skel2)
        skel3 = skeletons.image_at((207, 718, 33, 44), -1)
        self.run_rt_list.append(skel3)
        skel4 = skeletons.image_at((270, 718, 33, 44), -1)
        self.run_rt_list.append(skel4)
        skel5 = skeletons.image_at((333, 718, 33, 44), -1)
        self.run_rt_list.append(skel5)
        skel6 = skeletons.image_at((398, 718, 33, 44), -1)
        self.run_rt_list.append(skel6)
        skel7 = skeletons.image_at((462, 718, 33, 44), -1)
        self.run_rt_list.append(skel7)
        skel8 = skeletons.image_at((527, 718, 33, 44), -1)
        self.run_rt_list.append(skel8)
        self.run_rt_list = [pg.transform.scale(image, (player_size, player_size)) for image in self.run_rt_list]
        self.run_lft_list = [pg.transform.flip(player, True, False) for player in self.run_rt_list]


class Walls:
    def __init__(self, x, y):
        pass


class Platform(pg.sprite.Sprite):
    def __init__(self, direction, x, y, image, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.max_move = 50
        self.y_loc = 0
        self.x_loc = 0
        self.up = True
        self.down = False
        self.right = True
        self.left = False
        if self.direction == 'vertical':
            self.dy = speed
            self.dx = 0
        elif self.direction == "horizontal":
            self.dx = speed
            self.dy = 0

    def update(self, display):
        if self.y_loc >= self.max_move or self.y_loc <= -1*self.max_move:
            self.dy *= -1
        if self.x_loc >= self.max_move or self.x_loc <= -1*self.max_move:
            self.dx *= -1

        self.x_loc += self.dx
        self.y_loc += self.dy

        self.rect.y += self.dy
        self.rect.x += self.dx

        display.blit(self.image, self.rect)


class Layout:
    def __init__(self, layout, tile_size):
        self.layout = layout
        self.tile_size = tile_size

        self.ladder = None
        self.platform = None
        self.brown_block = None
        self.yellow_brick = None
        self.brown_box = None
        self.spikes = None
        self.doors = []
        self.get_images()
        self.tile_list = []
        self.platform_grp = pg.sprite.Group()


    def create_layout(self, level):
        counter_v = 0
        counter_h = 0
        self.tile_list = []
        level_layout = self.layout[level-1]
        for i, row in enumerate(level_layout):
            for j, col in enumerate(row):
                x_val = j * self.tile_size
                y_val = i * self.tile_size

                if col == "1":
                    img_rect = self.brown_block.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.brown_block, img_rect)
                    self.tile_list.append(tile)
                elif col == "2":
                    img_rect = self.yellow_brick.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.yellow_brick, img_rect)
                    self.tile_list.append(tile)
                elif col == "3":
                    img_rect = self.brown_box.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.brown_box, img_rect)
                    self.tile_list.append(tile)
                elif col == "4":
                    speed_h = (counter_h % 2) + 1
                    vert_plat = Platform("horizontal", x_val, y_val, self.platform, speed_h)
                    self.platform_grp.add(vert_plat)
                    tile = (self.platform, vert_plat.rect)
                    self.tile_list.append(tile)
                    counter_h += 1
                elif col == "5":
                    img_rect = self.doors[0].get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    # adding a 3rd value to tile to differentiate the it as an exit tile
                    tile = (self.doors[0], img_rect, 1)
                    self.tile_list.append(tile)
                elif col == "7":
                    speed_y = (counter_v % 2) + 1
                    vert_plat = Platform("vertical", x_val, y_val, self.platform, speed_y)
                    self.platform_grp.add(vert_plat)
                    tile = (self.platform, vert_plat.rect)
                    self.tile_list.append(tile)
                    counter_v += 1
                elif col == "8":
                    img_rect = self.ladder.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.ladder, img_rect)
                    self.tile_list.append(tile)
                elif col == "9":
                    img_rect = self.key.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.key, img_rect)
                    self.tile_list.append(tile)
                elif col == "a":
                    pass

    def draw(self, display):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])

    def get_layout(self):
        return self.tile_list

    def get_sprite_groups(self):
        return self.platform_grp

    def get_images(self):
        tile_sheet = SpriteSheet("images/layout3.png")
        key = tile_sheet.image_at((282, 152, 30, 14))
        self.key = pg.transform.scale(key, (self.tile_size, self.tile_size))
        ladder = tile_sheet.image_at((432, 23, 25, 86))
        self.ladder = pg.transform.scale(ladder, (self.tile_size, 3 * self.tile_size))
        platform = tile_sheet.image_at((316, 8, 121, 11))
        self.platform = pg.transform.scale(platform, (2 * self.tile_size, .5 * self.tile_size))
        brown_block = tile_sheet.image_at((22, 24, 36, 36))
        self.brown_block = pg.transform.scale(brown_block, (self.tile_size, self.tile_size))
        yellow_brick = tile_sheet.image_at((22, 294, 36, 36))
        self.yellow_brick = pg.transform.scale(yellow_brick, (self.tile_size, self.tile_size))
        brown_box = tile_sheet.image_at((340, 25, 36, 36))
        self.brown_box = pg.transform.scale(brown_box, (self.tile_size, self.tile_size))
        spikes = tile_sheet.image_at((400, 116, 46, 29), -1)
        self.spikes = pg.transform.scale(spikes, (self.tile_size, self.tile_size))
        self.doors = []
        door1 = tile_sheet.image_at((172, 340, 30, 44))
        door1 = pg.transform.scale(door1, (2 * self.tile_size, 2 * self.tile_size))
        self.doors.append(door1)
        door2 = tile_sheet.image_at((215, 340, 30, 44))
        door2 = pg.transform.scale(door2, (2 * self.tile_size, 2 * self.tile_size))
        self.doors.append(door2)
        door3 = tile_sheet.image_at((263, 340, 30, 44))
        door3 = pg.transform.scale(door3, (2 * self.tile_size, 2 * self.tile_size))
        self.doors.append(door3)
        door4 = tile_sheet.image_at((310, 340, 30, 44))
        door4 = pg.transform.scale(door4, (2 * self.tile_size, 2 * self.tile_size))
        self.doors.append(door4)
        door5 = tile_sheet.image_at((357, 340, 30, 44))
        door5 = pg.transform.scale(door5, (2 * self.tile_size, 2 * self.tile_size))
        self.doors.append(door5)
        door6 = tile_sheet.image_at((404, 340, 30, 44))
        door6 = pg.transform.scale(door6, (2 * self.tile_size, 2 * self.tile_size))
        self.doors.append(door6)
