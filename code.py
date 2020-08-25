import requests
import json
import design
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def herostats_fill():  # update
    od = requests.get("https://api.opendota.com/api/heroStats")
    count_heroes = len(od.json())
    d = list(od.json()[0].keys())
    with open("heroes_stats.json", "w") as out:
        flag = 0
        for i in d:
            if flag == 0:
                flag = 1
            else:
                out.write(';')
            out.write(i)
        out.write('\n')
        for i in range(count_heroes):
            flag = 0
            for j in d:
                if flag == 0:
                    flag = 1
                else:
                    out.write(';')
                out.write(str(od.json()[i][j]))
            out.write('\n')


def winrates_fill(d):  # update
    with open("winrates.json", "w") as out:
        with open("heroes_stats.json", "r") as f:
            out.write('id;name;roles;winrate_Herald;winrate_Guardian;winrate_Crusader;winrate_Archon;'
                      'winrate_Legend;winrate_Ancient;winrate_Divine;winrate_Immortal;winrate_pro' + '\n')
            s = f.readlines()
            n = len(s)
            i = 1
            while i < n:
                substr = s[i].split(';')
                wr_1 = str(int(substr[d['1_win']]) / int(substr[d['1_pick']])) + ';'
                wr_2 = str(int(substr[d['2_win']]) / int(substr[d['2_pick']])) + ';'
                wr_3 = str(int(substr[d['3_win']]) / int(substr[d['3_pick']])) + ';'
                wr_4 = str(int(substr[d['4_win']]) / int(substr[d['4_pick']])) + ';'
                wr_5 = str(int(substr[d['5_win']]) / int(substr[d['5_pick']])) + ';'
                wr_6 = str(int(substr[d['6_win']]) / int(substr[d['6_pick']])) + ';'
                wr_7 = str(int(substr[d['7_win']]) / int(substr[d['7_pick']])) + ';'
                wr_8 = str(int(substr[d['8_win']]) / int(substr[d['8_pick']])) + ';'
                wr_pro = str(int(substr[d['pro_win']]) / int(substr[d['pro_pick']]))
                out.write(substr[d['id']] + ';' + substr[d['localized_name']] + ';' + substr[d['roles']]
                          + ';' + wr_1 + wr_2 + wr_3 + wr_4 + wr_5 + wr_6 + wr_7 + wr_8 + wr_pro + '\n')
                i += 1


def roles_fill():
    with open('winrates.json', 'r') as f:
        s = f.readlines()
        count_heroes = len(s)
        for i in range(count_heroes):
            s[i] = s[i].split(';')
        for i in range(count_heroes):
            s[i][2] = s[i][2].split(',')
            count_roles = len(s[i][2])
            for j in range(count_roles):
                s[i][2][j] = s[i][2][j].replace('[', '')
                s[i][2][j] = s[i][2][j].replace(']', '')
                s[i][2][j] = s[i][2][j].replace("'", '')
                s[i][2][j] = s[i][2][j].replace(' ', '')
        roles = set()
        for i in range(1, count_heroes - 1):
            for j in s[i][2]:
                if j not in roles:
                    roles.add(j)
        with open('roles.json', 'w') as out:
            for i in range(count_heroes):
                for j in range(3):
                    if j != 0:
                        out.write(';')
                    if j != 2:
                        out.write(s[i][j])
                    else:
                        count_roles = len(s[i][j])
                        for k in range(count_roles):
                            if k != 0:
                                out.write(',')
                            out.write(s[i][j][k])
                out.write('\n')


def fill_table(rank, req_roles):
    with open('winrates.json', 'r') as f:
        s = f.readlines()
        count_heroes = len(s)
        for i in range(count_heroes):
            s[i] = s[i].split(';')
            s[i][11] = s[i][11].replace('\n', '')
        for i in range(count_heroes):
            s[i][2] = s[i][2].split(',')
            count_roles = len(s[i][2])
            for j in range(count_roles):
                s[i][2][j] = s[i][2][j].replace('[', '')
                s[i][2][j] = s[i][2][j].replace(']', '')
                s[i][2][j] = s[i][2][j].replace("'", '')
                s[i][2][j] = s[i][2][j].replace(' ', '')
        hero_nums = set()
        for hero_num in range(1, count_heroes):
            flag = 1
            roles = set()
            for role in s[hero_num][2]:
                roles.add(role)
            print(roles)
            print(req_roles)
            for req_role in req_roles:
                if req_role not in roles:
                    flag = 0
                    break
            if flag == 1:
                hero_nums.add(s[hero_num][0])
        key_sort = (key_sort3, key_sort4, key_sort5, key_sort6, key_sort7, key_sort8, key_sort9, key_sort10, key_sort11)
        s = sorted(s, key=key_sort[rank-3], reverse=True)
        n = 0
        winrates_str = ''
        for i in range(count_heroes):
            if s[i][0] in hero_nums:
                n += 1
                winrates_str += s[i][1] + ' ' + s[i][rank] + '\n'
                if n == 30:
                    break
        return winrates_str


def key_sort3(strs):
    return strs[3]
def key_sort4(strs):
    return strs[4]
def key_sort5(strs):
    return strs[5]
def key_sort6(strs):
    return strs[6]
def key_sort7(strs):
    return strs[7]
def key_sort8(strs):
    return strs[8]
def key_sort9(strs):
    return strs[9]
def key_sort10(strs):
    return strs[10]
def key_sort11(strs):
    return strs[11]


def save_img(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(r.text, "lxml")
    kek = soup.find('div', {'class': 'image-container image-container-avatar image-container-hero'})
    kek = str(kek)
    name = kek[kek.find('alt')+5:]
    name = name[:name.find('"')]
    s = kek[kek.find('src')+5:]
    s = s[:s.find('"')]
    s = 'https://www.dotabuff.com'+s
    p = requests.get(s)
    out = open(name+"_img.jpg", "wb")
    out.write(p.content)
    out.close()


def fill_heroes_links():
    url = 'https://ru.dotabuff.com/heroes'
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(r.text, "lxml")
    req = str(soup.find('div', {'class': 'hero-grid'}))
    pos = req.find('href')
    heroes_links = set()
    while (pos != -1):
        req = req[pos + 6:]
        link = req[:req.find('"')]
        link = 'https://www.dotabuff.com' + link
        heroes_links.add(link)
        pos = req.find('href')
    return heroes_links


def reduc_brightness(dir, name):
    from PIL import Image, ImageDraw  # Подключим необходимые библиотеки.
    image = Image.open(dir + name + "_img.jpg")  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
    factor = -75
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0] + factor
            b = pix[i, j][1] + factor
            c = pix[i, j][2] + factor
            if (a < 0):
                a = 0
            if (b < 0):
                b = 0
            if (c < 0):
                c = 0
            if (a > 255):
                a = 255
            if (b > 255):
                b = 255
            if (c > 255):
                c = 255
            draw.point((i, j), (a, b, c))
    image.save(dir + name + "_img_black.jpg", "JPEG")
    del draw


def black_images():
    with open('winrates.json', 'r') as f:
        s = f.readlines()
        count_heroes = len(s)
        for hero_num in range(1, count_heroes):
            s[hero_num] = s[hero_num].split(';')
            reduc_brightness('dota_img/', s[hero_num][1])
