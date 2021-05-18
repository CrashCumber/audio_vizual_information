import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from laba_1.utils import mono


s = "աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցուփքեւօֆ"

white = 255
black = 0


def get_profiles(img):
    # img = convert_to_bin(img)

    width = img.size[0]
    height = img.size[1]
    x_profiles = []
    y_profiles = []

    for x in range(width):
        bright = 0
        for y in range(height):
            pix = img.getpixel((x, y))
            if pix == black:
                bright += 1
        x_profiles.append(bright)

    for y in range(height):
        bright = 0
        for x in range(width):
            pix = img.getpixel((x, y))
            if pix == black:
                bright += 1
        y_profiles.append(bright)

    return x_profiles, y_profiles


def print_bar(img):
    x_profiles, y_profiles = get_profiles(img)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3))

    axs[0].bar(np.arange(0, len(x_profiles)), height=x_profiles)
    axs[1].barh(np.arange(0, len(y_profiles)), width=y_profiles)

    plt.savefig(f"profile.png", dpi=70)


def convert_to_bin(img):
    if str(img.mode) != "1":
        img = mono(img)
    img.save("string.bmp")
    return img


def segmentation(img):
    height = img.size[1]
    x_profiles, y_profiles = get_profiles(img)
    ep = 0
    res = []
    for i in range(len(x_profiles)):

        if x_profiles[i] <= ep:
            step = 0
        else:
            step += 1
            right = i
            left = right - step
            if x_profiles[i + 1] <= ep:
                res.append((left, right))

    for i in range(len(res)):
        left, right = res[i]
        new_im = img.crop((left, 0, right + 2, height))
        new_im = reference_image(new_im)
        new_im.save("results/" + str(i) + ".bmp", mode="1")
    return res


def get_hist_profile(res):

    for i in range(len(res)):
        img = Image.open("results/" + str(i) + ".bmp")
        img = reference_image(img)

        x_profile, y_profile = get_profiles(img)
        fig, axs = plt.subplots(1, 2, figsize=(9, 3))

        axs[0].bar(np.arange(0, len(x_profile)), height=x_profile)
        axs[1].barh(np.arange(0, len(y_profile)), width=y_profile)

        plt.savefig(f"hists/{i}.png", dpi=70)
        del fig
        del axs


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
    hor_p = [0 for _ in range(width)]
    ver_p = [0 for _ in range(height)]
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


img = Image.open("string.bmp")
print(segmentation(img))
