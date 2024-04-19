import pygame
import math
import random

import player as player_file_code
import animation
import ai
#import map_creator


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
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class FreeField:

    def __init__(self):
        self.board = load_image("data/board.png")
        self.board = pygame.transform.scale(self.board, (23170, 23170))
        self.floor = load_image('data/full_floor.png')
        self.floor = pygame.transform.scale(self.floor, (23170, 23170))

        class Mask(pygame.sprite.Sprite):
            def __init__(self, board):
                super().__init__(animation.all_sprites)
                self.board = board
                self.board = pygame.transform.scale(self.board, (23170, 23170))
                self.mask = pygame.mask.from_surface(self.board)
                self.rect = self.board.get_rect()

                self.rect.x = form_size[0] / 2 - 25
                self.rect.y = form_size[1] / 2 - 25

        self.mask = Mask(self.board)

    def make_npc(self, size_of_entity, mode, entity):
        if mode == 0:
            while True:
                f = -40  # random.randint(-23120, -40)
                d = -40  # random.randint(-23120, -40)

                free_field.mask.rect = free_field.mask.rect.move(f, d)
                if not pygame.sprite.collide_mask(entity, free_field.mask):
                    break
                else:
                    free_field.mask.rect = free_field.mask.rect.move(-f, -d)
        elif mode == 1:
            while True:
                f = 0 + free_field.mask.rect.x + 20  # random.randint(0 + free_field.mask.rect.x, 23170 - size_of_entity[0] + free_field.mask.rect.x)  # random.randint(free_field.mask.rect.x - 1, free_field.mask.rect.x + 1)  # random.randint(0, 23170)
                d = 0 + free_field.mask.rect.y + 20  # random.randint(0 + free_field.mask.rect.y, 23170 - size_of_entity[1] + free_field.mask.rect.y)  # random.randint(free_field.mask.rect.y - 1, free_field.mask.rect.y + 1)  # random.randint(0, 23170)

                entity.rect = entity.rect.move(f, d)
                if not pygame.sprite.collide_mask(entity, free_field.mask):
                    break
                else:
                    entity.rect = entity.rect.move(-f, -d)

    def update_rects_of_entities(self, lx, ly):
        for i in entities:
            if i != 'player':
                i.rect = i.rect.move(lx, ly)

    def render(self, mode):
        if mode == 0:
            screen.blit(self.floor, self.mask.rect)
            screen.blit(self.board, self.mask.rect)
        elif mode == 1:
            for i in entities:
                if i == 'player':
                    screen.blit(image, player.position)
                else:
                    screen.blit(i.image, i.rect)
            for i in range(9):
                #print(i)
                screen.blit(icon_image, (((form_size[0] - (100 * 9)) / 2) + (100 * i), (form_size[1] - 10) - 100))
        #screen.blit(player.surface, player.position)


clock = pygame.time.Clock()
pygame.init()

display_info = pygame.display.Info()
monitor_width = display_info.current_w
monitor_height = display_info.current_h

screen = pygame.display.set_mode((monitor_width, monitor_height - 50), pygame.RESIZABLE)
pygame.display.set_caption('Project T.U.P.')
del monitor_height, monitor_width, display_info

form_size = get_form_size()

free_field = FreeField()

player = player_file_code.Player('johua blake', [form_size[0] / 2 - 50, form_size[1] / 2 - 50],
                                 animation.AnimatedSprite(load_image("data/player_test_2_2.png"), 9, 1, 0, 0),
                                 animation.all_sprites)

icon_image = load_image("data/inventory_icon.png")
icon_image = pygame.transform.scale(icon_image, (100, 100))
player_angle = 0
tick = 0
entities = []

map_entities = ['player;0', 'robot;1;player_test_2_2', 'robto;1;player_test_2_2']

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

