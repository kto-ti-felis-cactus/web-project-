import pygame
import math
import random
import os

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
        print('Cannot load image:', name, 'message:', message)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def set_screen(color, n):
    pass


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
                f = -40  # random.randint(-23120, -40)
                d = -40  # random.randint(-23120, -40)

                self.mask.rect = self.mask.rect.move(f, d)
                if not pygame.sprite.collide_mask(entity, self.mask):
                    break
                else:
                    self.mask.rect = self.mask.rect.move(-f, -d)
        elif mode == 1:
            while True:
                f = 0 + self.mask.rect.x + 20  # random.randint(0 + free_field.mask.rect.x, 23170 - size_of_entity[0] + free_field.mask.rect.x)  # random.randint(free_field.mask.rect.x - 1, free_field.mask.rect.x + 1)  # random.randint(0, 23170)
                d = 0 + self.mask.rect.y + 20  # random.randint(0 + free_field.mask.rect.y, 23170 - size_of_entity[1] + free_field.mask.rect.y)  # random.randint(free_field.mask.rect.y - 1, free_field.mask.rect.y + 1)  # random.randint(0, 23170)

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
                #print(i)
                screen.blit(icon_image, (((form_size[0] - (100 * 9)) / 2) + (100 * i), (form_size[1] - 10) - 100))

            for i in eval(player.player_data['inventory']):
                if i == 0:
                    pass
                else:
                    screen.blit(pygame.transform.scale(load_image(f'{i}.png'), (100, 100)),
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

ab = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x002\x00\x00\x002\x08\x06\x00\x00\x00\x1e?\x88\xb1\x00\x00\x00\tpHYs\x00\x00.#\x00\x00.#\x01x\xa5?v\x00\x00\x06\x9ciTXtXML:com.adobe.xmp\x00\x00\x00\x00\x00<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?> <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.6-c145 79.163499, 2018/08/13-16:40:22        "> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#" xmp:CreatorTool="Adobe Photoshop CC 2019 (Windows)" xmp:CreateDate="2024-04-19T22:12:37+02:00" xmp:MetadataDate="2024-04-20T23:57:08+02:00" xmp:ModifyDate="2024-04-20T23:57:08+02:00" photoshop:ColorMode="3" photoshop:ICCProfile="Samsung - Natural Color Pro 1.0 ICM" dc:format="image/png" xmpMM:InstanceID="xmp.iid:18ea97fd-3eb5-cd4e-94a2-8f27db9bf951" xmpMM:DocumentID="xmp.did:a79f2aae-4de0-dc4e-9d7a-47a13d2b2193" xmpMM:OriginalDocumentID="xmp.did:a79f2aae-4de0-dc4e-9d7a-47a13d2b2193"> <photoshop:DocumentAncestors> <rdf:Bag> <rdf:li>adobe:docid:photoshop:796f6a58-6e1f-fa41-90fc-3ff0d1f076f2</rdf:li> </rdf:Bag> </photoshop:DocumentAncestors> <xmpMM:History> <rdf:Seq> <rdf:li stEvt:action="created" stEvt:instanceID="xmp.iid:a79f2aae-4de0-dc4e-9d7a-47a13d2b2193" stEvt:when="2024-04-19T22:12:37+02:00" stEvt:softwareAgent="Adobe Photoshop CC 2019 (Windows)"/> <rdf:li stEvt:action="saved" stEvt:instanceID="xmp.iid:18ea97fd-3eb5-cd4e-94a2-8f27db9bf951" stEvt:when="2024-04-20T23:57:08+02:00" stEvt:softwareAgent="Adobe Photoshop CC 2019 (Windows)" stEvt:changed="/"/> </rdf:Seq> </xmpMM:History> </rdf:Description> </rdf:RDF> </x:xmpmeta> <?xpacket end="r"?>o\xbeR\xb3\x00\x00\x01\xaeIDATh\xde\xed\xd8\xb1N\xc30\x10\x00\xd0\x1cb\x04\tT)\x03\xbfR>\x81\x81\x85\x91\x9f\xc8\x87\xe4G\xba0\xf0\t\xf0+\x0c\x11\x08$\x18\x11\xaeO\x8d\x9b\x8b\x1b\x1b5wN\x9c\xea,\xb5\xaaS\xc7\xbe\xd7\xb3\x9d&`\x8c)N\xa1\x80B\x14\xa2\x10\x85(\xe4\xa4!\x00P\xb8\xb1.o\xcfB\x83\xc2\xf7\xcb_\x9e\x90G\x007\x00<\xadw\x9f\xcfo\x0e\xc7\xfc}\x83e@,b\x10@\x11\xf8\x96%\x04\xa7\xd0\xfd\xeb\xae\xff\xe7\x87 `\x8fX\x1cd\x08\x80\xe5\xc7\xb6\x1d\x1bOjHa!\xfb\xa9E\xc7\xf5\xdbr\x10I!ng\xc2\x8c\xd0\xf5\xe1gc\xecTJ\x0eq\x00?p\x7f\xa1S\x90\x04F\x0c\xe2\x03h\xc0~V$\xb7]Q\x08"BA\xba\xc5n!\x18\xb1\x89d\x87\x85aC|\x04\x992\x180\xdcm\nC \xae\x18\xc9\xab\xba\x18\x84\xd6m0\x80\xbb\x15\xe2\xae,\xe2\xba=\xfe\xd9\x8e\xf7\xbe\x86`_sCzS\xe5k\xd3\xfd\xda+\xfc\xde\x05i_\x1f\xe4\xbc\x8b~\x86\xf2\x80\xb4\xd7\x81\x83\x8e\xca\xb2\xec\xd5\x9b\xa6I\xb6Ne:\xe9\xfe\x18\xf6\x10UU\xf5\x8e\xd5u\x1dB\xb1\xe3\xe0w0\x80\x08e\x84\xc2\x10%\x89\xe1\x9d\x1cA\xfc\x07C\x94$f\xfc\x89G"BSO\n3\x1b$\x82\x99\x0e"\x81\x90\xc6(d\xf1\x10ID\x0cc\xe3\x02\x85(d\xa1\x90\xd0\xfd\x04\x1b3\xf5bO\x02a\xc75\xf7\xf6;7$eV\xa0]#\n\xc9\x013\n!\x01\x91\xc4t\x1dN\t\x11\xc6\xb0\x10R\xb7\xba\\\x0c\x1b!\xf9\xf0\x81V\xcd\xb1\x00.B\x0c2\x80\t\xa1\x86\x1b\xe5\xf28(\x87\xa2\x10\x85($^\xb6u\xb3\xcd\xacw\xcc[\xe0\x00\x00\x00\x00IEND\xaeB`\x82'

with open('1.png', 'wb') as a:
    a.write(ab)

ab = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x002\x00\x00\x002\x08\x06\x00\x00\x00\x1e?\x88\xb1\x00\x00\x00\tpHYs\x00\x00.#\x00\x00.#\x01x\xa5?v\x00\x00\x06\x9ciTXtXML:com.adobe.xmp\x00\x00\x00\x00\x00<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?> <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.6-c145 79.163499, 2018/08/13-16:40:22        "> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#" xmp:CreatorTool="Adobe Photoshop CC 2019 (Windows)" xmp:CreateDate="2024-04-20T00:09:10+02:00" xmp:MetadataDate="2024-04-20T23:56:58+02:00" xmp:ModifyDate="2024-04-20T23:56:58+02:00" photoshop:ColorMode="3" photoshop:ICCProfile="Samsung - Natural Color Pro 1.0 ICM" dc:format="image/png" xmpMM:InstanceID="xmp.iid:078e8ffe-7d00-544f-b200-963efa8a86e8" xmpMM:DocumentID="xmp.did:23b9980c-9876-3049-b1b0-5cb23d37c2c4" xmpMM:OriginalDocumentID="xmp.did:23b9980c-9876-3049-b1b0-5cb23d37c2c4"> <photoshop:DocumentAncestors> <rdf:Bag> <rdf:li>adobe:docid:photoshop:796f6a58-6e1f-fa41-90fc-3ff0d1f076f2</rdf:li> </rdf:Bag> </photoshop:DocumentAncestors> <xmpMM:History> <rdf:Seq> <rdf:li stEvt:action="created" stEvt:instanceID="xmp.iid:23b9980c-9876-3049-b1b0-5cb23d37c2c4" stEvt:when="2024-04-20T00:09:10+02:00" stEvt:softwareAgent="Adobe Photoshop CC 2019 (Windows)"/> <rdf:li stEvt:action="saved" stEvt:instanceID="xmp.iid:078e8ffe-7d00-544f-b200-963efa8a86e8" stEvt:when="2024-04-20T23:56:58+02:00" stEvt:softwareAgent="Adobe Photoshop CC 2019 (Windows)" stEvt:changed="/"/> </rdf:Seq> </xmpMM:History> </rdf:Description> </rdf:RDF> </x:xmpmeta> <?xpacket end="r"?>\x86\xa5\x0b\xe2\x00\x00\x02QIDATh\xde\xed\xd9\xbfJ\x031\x18\x00\xf0D\xa4Vi7[\xb8\x0e\x0e\x1d\x1c\xac\xd4Q\'\x07\xf1\r\x1c\x04\x11|\x04\xf1I\xc4G\x10Dp\xf0\r\xc4\xc1\xc9\x8e\x15+\xe8 \xe8\xa0`\x1d\n\x8a\xd6\xfa\'\xe6K/5\xd7\xe6\xfe\xb4\x17\xc8\xd7zY\xda\xa65\xf9~\xe4\xfbr\xf1\x8e2\xc6\xc8(4\x9a@\x12H\x02I \xff\x0b\x92\xcf\xe7Y\xde\x19\x1fx\xfe\xcb\xea\x83}\x08 \xba\xfb\xea\xf5:\xc9\xe5r\xa4\x0f\x9c\x11\x8cq\x88\x8a\xf1\xfd;/\x12\x05D\xbee\xfd`\xe0\xbbR\xd91\x8a1\x05\x89\x8c\xd1 \xecC\xba@\xa1\x03\x85\xd4O,\x8c\xb1\xed\x170\xadV\xabg\xb0T*\x15\x98j\n\n\x0fD\xb7*\x1c\xe7\x01\x85\x14\xff\xc0\x18\xa3\x17D\xbf],\n(.\xc6\x08d~\xa1\x10k\x90\xa7\xc7/\x11\x0b\xc7\xb0A1\xc6 \xe9\xc9\xb1\xce\xe7\xe6\xfb\x0f\x81\xcf\xebk\xdb\x9e\xdf\x1d\x1d\xefu\xbeS\x7f\xcb!TY\x15\x11\x10\x87P\x14\x90\xad\xcd\x1d\x11\xf8\xca\xf2\x86\xe8;=;\x14\xb0\xfd\x83\xdd0\x88\xc0\xd8\x82\x88\xc9e\x80QW\xc4}O\xe1U\xa6\x92\x1c\xcb\x1a\x04\x82\xe3\x01\xf55\x18 $H\xad\tXa+\x90n\x8c\x9a:\xba&WB\x87\xb0\x0e\xd1\xa5X\x10\x04\xe6v\x8bZ[sV!~\x85\xef\xa6Q\x0f\xc4o\x8b\xc5\x02\xe9\xac\x8a\xd8\x91\x9e\x1e\xdd\x8b\xa5#S\xaf\xa7\xc0G\x16\xb2P*\xb0jm\x04R\x0b\x05\xa4\x98\xcd\xb2L\xc0\x01\x11\xdak\xfb\xdcEo_^\xf4\x90Y\x0e\xb9\xb1\x0c\x99[]b\xe9\x89t\xf0\xae\xf5\xd1$\xcdJm\xb8 \x10\xb4H\xad\xae\xbe@\xc8\x0c\x87\xdc\xdb\x87\xb4\x8b\x9d\x07\x0e\x01?\xd7*\xa2\x7f\xba\xb4Hd\x9f\xbc\x86\\\x9d\x9c\x8f8\xa4\xc0!\x0fC\x92Z0\xf7PA\xfc\x8a\x1d=$\xca\xf6\xfb\xf1\xfd-\xe6\xben4\xf0B\xa2^\x10?\xef\xdepC\xf8\x8a\x90\xa9b\xb6sDy\xbdh\x1fQ2\xe5\xbf#\n \xa0O\x07\x01\x04\xbcbX\x11\xcfYK\x07Q\xcfZ\x94\xb6\xe3-;\x8e\x1a\x08\xe5\x102\x14\xa9%\xcfZ\n\xc43\x0e:H\xd0?V\xea\xa1\x91\xa7\x14\x1e\xc8\x00\xf7\xb7p<\xe8\xf1[\x89~\xee\xa2\x10\x0c\xcfGL\xdd\xd7"X\x1e+\xc4\xbd\xd3\x88\n\x1273P@0\xb4\x04\x92@\x12Hp\xfb\x05\xa6\xd0\x8d\xbb\x84Q\xceE\x00\x00\x00\x00IEND\xaeB`\x82'

with open('2.png', 'wb') as a:
    a.write(ab)

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
            '''free_field.mask.rect = free_field.mask.rect.move(-(past_form_size[0] - player.position[0]),
                                                             -(past_form_size[1] - player.position[1]))'''
            #free_field.mask.mask = pygame.mask.from_surface(free_field.board)
            free_field.mask.rect = free_field.mask.rect.move(-(past_form_size[0] - player.position[0]),
                                                             -(past_form_size[1] - player.position[1]))
            #free_field.mask.rect = free_field.board.get_rect()
            free_field.update_rects_of_entities_and_portals(-(past_form_size[0] - player.position[0]),
                                                            -(past_form_size[1] - player.position[1]))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if free_field.get_cell(pygame.mouse.get_pos()) != None:
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
        print(screen_color)
    else:
        del s

    pygame.display.flip()
    '''
    print([(i.rect.x, i.rect.y) for i in portals])'''

    tick += 1

    clock.tick(30)

os.remove('1.png')
os.remove('2.png')

pygame.quit()
