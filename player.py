import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, stats_path, position, image_name, all_sprites, colision_image):
        super().__init__(all_sprites)
        self.stats_path = stats_path
        self.position = position
        self.type_of_entity = '[player]'
        self.player_data = {}
        self.image_class = image_name
        self.rect = self.image_class.image.get_rect()
        self.colision_image = colision_image
        self.mask = pygame.mask.from_surface(self.colision_image)

        class HearColision(pygame.sprite.Sprite):
            def __init__(self, image):
                super().__init__()
                self.image = image
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()

        self.hear_colision = HearColision(pygame.transform.scale(self.colision_image, (1234, 1234)))
        self.health = 10
        self.score = 0
        self.update_rect_x_y()

    def update_rect_x_y(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    def read_player_stats(self):
        file = open(fr'player_stats\{self.stats_path}.txt', 'r', encoding='utf-8')
        for i in file.read().split('\n'):
            self.player_data[i.split('--')[0]] = i.split('--')[1]
        file.close()

    def write_player_stats(self):
        file = open(fr'player_stats\{self.stats_path}.txt', 'w', encoding='utf-8')
        output = ''
        for i in self.player_data.keys():
            output += f'{i}--{self.player_data[i]}\n'
        output = output.split('\n')
        output = output[:-1]
        output = '\n'.join(output)
        file.write(output)
        file.close()

    def update_score(self):
        self.player_data['score'] = float(self.player_data['score']) + self.score
        self.score = 0

    def set_image(self, image_name):
        self.image_class = image_name

