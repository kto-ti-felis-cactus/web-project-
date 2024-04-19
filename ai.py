import pygame
from random import randint


def find_danger(list_of_entities, type_of_entity, self_name):
    danger = []
    for i in list_of_entities:
        if type_of_entity == '[entity]':
            if i != 'player':
                if i.type_of_entity == '[cuscas]':
                    danger.append([i.name, (i.weapon_id * average_damage_level) + (i.to_the_human * -1)])
                if i.type_of_entity == '[human]':
                    if eval(self_name).group != i.group:
                        danger.append([i.name, (i.weapon_id * average_damage_level) + (i.to_the_noname_humans * -1)])
                    else:
                        danger.append([i.name, 0])
            else:
                danger.append(['player', 5 * (5 * average_damage_level)])
        elif type_of_entity == '[cuscas]':
            if i != 'player':
                if i.type_of_entity == '[cuscas]':
                    danger.append([i.name, 0])
                if i.type_of_entity == '[human]':
                    danger.append([i.name, (i.weapon_id * average_damage_level) + (i.to_the_cuscas * -1)])

            else:
                danger.append(['player', 5 * (5 * average_damage_level)])

    return danger


class Entity(pygame.sprite.Sprite):
    def __init__(self, is_dead, list_of_entities, name, player_pos, image_class, board, all_sprites, a):
        super().__init__(all_sprites)
        self.type_of_entity = '[entity]'
        self.is_dead = is_dead
        self.target_position = [player_pos[0], player_pos[1]]
        self.list_of_entities = list_of_entities
        self.danger = find_danger(list_of_entities, self.type_of_entity, name)
        self.name = name 
        self.target = '[NULL]'
        self.victim = '[NULL]'
        self.health = 762559748  # (3 ** 3 ** 3) // 10000
        self.image_class = image_class
        self.image = image_class.image

        self.mask = pygame.mask.from_surface(a)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

        self.angle = 0
        self.board = board

        self.past = [[], [], [], []]
        self.process = 'walk to target'
        self.where_wall = [False for i in range(4)]
        self.bypass = '[NULL]'
        self.wait = False
        self.timer = 0

        self.perseverance(player_pos)

    def perseverance(self, player_pos):
        self.danger = find_danger(self.list_of_entities, self.type_of_entity, self.name)
        if self.is_dead is False:
            self.do(player_pos)

    def update_past(self):
        self.past = [[self.rect.x, self.rect.y], [self.rect.x, self.rect.y], [self.rect.x, self.rect.y],
                     [self.rect.x, self.rect.y]]

    def update_danger(self):
        self.danger = find_danger(self.list_of_entities, self.type_of_entity, self.name)

    def find_max_danger(self):
        self.max_danger = ['player', 0]
        for i in self.danger:
            if i[1] > self.max_danger[1]:
                self.max_danger = i

    def check_wall(self):
            self.rect = self.rect.move(-8 * -1, 0)
            if pygame.sprite.collide_mask(self, self.board):
                self.where_wall[0] = True
            else:
                self.where_wall[0] = False
            self.rect = self.rect.move(8 * -1, 0)

            self.rect = self.rect.move(8 * -1, 0)
            if pygame.sprite.collide_mask(self, self.board):
                self.where_wall[1] = True
            else:
                self.where_wall[1] = False
            self.rect = self.rect.move(-8 * -1, 0)

            self.rect = self.rect.move(0, -8 * -1)
            if pygame.sprite.collide_mask(self, self.board):
                self.where_wall[2] = True
            else:
                self.where_wall[2] = False
            self.rect = self.rect.move(0, 8 * -1)

            self.rect = self.rect.move(0, 8 * -1)
            if pygame.sprite.collide_mask(self, self.board):
                self.where_wall[3] = True
            else:
                self.where_wall[3] = False
            self.rect = self.rect.move(0, -8 * -1)

    def do(self, player_pos):
        if self.timer == 10:

            while True:
                f = randint(-200, 200)
                d = randint(-200, 200)

                self.rect = self.rect.move(f, d)
                if not pygame.sprite.collide_mask(self, self.board):
                    break
                else:
                    self.rect = self.rect.move(-f, -d)
        self.find_max_danger()
        if self.max_danger[0] == 'player':
            self.target = 'kill player'
        else:
            self.target = 'go to'

        if self.target == 'kill player':
            self.victim = 'player'
            self.target_position = player_pos

        elif self.target == 'go to':
            if self.max_danger[0] != 'player':
                self.victim = self.max_danger[0]
                self.target_position = eval(self.victim).position

        if self.target in ('go to', 'kill player'):
            if self.past[0] == self.past[2] and self.past[1] == self.past[3]:
                self.process = 'bypass the obstacle'
                self.wait = True
            elif ((self.past[0] != self.past[2] and self.past[1] != self.past[3] and self.wait is False)
                    or self.wait is False):
                self.process = 'walk to target'
            if (self.past[0] == self.past[2] == self.past[1] == self.past[3] or
                    (self.past[0] == self.past[2] and self.past[1] == self.past[3]) or
                    (self.past[0] == self.past[3]) or (self.past[1] == self.past[2])):
                self.timer += 1
            else:
                self.timer = 0

            if self.process == 'bypass the obstacle':

                self.check_wall()
                if (self.where_wall[0] is True and self.where_wall[1] is False and self.where_wall[2] is False
                        and self.where_wall[3] is False):
                    self.bypass = 'up'
                    self.rect = self.rect.move(0, -8)
                elif (self.where_wall[0] is False and self.where_wall[1] is True and self.where_wall[2] is False
                        and self.where_wall[3] is False):
                    self.bypass = 'down'
                    self.rect = self.rect.move(0, 8)
                elif (self.where_wall[0] is False and self.where_wall[1] is False and self.where_wall[2] is True
                        and self.where_wall[3] is False):
                    self.bypass = 'right'
                    self.rect = self.rect.move(8, 0)
                elif (self.where_wall[0] is False and self.where_wall[1] is False and self.where_wall[2] is False
                        and self.where_wall[3] is True):
                    self.bypass = 'left'
                    self.rect = self.rect.move(-8, 0)

                if(self.where_wall[0] is False and self.where_wall[1] is False and self.where_wall[2] is False
                        and self.where_wall[3] is False):
                    self.process = 'walk to target'
                    self.wait = False

                if self.bypass == 'down' and self.where_wall[0] is False:
                    self.rect = self.rect.move(0, 8)

                elif self.bypass == 'up' and self.where_wall[0] is False:
                    self.rect = self.rect.move(0, -8)

                if self.bypass == 'up' and self.where_wall[1] is False:
                    self.rect = self.rect.move(0, -8)

                elif self.bypass == 'down' and self.where_wall[1] is False:
                    self.rect = self.rect.move(0, 8)

                if self.bypass == 'right' and self.where_wall[2] is False:
                    self.rect = self.rect.move(8, 0)

                elif self.bypass == 'left' and self.where_wall[2] is False:
                    self.rect = self.rect.move(-8, 0)

                if self.bypass == 'left' and self.where_wall[2] is False:
                    self.rect = self.rect.move(-8, 0)

                elif self.bypass == 'right' and self.where_wall[2] is False:
                    self.rect = self.rect.move(8, 0)

            elif self.process == 'walk to target':
                self.where_wall = [False for i in range(4)]
                if abs(self.target_position[0] - self.rect[0]) != 1:
                    if abs(self.target_position[0] - self.rect[0]) < 1:

                        if self.target_position[0] > self.rect[0]:
                            self.rect = self.rect.move(-8, 0)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(8, 0)

                        elif self.target_position[0] < self.rect[0]:
                            self.rect = self.rect.move(8, 0)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(-8, 0)
                    else:
                        if self.target_position[0] > self.rect[0]:
                            self.rect = self.rect.move(8, 0)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(-8, 0)

                        elif self.target_position[0] < self.rect[0]:
                            self.rect = self.rect.move(-8, 0)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(8, 0)
                else:
                    self.rect = self.rect.move(0, 0)

                if abs(self.target_position[1] - self.rect[1]) != 1:
                    if abs(self.target_position[1] - self.rect[1]) < 1:
                        if self.target_position[1] > self.rect[1]:
                            self.rect = self.rect.move(0, -8)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(0, 8)

                        elif self.target_position[1] < self.rect[1]:
                            self.rect = self.rect.move(0, 8)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(0, -8)
                    else:
                        if self.target_position[1] > self.rect[1]:
                            self.rect = self.rect.move(0, 8)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(0, -8)

                        elif self.target_position[1] < self.rect[1]:
                            self.rect = self.rect.move(0, -8)
                            if pygame.sprite.collide_mask(self, self.board):
                                self.rect = self.rect.move(0, 8)
            self.past.pop(0)
            self.past.append([self.rect[0], self.rect[1]])


    def set_image(self, image_class):
        self.image_class = image_class
        self.image = self.image_class.image

    def all_parameters(self):
        print('>->->->->-<-<-<-<-<')
        print(f'all parameters of entity <{self.name}>')
        print('------------------')
        print(f'type_of_entity: {self.type_of_entity}')
        print(f'is_dead: {self.is_dead}')
        print(f'position: {[self.rect[0], self.rect[1]]}')
        print(f'target_position: {self.target_position}')
        print(f'list_of_entities: {self.list_of_entities}')
        print(f'danger: {self.danger}')
        print(f'max_danger: {self.max_danger}')
        print(f'name: {self.name}')
        print(f'target: {self.target}')
        print(f'victim: {self.victim}')
        print(f'health: {self.health}')
        print(f'image_class: {self.image_class}')
        print(f'image: {self.image}')
        print(f'angle: {self.angle}')
        print('>->->->->-<-<-<-<-<')


