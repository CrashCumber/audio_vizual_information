import csv

import numpy
from PIL import Image, ImageDraw, ImageFont

import matplotlib.pyplot as plt


s = 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցուփքեւօֆ'

fieldnames = [
            "weight_black",
            "normal_black",
            "x_center",
            "y_center",
            "x_norm_center",
            "y_norm_center",
            "x_moment",
            "x_norm_moment",
            "y_moment",
            "y_norm_moment",
        ]

white = 255
black = 0


def get_profiles(file):
    img = Image.open(file)
    pix = img.load()
    width = img.size[0]
    height = img.size[1]
    x_profiles = []
    y_profiles = []

    for i in range(width):
        bright = 0
        for j in range(height):
            if (pix[i, j] == black):
                bright += 1
        x_profiles.append(bright)

    for i in range(height):
        bright = 0
        for j in range(width):
            if (pix[j, i] == black):
                bright += 1
        y_profiles.append(bright)

    return x_profiles, y_profiles


def get_hist_profile(s):

    for c in s:
        x_profile, y_profile = get_profiles("reference/" + c + '.bmp')
        fig, axs = plt.subplots(1, 2, figsize=(9, 3))
        axs[0].hist(x_profile)
        axs[1].hist(y_profile, orientation="horizontal")
        plt.savefig(f'hists/{c}.png')
        del fig
        del axs


def attribute(file):
    img = Image.open(file)
    pix = img.load()
    width = img.size[0]
    height = img.size[1]

    size, size1, weight_black, normal_black, x_center, y_center = 0, 0, 0, 0, 0, 0

    for i in range(width):
        for j in range(height):
            if (pix[i, j] == black):
                weight_black += 1
                x_center += i
                y_center += j

    size = width * height
    normal_black = weight_black / size
    x_center = x_center / weight_black
    x_norm_center = (x_center - 1) / (width - 1)
    y_center = y_center / weight_black
    y_norm_center = (y_center - 1) / (height - 1)

    return [weight_black, normal_black, x_center, y_center, x_norm_center, y_norm_center]


def attribute_moment(file):
    img = Image.open(file)
    pix = img.load()
    width = img.size[0]
    height = img.size[1]

    weight_black, normal_black, x_center, y_center, x_norm_center, y_norm_center = attribute(file)
    x_moment, x_norm_moment, y_moment, y_norm_moment = 0, 0, 0, 0

    for i in range(width):
        for j in range(height):
            if (pix[i, j] == black):
                x_moment = ((j - y_center) ** 2)
                y_moment = ((i - y_center) ** 2)
                # I45center = ((j - y_center - i + x_center) ** 2) / 2
                # I135center = ((j - y_center + i - x_center) ** 2) / 2

    size1 = width * width + height * height
    x_norm_moment = x_moment / size1
    y_norm_moment = y_moment / size1

    return [x_moment, x_norm_moment, y_moment, y_norm_moment]


def get_info(file):
    res = [str(file).split('/')[1][0]]

    return res + attribute(file) + attribute_moment(file)


def generate_csv(string):
    rows = [fieldnames]
    for c in string:
        rows.append(get_info("reference/" + str(c) + '.bmp'))

    with open('info.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerows(rows)


def return_opt_size(font, alphabet):
    img = Image.new("1", (50, 50), "white")
    draw = ImageDraw.Draw(img)
    wmax, hmax = -1, -1
    for c in alphabet:
        sz = draw.textsize(str(c), font)
        wmax, hmax = max(wmax, sz[0]), max(hmax, sz[1])
    return wmax, hmax


def reference_image(img):
    pix = img.load()
    width, height = img.size[0], img.size[1]
    hor_p = [0 for x in range(width)]
    ver_p = [0 for x in range(height)]
    for i in range(width):
        for j in range(height):
            if pix[i, j] == 0:
                hor_p[i] += 1
                ver_p[j] += 1
    x0, y0, x1, y1 = 0, 0, width, height
    eps = 0
    for i in range(width):
        if hor_p[i] > eps:
            x0 = i
            break

    for i in range(width - 1, -1, -1):
        if hor_p[i] <= eps:
            x1 = i
        else:
            break

    for i in range(height):
        if ver_p[i] > eps:
            y0 = i
            break

    for i in range(height - 1, -1, -1):
        if ver_p[i] <= eps:
            y1 = i
        else:
            break

    new_sz = (x0, y0, x1, y1)
    return img.crop(new_sz)


def gen_letters_reference_images(letters, save_to_file):
    """Получение эталоного изображения"""

    font = ImageFont.truetype(font="arm.ttf", size=40)
    sz = return_opt_size(font, letters)
    for letter in letters:
        img = Image.new("1", sz, "white")
        draw = ImageDraw.Draw(img)
        cursz = draw.textsize(str(letter), font)
        pos = ((sz[0] - cursz[0]) // 2, (sz[1] - cursz[1]) // 2)
        draw.text((pos[0], 0), str(letter), font=font)
        img = reference_image(img)
        if save_to_file:
            img.save("reference/" + str(letter) + ".bmp")







