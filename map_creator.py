from PIL import Image, ImageDraw
from random import randint


def start_process_create_map(mode):
    if mode == 0:
        imf = Image.open('data/wall.png')
        img = Image.new('RGBA', (1680, 300))
        idraw = ImageDraw.Draw(img)

        a = 1680 // 50


        for i in range(1680 // 50 + 1):
            img.paste(imf, (50 * i, 0))

        for i in range(1680 // 50 + 1):
            img.paste(imf, (50 * i, 250))

        img.save('data/board.png')



        '''img1 = Image.new('RGBA', (200, 50))
        idraw1 = ImageDraw.Draw(img1)
        
        idraw1.rectangle((0, 0, 200, 50), 'gray')
        
        img1.save('data/wall.png')
        
        npc_human_corpse_1.png
        
        '''
    elif mode == 1:
        def gen_mat():
            matheight = 80
            mat = []
            for i in range(matheight):
                mat.append(['-'] * matheight)
            return mat

        def gen_room(levelmat, count):
            for c in range(count):
                roomheight = randint(8, 10)
                x = randint(3, len(levelmat[0]) - roomheight - 3)
                y = randint(2, len(levelmat) - roomheight - 4)
                ytmp = y
                for i in range(roomheight):
                    xtmp = x
                    ytmp += 1
                    for o in range(roomheight):
                        if levelmat[ytmp][xtmp] == '-':
                            levelmat[ytmp][xtmp] = '1'
                        elif levelmat[ytmp][xtmp] == '1':
                            levelmat[ytmp][xtmp] = '-'
                        xtmp += 1
            return levelmat

        def edit_map(mat):
            for i in range(len(mat)):
                for ii in range(len(mat[i])):
                    if (mat[i][ii] == '1' and mat[i][ii - 1] == '-' and mat[i][ii + 1] == '-' and mat[i + 1][ii] == '-'
                            and mat[i - 1][ii] == '-'):
                        try:
                            mat[i][ii - 1] = '1'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii] = '1'
                        except IndexError:
                            pass
                    if mat[i][ii] == '1' and mat[i - 1][ii - 1] == '1' and mat[i - 1][ii] == '-':
                        try:
                            mat[i - 1][ii - 1] = '1'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii] = '1'
                        except IndexError:
                            pass
                        try:
                            mat[i - 1][ii] = '1'
                        except IndexError:
                            pass
                    if mat[i][ii] == '1' and mat[i - 1][ii + 1] == '1' and mat[i - 1][ii] == '-':
                        try:
                            mat[i - 1][ii + 1] = '1'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii] = '1'
                        except IndexError:
                            pass
                        try:
                            mat[i - 1][ii] = '1'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i - 1][ii] == '1' and mat[i][ii - 1] == '-' and mat[i - 1][ii - 1] == '-'
                            and mat[i][ii + 1] == '-' and mat[i - 1][ii + 1] == '-' and mat[i - 2][ii - 1] == '-'
                            and mat[i - 2][ii] == '-' and mat[i - 2][ii + 1] == '-' and mat[i + 1][ii - 1] == '-'
                            and mat[i + 1][ii] == '-' and mat[i + 1][ii + 1] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 1][ii] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i - 1][ii] == '-' and mat[i][ii - 1] == '-' and mat[i - 1][ii - 1] == '-'
                            and mat[i][ii + 1] == '-' and mat[i - 1][ii + 1] == '-' and mat[i + 1][ii - 1] == '-'
                            and mat[i + 1][ii] == '-' and mat[i + 1][ii + 1] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i - 1][ii] == '1' and mat[i - 2][ii] == '1' and mat[i - 3][ii] == '-'
                            and mat[i][ii - 1] == '-' and mat[i - 1][ii - 1] == '-' and mat[i][ii + 1] == '-'
                            and mat[i - 1][ii + 1] == '-' and mat[i - 2][ii - 1] == '-' and mat[i - 2][ii + 1] == '-'
                            and mat[i + 1][ii - 1] == '-' and mat[i + 1][ii] == '-' and mat[i + 1][ii + 1] == '-'
                            and mat[i - 3][ii - 1] == '-' and mat[i - 3][ii + 1] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 1][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 2][ii] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i - 1][ii] == '1' and mat[i - 2][ii] == '1' and mat[i - 3][ii] == '1'
                            and mat[i][ii - 1] == '-' and mat[i - 1][ii - 1] == '-' and mat[i][ii + 1] == '-'
                            and mat[i - 1][ii + 1] == '-' and mat[i - 2][ii - 1] == '-' and mat[i - 2][ii + 1] == '-'
                            and mat[i + 1][ii - 1] == '-' and mat[i + 1][ii] == '-' and mat[i + 1][ii + 1] == '-'
                            and mat[i - 3][ii - 1] == '-' and mat[i - 3][ii + 1] == '-' and mat[i - 4][ii - 1] == '-'
                            and mat[i - 4][ii] == '-' and mat[i - 4][ii + 1] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 1][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 2][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 3][ii] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i - 1][ii] == '1' and mat[i - 2][ii] == '1' and mat[i - 3][ii] == '1'
                            and mat[i - 4][ii] == '1' and mat[i][ii - 1] == '-' and mat[i][ii + 1] == '-'
                            and mat[i - 1][ii - 1] == '-' and mat[i - 1][ii + 1] == '-' and mat[i - 2][ii - 1] == '-'
                            and mat[i - 2][ii + 1] == '-' and mat[i + 1][ii - 1] == '-' and mat[i + 1][ii] == '-'
                            and mat[i + 1][ii + 1] == '-' and mat[i - 3][ii - 1] == '-' and mat[i - 3][ii + 1] == '-'
                            and mat[i - 4][ii - 1] == '-' and mat[i - 4][ii + 1] == '-' and mat[i - 5][ii - 1] == '-'
                            and mat[i - 5][ii] == '-' and mat[i - 5][ii + 1] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 1][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 2][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 3][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i - 4][ii] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i][ii + 1] == '1' and mat[i][ii - 1] == '-' and mat[i - 1][ii] == '-'
                            and mat[i - 1][ii - 1] == '-' and mat[i - 1][ii + 1] == '-' and mat[i + 1][ii - 1] == '-'
                            and mat[i + 1][ii] == '-' and mat[i + 1][ii + 1] == '-' and mat[i - 1][ii + 2] == '-'
                            and mat[i][ii + 2] == '-' and mat[i + 1][ii + 2] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 1] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i][ii + 1] == '1' and mat[i][ii + 2] == '1' and mat[i][ii - 1] == '-'
                            and mat[i - 1][ii] == '-' and mat[i - 1][ii - 1] == '-' and mat[i - 1][ii + 1] == '-'
                            and mat[i + 1][ii - 1] == '-' and mat[i + 1][ii] == '-' and mat[i + 1][ii + 1] == '-'
                            and mat[i - 1][ii + 2] == '-' and mat[i + 1][ii + 2] == '-' and mat[i][ii + 3] == '-'
                            and mat[i - 1][ii + 3] == '-' and mat[i + 1][ii + 3] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 1] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 2] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i][ii + 1] == '1' and mat[i][ii + 2] == '1' and mat[i][ii + 3] == '1'
                            and mat[i][ii - 1] == '-' and mat[i - 1][ii] == '-' and mat[i - 1][ii - 1] == '-'
                            and mat[i - 1][ii + 1] == '-' and mat[i + 1][ii - 1] == '-' and mat[i + 1][ii] == '-'
                            and mat[i + 1][ii + 1] == '-' and mat[i - 1][ii + 2] == '-' and mat[i + 1][ii + 2] == '-'
                            and mat[i - 1][ii + 3] == '-' and mat[i + 1][ii + 3] == '-' and mat[i - 1][ii + 4] == '-'
                            and mat[i][ii + 4] == '-' and mat[i + 1][ii + 4] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 1] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 2] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 3] = '-'
                        except IndexError:
                            pass
                    if (mat[i][ii] == '1' and mat[i][ii + 1] == '1' and mat[i][ii + 2] == '1' and mat[i][ii + 3] == '1'
                            and mat[i][ii + 4] == '1' and mat[i][ii - 1] == '-' and mat[i - 1][ii] == '-' and mat[i - 1][ii - 1] == '-'
                            and mat[i - 1][ii + 1] == '-' and mat[i + 1][ii - 1] == '-' and mat[i + 1][ii] == '-'
                            and mat[i + 1][ii + 1] == '-' and mat[i - 1][ii + 2] == '-' and mat[i + 1][ii + 2] == '-'
                            and mat[i - 1][ii + 3] == '-' and mat[i + 1][ii + 3] == '-' and mat[i - 1][ii + 4] == '-'
                            and mat[i + 1][ii + 4] == '-' and mat[i - 1][ii + 5] == '-' and mat[i][ii + 5] == '-'
                            and mat[i + 1][ii + 5] == '-'):
                        try:
                            mat[i][ii] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 1] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 2] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 3] = '-'
                        except IndexError:
                            pass
                        try:
                            mat[i][ii + 4] = '-'
                        except IndexError:
                            pass

            counter = 0
            for i in range(len(mat[0])):
                if counter == 0:
                    mat[0][i] = '1'
                    mat[1][i] = '1'
                    mat[2][i] = '1'

                    mat[-1][i] = '1'
                    mat[-2][i] = '1'
                    mat[-3][i] = '1'
                    counter = 1
                else:
                    mat[0][i] = '-'
                    mat[1][i] = '1'
                    mat[2][i] = '-'

                    mat[-1][i] = '-'
                    mat[-2][i] = '1'
                    mat[-3][i] = '-'
                    counter = 0
            for i in range(len(mat)):
                if counter == 0:
                    mat[i][0] = '1'
                    mat[i][1] = '1'
                    mat[i][2] = '1'

                    mat[i][-1] = '1'
                    mat[i][-2] = '1'
                    mat[i][-3] = '1'
                    counter = 1
                else:
                    mat[i][0] = '-'
                    mat[i][1] = '1'
                    mat[i][2] = '-'

                    mat[i][-1] = '-'
                    mat[i][-2] = '1'
                    mat[i][-3] = '-'

                    counter = 0

            mat[0][0] = '1'
            mat[0][1] = '1'
            mat[0][2] = '1'
            mat[0][3] = '-'

            mat[1][0] = '1'
            mat[1][1] = '-'
            mat[1][2] = '1'
            mat[1][3] = '1'

            mat[2][0] = '1'
            mat[2][1] = '1'
            mat[2][2] = '1'
            mat[2][3] = '1'

            mat[3][0] = '-'
            mat[3][1] = '1'
            mat[3][2] = '1'

            mat[-1][0] = '1'
            mat[-1][1] = '1'
            mat[-1][2] = '1'
            mat[-1][3] = '-'

            mat[-2][0] = '1'
            mat[-2][1] = '-'
            mat[-2][2] = '1'
            mat[-2][3] = '1'

            mat[-3][0] = '1'
            mat[-3][1] = '1'
            mat[-3][2] = '1'
            mat[-3][3] = '1'

            mat[-4][0] = '-'
            mat[-4][1] = '1'
            mat[-4][2] = '1'

            mat[0][-1] = '1'
            mat[0][-2] = '1'
            mat[0][-3] = '1'
            mat[0][-4] = '-'

            mat[1][-1] = '1'
            mat[1][-2] = '-'
            mat[1][-3] = '1'
            mat[1][-4] = '1'

            mat[2][-1] = '1'
            mat[2][-2] = '1'
            mat[2][-3] = '1'
            mat[2][-4] = '1'

            mat[3][-1] = '-'
            mat[3][-2] = '1'
            mat[3][-3] = '1'

            mat[-1][-1] = '1'
            mat[-1][-2] = '1'
            mat[-1][-3] = '1'
            mat[-1][-4] = '-'

            mat[-2][-1] = '1'
            mat[-2][-2] = '-'
            mat[-2][-3] = '1'
            mat[-2][-4] = '1'

            mat[-3][-1] = '1'
            mat[-3][-2] = '1'
            mat[-3][-3] = '1'
            mat[-3][-4] = '1'

            mat[-4][-1] = '-'
            mat[-4][-2] = '1'
            mat[-4][-3] = '1'
            '''for i in range(len(mat)):
                mat[i] = ' '.join(mat[i])
    
            print('\n'.join(mat))
            for i in range(len(rmat)):
                mat[i] = mat[i].split(' ')'''
            return mat

        def save_level(levelmat, levelname):
            '''with open(f'{levelname}.txt', 'w', encoding='utf-8') as level:
                for i in range(len(levelmat)):
                    levelline = ''
                    for o in levelmat[i]:
                        levelline += (o + ',')
                    levelline = levelline[0:len(levelline) - 1] + '\n'
                    level.write(levelline)
            with open(f'{levelname}.txt', 'r', encoding='utf-8') as level:
                data = level.read().split('\n')
                data = '\n'.join(data[:-2])
            with open(f'{levelname}.txt', 'w', encoding='utf-8') as level:
                level.write(data)'''

            imf = Image.open('data/wall.png')
            img = Image.new('RGBA', (80 * 50 * 3, 80 * 50 * 3))

            for i in range(len(levelmat)):
                for ii in range(len(levelmat[i])):
                    if levelmat[i][ii] == '-':
                        img.paste(imf, (50 * ii, 50 * i))
            img.save('data/board.png')

            imf = Image.open('data/floor.png')
            img = Image.new('RGBA', (80 * 50 * 3, 80 * 50 * 3))

            for i in range(len(levelmat)):
                for ii in range(len(levelmat[i])):
                    img.paste(imf, (50 * ii, 50 * i))
            img.save('data/full_floor.png')
            '''idraw = ImageDraw.Draw(img)

            a = 1680 // 50

            for i in range(1680 // 50 + 1):
                img.paste(imf, (50 * i, 0))

            for i in range(1680 // 50 + 1):
                img.paste(imf, (50 * i, 250))

            img.save('data/board.png')'''

        def create_room():
            mat = gen_mat()
            rmat = gen_room(mat, randint(60, 90))
            rmat = gen_room(rmat, randint(60, 90))

            rmat = edit_map(rmat)
            del mat
            for i in range(len(rmat)):
                rmat[i] = ' '.join(rmat[i])
            return rmat

        def create_level():
            rmat = create_room()
            rmat1 = create_room()
            rmat2 = create_room()
            for i in range(len(rmat)):
                rmat[i] += ' ' + rmat1[i] + ' ' + rmat2[i]
            del rmat1, rmat2

            rmat1 = create_room()
            rmat2 = create_room()

            #rmat2[40][40] = '1'




            rmat3 = create_room()
            for i in range(len(rmat)):
                rmat1[i] += ' ' + rmat2[i] + ' ' + rmat3[i]
            del rmat2, rmat3

            rmat2 = create_room()
            rmat3 = create_room()
            rmat4 = create_room()
            for i in range(len(rmat)):
                rmat2[i] += ' ' + rmat3[i] + ' ' + rmat4[i]
            del rmat3, rmat4
            print(rmat)
            print()

            rmat += rmat1
            rmat += rmat2

            print('\n'.join(rmat))

            for i in range(len(rmat)):
                rmat[i] = rmat[i].split(' ')
            save_level(rmat, '1')

        create_level()
    elif mode == 2:
        img1 = Image.new('RGBA', (50, 50))
        idraw1 = ImageDraw.Draw(img1)

        idraw1.rectangle((0, 0, 50, 50), 'gray')

        img1.save('data/wall.png')


#start_process_create_map(2)
#start_process_create_map(1)