class PastPos:
    def __init__(self):
        pass


class NextPos:
    def __init__(self):
        pass


class Cuscas(Entity):
    def __init__(self, to_the_player, is_dead, weapon_id, group, position, list_of_entities, name, player_pos,
                 image_class, board):
        super().__init__(to_the_player, is_dead, weapon_id, group, position, list_of_entities, name, player_pos,
                         image_class, board)
        self.to_the_player = to_the_player
        self.type_of_entity = '[cuscas]'
        self.is_dead = is_dead
        self.weapon_id = weapon_id
        self.group = group
        self.position = position[0], position[1]
        self.enemy_position = ['[NULL]', '[NULL]']
        self.list_of_entities = list_of_entities
        self.danger = find_danger(list_of_entities, self.type_of_entity, name)
        self.name = name
        self.target = '[NULL]'
        self.enemy = '[NULL]'
        self.to_the_human = -5
        self.health = 5
        self.image_class = image_class
        self.image = image_class.image
        self.angle = 0
        self.board = board
        self.perseverance(player_pos)

    def perseverance(self, player_pos):
        self.update_danger()
        if self.to_the_player > 0 and self.to_the_player > 4:
            self.target = 'best to player'

        if self.to_the_player > 0 and self.to_the_player < 4:
            self.target = 'good to player'

        if self.to_the_player == 0:
            self.target = 'neutral to player'

        if self.to_the_player < 0 and self.to_the_player > -4:
            self.target = 'bad to player'

        if self.to_the_player < 0 and self.to_the_player <= -4:
            self.target = 'worst to player'

        self.check_health()

        if self.is_dead is False:
            self.do(player_pos)

    def check_health(self):
        if self.health <= 0:
            self.kill()

    def update_danger(self):
        self.danger = find_danger(self.list_of_entities, self.type_of_entity, self.name)

    def find_max_danger(self):
        self.max_danger = ['player', 0]
        for i in self.danger:
            if i[1] > self.max_danger[1]:
                self.max_danger = i

    def do(self, player_pos):
        self.find_max_danger()
        if self.max_danger[0] == 'player':
            if self.target == 'worst to player':
                self.target = 'kill player'
        else:
            self.target = 'destroy danger'

        if self.target == 'kill player':
            self.enemy = 'player'
            self.enemy_position = player_pos

        elif self.target == 'destroy danger':
            if self.max_danger[0] != 'player':
                self.enemy = self.max_danger[0]
                self.enemy_position = eval(self.enemy).position

        if self.target == ('destroy danger' or 'kill player'):
            # x - 11, y - 4

            if abs(self.enemy_position[0] - self.position[0]) != 1:
                if abs(self.enemy_position[0] - self.position[0]) < 1:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]
                else:
                    if self.enemy_position[0] > self.position[0]:
                        if [self.position[0] + 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] + 1, self.position[1]]

                    elif self.enemy_position[0] < self.position[0]:
                        if [self.position[0] - 1 - 11, self.position[1] - 4] not in self.board:
                            self.position = [self.position[0] - 1, self.position[1]]
            else:
                self.position = [self.position[0], self.position[1]]

            if abs(self.enemy_position[1] - self.position[1]) != 1:
                if abs(self.enemy_position[1] - self.position[1]) < 1:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]
                else:
                    if self.enemy_position[1] > self.position[1]:
                        if [self.position[0] - 11, self.position[1] + 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] + 1]

                    elif self.enemy_position[1] < self.position[1]:
                        if [self.position[0] - 11, self.position[1] - 1 - 4] not in self.board:
                            self.position = [self.position[0], self.position[1] - 1]
            else:
                self.position = [self.position[0], self.position[1]]

    def kill(self):
        self.is_dead = True

    def set_image(self, image_class):
        self.image_class = image_class
        self.image = self.image_class.image

    def all_parameters(self):
        print('>->->->->-<-<-<-<-<')
        print(f'all parameters of entity <{self.name}>')
        print('------------------')
        print(f'to_the_player: {self.to_the_player}')
        print(f'type_of_entity: {self.type_of_entity}')
        print(f'is_dead: {self.is_dead}')
        print(f'weapon_id: {self.weapon_id}')
        print(f'group: {self.group}')
        print(f'position: {self.position}')
        print(f'list_of_entities: {self.list_of_entities}')
        print(f'danger: {self.danger}')
        print(f'max_danger: {self.max_danger}')
        print(f'name: {self.name}')
        print(f'target: {self.target}')
        print(f'to_the_cuscas: {self.to_the_human}')
        print('>->->->->-<-<-<-<-<')


average_damage_level = 1
