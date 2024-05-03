import pygame
import math
import random
import os

import player as player_file_code
import animation
import ai
# import map_creator


def rotate_player():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x = mouse_x - form_size[0] / 2 + 25
    rel_y = mouse_y - form_size[1] / 2 + 25
    angle = math.degrees(-math.atan2(rel_y, rel_x))
    return angle


def get_form_size():
    width, height = pygame.display.get_surface().get_size()
    return [width, height]


def load_image(name, color_key=None):
    fullname = name
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name, 'message:', message)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(animation.all_sprites)
        self.image = load_image("data/portal.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = free_field.mask.rect.x
        self.rect.y = free_field.mask.rect.y


class FreeField:

    def __init__(self, level_name):
        self.board = load_image(f"data/level_board--{level_name}--.png")
        self.board = pygame.transform.scale(self.board, (23170, 23170))
        self.floor = load_image(f'data/level_floor--{level_name}--.png')
        self.floor = pygame.transform.scale(self.floor, (23170, 23170))

        class Mask(pygame.sprite.Sprite):
            def __init__(self, board, pos):
                super().__init__(animation.all_sprites)
                self.board = board
                self.board = pygame.transform.scale(self.board, (23170, 23170))
                self.mask = pygame.mask.from_surface(self.board)
                self.rect = self.board.get_rect()

                self.rect.x = pos[0]
                self.rect.y = pos[1]

        self.mask = Mask(self.board, [form_size[0] / 2 - 25, form_size[1] / 2 - 25])

    def make_npc(self, size_of_entity, mode, entity):
        if mode == 0:
            while True:
                f = random.randint(-23120, -40)
                d = random.randint(-23120, -40)

                self.mask.rect = self.mask.rect.move(f, d)
                if not pygame.sprite.collide_mask(entity, self.mask):
                    break
                else:
                    self.mask.rect = self.mask.rect.move(-f, -d)
        elif mode == 1:
            while True:
                f = random.randint(0 + free_field.mask.rect.x, 23170 - size_of_entity[0] + free_field.mask.rect.x)
                d = random.randint(0 + free_field.mask.rect.y, 23170 - size_of_entity[1] + free_field.mask.rect.y)

                entity.rect = entity.rect.move(f, d)
                if not pygame.sprite.collide_mask(entity, self.mask):
                    break
                else:
                    entity.rect = entity.rect.move(-f, -d)

    def update_rects_of_entities_and_portals(self, lx, ly):
        for i in portals:
            i.rect = i.rect.move(lx, ly)
        for i in entities:
            if i != 'player':
                i.rect = i.rect.move(lx, ly)

    def render(self, mode):
        if mode == 0:
            screen.blit(self.floor, self.mask.rect)
            screen.blit(self.board, self.mask.rect)
        elif mode == 1:
            for i in portals:
                screen.blit(i.image, i.rect)

            for i in entities:
                if i == 'player':
                    screen.blit(image, player.position)
                else:
                    screen.blit(i.image, i.rect)

            for i in range(3):
                pygame.draw.circle(screen, 'black', (player.position[0] + 25, player.position[1] + 25),
                                   700.0 + float(i * 166), 166)

            for i in range(9):
                screen.blit(icon_image, (((form_size[0] - (100 * 9)) / 2) + (100 * i), (form_size[1] - 10) - 100))

            for i in eval(player.player_data['inventory']):
                if i == 0:
                    pass
                else:
                    screen.blit(pygame.transform.scale(load_image(f'data/{i}.png'), (100, 100)),
                                (((form_size[0] - (100 * 9)) / 2) + (100 *
                                                                     eval(player.player_data['inventory']).index(i)),
                                 (form_size[1] - 10) - 100))

    def get_cell(self, mouse_pos):
        column = (mouse_pos[0] - ((form_size[0] - (100 * 9)) / 2)) // 100
        row = (mouse_pos[1] - ((form_size[1] - 10) - 100)) // 100
        if 0 <= column < 9 and 0 <= row < 1:
            return int(column), int(row)
        else:
            return None


def change_map(level_out, scur_level):
    global cur_level
    global entities
    global portals
    next_level = random.choice(level_out)
    if next_level != scur_level:
        print(1)
        free_field.__init__(next_level)

        entities = []

        map_entities = ['player;0', 'robot;1;player_test_2_2', 'robto;1;player_test_2_2']

        portals = [Portal() for x in range(random.randint(1, 25))]

        for i in portals:
            while True:
                f = random.randint(0 + free_field.mask.rect.x, 23170 - 200 + free_field.mask.rect.x)
                d = random.randint(0 + free_field.mask.rect.y, 23170 - 200 + free_field.mask.rect.y)

                i.rect = i.rect.move(f, d)
                if not pygame.sprite.collide_mask(i, free_field.mask):
                    break
                else:
                    i.rect = i.rect.move(-f, -d)

        for i in map_entities:
            if i.split(';')[1] == '0':
                exec(i.split(';')[0])
            elif i.split(';')[1] == '1':
                exec(f"ai.{i.split(';')[0]} = ai.Entity(False, entities, '{i.split(';')[0]}', player.position, " +
                     f'animation.AnimatedSprite(load_image("data/{i.split(";")[2]}.png"), 9, 1, 0, 0),' +
                     ' free_field.mask, animation.all_sprites, load_image("data/collision_____________________.png"))')

        for i in map_entities:
            if i != 'player;0':
                entities.append(eval(f"ai.{i.split(';')[0]}"))
            else:
                entities.append('player')
        del map_entities

        for i in entities:
            if i != 'player':
                i.update_danger()

        for i in entities:
            if i == 'player':
                free_field.make_npc([50, 50], 0, player)
            else:
                free_field.make_npc([50, 50], 1, i)
        cur_level = next_level


clock = pygame.time.Clock()
pygame.init()

display_info = pygame.display.Info()
monitor_width = display_info.current_w
monitor_height = display_info.current_h

screen = pygame.display.set_mode((monitor_width, monitor_height - 50), pygame.RESIZABLE)
pygame.display.set_caption('Project T.U.P.')
del monitor_height, monitor_width, display_info

form_size = get_form_size()

cur_level = '0'

free_field = FreeField('0')

player = player_file_code.Player('johua blake', [form_size[0] / 2 - 50, form_size[1] / 2 - 50],
                                 animation.AnimatedSprite(load_image("data/player_test_2_2.png"), 9, 1, 0, 0),
                                 animation.all_sprites, load_image("data/collision_____________________.png"))
player.read_player_stats()
inventory = eval(player.player_data['inventory'])

icon_image = load_image("data/inventory_icon.png")
icon_image = pygame.transform.scale(icon_image, (100, 100))

items = ['empty', 'black_apple', 'flash_bang']
code_of_items = {'empty':
                 '''pass''',
                 'black_apple':
                 '''for i in [random.choice(portals)]:
    f = player.position[0] - i.rect[0] # (i.rect[0] - player.position[0]) // 2
    d = player.position[1] - i.rect[1] # (i.rect[1] - player.position[0]) // 2
    
    free_field.mask.rect = free_field.mask.rect.move(f, d)
    free_field.update_rects_of_entities_and_portals(f, d)
    
''',
                 'flash_bang':
                 '''for i in entities:
    if i != 'player':
        i.wait_(50)
        screen_color = [255, 255, 255, 255]
        n = 50'''}

player_angle = 0
tick = 0
n = 0
screen_color = [255, 255, 255, 255]

entities = []

map_entities = ['player;0', 'robot;1;player_test_2_2', 'robto;1;player_test_2_2']

portals = [Portal() for x in range(random.randint(1, 25))]

for i in portals:
    while True:
        f = random.randint(0 + free_field.mask.rect.x, 23170 - 200 + free_field.mask.rect.x)
        d = random.randint(0 + free_field.mask.rect.y, 23170 - 200 + free_field.mask.rect.y)

        i.rect = i.rect.move(f, d)
        if not pygame.sprite.collide_mask(i, free_field.mask):
            break
        else:
            i.rect = i.rect.move(-f, -d)

for i in map_entities:
    if i.split(';')[1] == '0':
        exec(i.split(';')[0])
    elif i.split(';')[1] == '1':
        exec(f"ai.{i.split(';')[0]} = ai.Entity(False, entities, '{i.split(';')[0]}', player.position, " +
             f'animation.AnimatedSprite(load_image("data/{i.split(";")[2]}.png"), 9, 1, 0, 0), free_field.mask,' +
             ' animation.all_sprites, load_image("data/collision_____________________.png"))')

for i in map_entities:
    if i != 'player;0':
        entities.append(eval(f"ai.{i.split(';')[0]}"))
    else:
        entities.append('player')
del map_entities

for i in entities:
    if i != 'player':
        i.update_danger()

for i in entities:
    if i == 'player':
        free_field.make_npc([50, 50], 0, player)
    else:
        free_field.make_npc([50, 50], 1, i)

list_level_out = ['1']

running = True
while running:
    if tick == 2:
        tick = 0
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if free_field.get_cell(pygame.mouse.get_pos()) is not None:
                    current_item = inventory[free_field.get_cell(pygame.mouse.get_pos())[0]]
                    print(code_of_items[items[current_item]])
                    a = compile(code_of_items[items[current_item]], '<string>', 'exec')
                    print(a)
                    exec(a)
                    del a

    for i in entities:
        if i == 'player':
            player_angle = rotate_player()
            image = pygame.transform.rotate(player.image_class.image, int(player_angle))
            player.mask = pygame.mask.from_surface(image)
        else:
            i.perseverance(player.position)
            i.image = i.image_class.image

    for i in portals:
        if pygame.sprite.collide_mask(player, i):
            change_map(list_level_out, cur_level)

    if tick == 1:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_a]:
                free_field.mask.rect = free_field.mask.rect.move(45, 0)
                free_field.update_rects_of_entities_and_portals(45, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(-45, 0)
                    free_field.update_rects_of_entities_and_portals(-45, 0)
            if keys[pygame.K_d]:
                free_field.mask.rect = free_field.mask.rect.move(-45, 0)
                free_field.update_rects_of_entities_and_portals(-45, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(45, 0)
                    free_field.update_rects_of_entities_and_portals(45, 0)
            if keys[pygame.K_w]:
                free_field.mask.rect = free_field.mask.rect.move(0, 45)
                free_field.update_rects_of_entities_and_portals(0, 45)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, -45)
                    free_field.update_rects_of_entities_and_portals(0, -45)
            if keys[pygame.K_s]:
                free_field.mask.rect = free_field.mask.rect.move(0, -45)
                free_field.update_rects_of_entities_and_portals(0, -45)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, 45)
                    free_field.update_rects_of_entities_and_portals(0, 45)

        elif keys[pygame.K_LCTRL]:
            if keys[pygame.K_a]:
                free_field.mask.rect = free_field.mask.rect.move(6, 0)
                free_field.update_rects_of_entities_and_portals(6, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(-6, 0)
                    free_field.update_rects_of_entities_and_portals(-6, 0)
            if keys[pygame.K_d]:
                free_field.mask.rect = free_field.mask.rect.move(-6, 0)
                free_field.update_rects_of_entities_and_portals(-6, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(6, 0)
                    free_field.update_rects_of_entities_and_portals(6, 0)
            if keys[pygame.K_w]:
                free_field.mask.rect = free_field.mask.rect.move(0, 6)
                free_field.update_rects_of_entities_and_portals(0, 6)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, -6)
                    free_field.update_rects_of_entities_and_portals(0, -6)
            if keys[pygame.K_s]:
                free_field.mask.rect = free_field.mask.rect.move(0, -6)
                free_field.update_rects_of_entities_and_portals(0, -6)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, 6)
                    free_field.update_rects_of_entities_and_portals(0, 6)
        else:
            if keys[pygame.K_a]:
                free_field.mask.rect = free_field.mask.rect.move(20, 0)
                free_field.update_rects_of_entities_and_portals(20, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(-20, 0)
                    free_field.update_rects_of_entities_and_portals(-20, 0)
            if keys[pygame.K_d]:
                free_field.mask.rect = free_field.mask.rect.move(-20, 0)
                free_field.update_rects_of_entities_and_portals(-20, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(20, 0)
                    free_field.update_rects_of_entities_and_portals(20, 0)
            if keys[pygame.K_w]:
                free_field.mask.rect = free_field.mask.rect.move(0, 20)
                free_field.update_rects_of_entities_and_portals(0, 20)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, -20)
                    free_field.update_rects_of_entities_and_portals(0, -20)
            if keys[pygame.K_s]:
                free_field.mask.rect = free_field.mask.rect.move(0, -20)
                free_field.update_rects_of_entities_and_portals(0, -20)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, 20)
                    free_field.update_rects_of_entities_and_portals(0, 20)

        animation.all_sprites.update()

    free_field.render(0)
    free_field.render(1)
    s = 0

    if n != 0:
        s = pygame.Surface(form_size, pygame.SRCALPHA)
        s.fill(screen_color)
        screen.blit(s, (0, 0))
        n -= 1
        screen_color[3] -= 5
    else:
        del s

    pygame.display.flip()

    tick += 1

    clock.tick(30)

pygame.quit()