running = True
while running:
    if tick == 2:
        tick = 0
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            past_form_size = player.position
            form_size = get_form_size()
            player.position = [form_size[0] / 2 - 50, form_size[1] / 2 - 50]
            '''print(-(past_form_size[0] - form_size[0]), -(past_form_size[1] - form_size[1]))
            free_field.mask.rect = free_field.mask.rect.move(-(past_form_size[0] - form_size[0]),
                                                             -(past_form_size[1] - form_size[1]))
            free_field.update_rects_of_entities(-(past_form_size[0] - form_size[0]),
                                                -(past_form_size[1] - form_size[1]))'''
            print(-(past_form_size[0] - player.position[0]), -(past_form_size[1] - player.position[1]))
            free_field.mask.rect = free_field.mask.rect.move(-(past_form_size[0] - player.position[0]),
                                                             -(past_form_size[1] - player.position[1]))
            free_field.update_rects_of_entities(-(past_form_size[0] - player.position[0]),
                                                -(past_form_size[1] - player.position[1]))

    for i in entities:
        if i == 'player':
            player_angle = rotate_player()
            image = pygame.transform.rotate(player.image_class.image, int(player_angle))
            player.mask = pygame.mask.from_surface(image)
        else:
            i.perseverance(player.position)
            i.image = i.image_class.image
    if tick == 1:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_a]:
                free_field.mask.rect = free_field.mask.rect.move(45, 0)
                free_field.update_rects_of_entities(45, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(-45, 0)
                    free_field.update_rects_of_entities(-45, 0)
            if keys[pygame.K_d]:
                free_field.mask.rect = free_field.mask.rect.move(-45, 0)
                free_field.update_rects_of_entities(-45, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(45, 0)
                    free_field.update_rects_of_entities(45, 0)
            if keys[pygame.K_w]:
                free_field.mask.rect = free_field.mask.rect.move(0, 45)
                free_field.update_rects_of_entities(0, 45)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, -45)
                    free_field.update_rects_of_entities(0, -45)
            if keys[pygame.K_s]:
                free_field.mask.rect = free_field.mask.rect.move(0, -45)
                free_field.update_rects_of_entities(0, -45)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, 45)
                    free_field.update_rects_of_entities(0, 45)

        elif keys[pygame.K_LCTRL]:
            if keys[pygame.K_a]:
                free_field.mask.rect = free_field.mask.rect.move(6, 0)
                free_field.update_rects_of_entities(6, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(-6, 0)
                    free_field.update_rects_of_entities(-6, 0)
            if keys[pygame.K_d]:
                free_field.mask.rect = free_field.mask.rect.move(-6, 0)
                free_field.update_rects_of_entities(-6, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(6, 0)
                    free_field.update_rects_of_entities(6, 0)
            if keys[pygame.K_w]:
                free_field.mask.rect = free_field.mask.rect.move(0, 6)
                free_field.update_rects_of_entities(0, 6)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, -6)
                    free_field.update_rects_of_entities(0, -6)
            if keys[pygame.K_s]:
                free_field.mask.rect = free_field.mask.rect.move(0, -6)
                free_field.update_rects_of_entities(0, -6)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, 6)
                    free_field.update_rects_of_entities(0, 6)
        else:
            if keys[pygame.K_a]:
                free_field.mask.rect = free_field.mask.rect.move(20, 0)
                free_field.update_rects_of_entities(20, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(-20, 0)
                    free_field.update_rects_of_entities(-20, 0)
            if keys[pygame.K_d]:
                free_field.mask.rect = free_field.mask.rect.move(-20, 0)
                free_field.update_rects_of_entities(-20, 0)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(20, 0)
                    free_field.update_rects_of_entities(20, 0)
            if keys[pygame.K_w]:
                free_field.mask.rect = free_field.mask.rect.move(0, 20)
                free_field.update_rects_of_entities(0, 20)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, -20)
                    free_field.update_rects_of_entities(0, -20)
            if keys[pygame.K_s]:
                free_field.mask.rect = free_field.mask.rect.move(0, -20)
                free_field.update_rects_of_entities(0, -20)
                if pygame.sprite.collide_mask(player, free_field.mask):
                    free_field.mask.rect = free_field.mask.rect.move(0, 20)
                    free_field.update_rects_of_entities(0, 20)

        animation.all_sprites.update()

    free_field.render(0)
    free_field.render(1)
    pygame.display.flip()

    tick += 1
    '''for i in animation.all_sprites:
        print()
        print(i)

    print()
    print()'''

    clock.tick(30)

pygame.quit()
