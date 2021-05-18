import os

import numpy as np
from PIL import Image, ImageChops

from laba_1.utils import mono
from laba_6.crop_options import cut


s = "աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցուփքեւօֆ"
k = 1 / 1.6

white = 255
black = 0


def convert_to_bin(img):
    if str(img.mode) != "1":
        img = mono(img)
    img.save("string.png")
    return img


def get_dif(real, ideal):
    res = 0
    for i in range(len(real)):
        res += (real[i] - ideal[i]) ** 2
    return 1 - res ** 0.5


def attribute(file):
    img = Image.open(file)
    width = img.size[0]
    height = img.size[1]

    weight_black, normal_black, x_center, y_center = 0, 0, 0, 0

    for i in range(width):
        for j in range(height):
            if img.getpixel((i, j)) == black:
                weight_black += 1
                x_center += i
                y_center += j

    size = width * height
    normal_black = weight_black / size

    x_center = x_center / weight_black
    x_norm_center = (x_center - 1) / (width - 1)
    y_center = y_center / weight_black
    y_norm_center = (y_center - 1) / (height - 1)

    x_moment, x_norm_moment, y_moment, y_norm_moment, I45_center, I135_center = (
        0,
        0,
        0,
        0,
        0,
        0,
    )

    for i in range(width):
        for j in range(height):
            if img.getpixel((i, j)) == black:
                x_moment += (j - y_center) ** 2
                y_moment += (i - x_center) ** 2
                I45_center += ((j - y_center - i + x_center) ** 2) / 2
                I135_center += ((j - y_center + i - x_center) ** 2) / 2

    x_norm_moment = x_moment / (weight_black ** 2)
    y_norm_moment = y_moment / (weight_black ** 2)
    I45_rel = I45_center / (weight_black ** 2)
    I135_rel = I135_center / (weight_black ** 2)

    return [
        normal_black,
        x_norm_center,
        y_norm_center,
        x_norm_moment,
        y_norm_moment,
        I135_rel,
        I45_rel,
    ]


reference_letter_close_values = {}
real_letter_close_values = {}

img = Image.open("image.png")
img = convert_to_bin(img)

text_len = cut("string.png")

for i in s:
    close = attribute("reference/" + i + ".bmp")
    reference_letter_close_values[i] = close


for i in range(text_len):
    close = attribute("letters/" + str(i) + ".bmp")
    real_letter_close_values[i] = close


res = {i: [] for i in range(text_len)}
for i in range(text_len):
    close_letter = real_letter_close_values[i]
    for j in s:
        value = get_dif(close_letter, reference_letter_close_values[j])
        res[i].append({j: value})

    res[i] = sorted(res[i], key=lambda k: list(k.values())[0], reverse=True)

print(reference_letter_close_values)
# for i in res:
#     print(i, res[i])
# img = Image.open('letters/0.bmp')
# a = np.asfarray(img)
# for i in a:
#     print(i[:10])
#
# img = Image.open('reference/ե.bmp')
# print(np.asfarray(img))

root, dirs, files = list(os.walk("reference"))[0]
files.sort()


root_h, dirs_h, files_h = list(os.walk("letters"))[0]
files_h.sort()


with open("README.md", "a") as file:

    for i in range(len(files_h)):
        title = f"{i}. \n\n"
        # h = f'![](letters/{i}.png)\n\n'
        # j = f'![](results/{i}.bmp)\n\n'
        # img = Image.open(f"results/{i}.bmp")
        # img = ImageChops.invert(img)
        # img.save("invert_letters/" + str(i) + ".bmp")
        # i_ = f'![](invert_letters/{i}.bmp)\n\n'
        j = f"![](letters/{i}.bmp)\n\n"
        fields = (
            f"\n#### Фактические значения\n\n"
            f"+ Удельный вес = {real_letter_close_values[0][0]}\n\n"
            f"+ Нормированные координаты центра тяжести x = {real_letter_close_values[1][1]}\n\n"
            f"+ Нормированные координаты центра тяжести y = {real_letter_close_values[2][2]}\n\n"
            f"+ Нормированные осевые моменты инерции по x = {real_letter_close_values[3][3]}\n\n"
            f"+ Нормированные осевые моменты инерции по y = {real_letter_close_values[4][4]}\n\n"
            f"+ Диагональный осевой момент инерции  = {real_letter_close_values[5][5]}\n\n"
            f"+ Диагональный осевой момент инерции  = {real_letter_close_values[6][6]}\n\n"
        )
        m = reference_letter_close_values[list(res[i][0].keys())[0]]

        fields_ = (
            f"\n#### Теоретическое значение самого подходящего варианта {list(res[i][0].keys())[0]}\n\n"
            f"+ Удельный вес = {m[0]}\n\n"
            f"+ Нормированные координаты центра тяжести x = {m[1]}\n\n"
            f"+ Нормированные координаты центра тяжести y = {m[2]}\n\n"
            f"+ Нормированные осевые моменты инерции по x = {m[3]}\n\n"
            f"+ Нормированные осевые моменты инерции по y = {m[4]}\n\n"
            f"+ Диагональный осевой момент инерции  = {m[5]}\n\n"
            f"+ Диагональный осевой момент инерции  = {m[6]}\n\n"
            f"#### Значения для всего алфавита\n\n"
        )
        dred = ""
        for d in res[i]:
            dred += f"{list(d.keys())[0]} : {list(d.values())[0]}; \n\n"

        file.writelines([title, j, fields, fields_, dred])

    for i in s:
        title = f"{i}  )  \n\n"
        # h = f'![](letters/{i}.png)\n\n'
        # j = f'![](results/{i}.bmp)\n\n'
        # img = Image.open(f"reference/{i}.bmp")

        j = f"![](reference/{i}.bmp)\n\n"
        fields = (
            f"\nУдельный вес = {reference_letter_close_values[i][0]}\n\n"
            f"+ Нормированные координаты центра тяжести x = {reference_letter_close_values[i][1]}\n\n"
            f"+ Нормированные координаты центра тяжести y = {reference_letter_close_values[i][2]}\n\n"
            f"+ Нормированные осевые моменты инерции по x = {reference_letter_close_values[i][3]}\n\n"
            f"+ Нормированные осевые моменты инерции по y = {reference_letter_close_values[i][4]}\n\n"
            f"+ Диагональный осевой момент инерции  = {reference_letter_close_values[i][5]}\n\n"
            f"+ Диагональный осевой момент инерции  = {reference_letter_close_values[i][6]}\n\n"
        )

        file.writelines([title, j, fields])
