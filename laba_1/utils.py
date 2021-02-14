import numpy as np
from PIL import Image, ImageDraw


def upsampling(img, m):

    width = img.size[0]
    height = img.size[1]
    new_w = int(width * m - 1)
    new_h = int(height * m - 1)

    new_image = Image.new('RGB', (new_w, new_h))
    for x in range(new_w):
        for y in range(new_h):
            pix = img.getpixel((x / m, y / m))
            new_image.putpixel((x, y), pix)
    return new_image


def downsampling(img, n):

    width = img.size[0]
    height = img.size[1]
    new_w = int(width / n - 1)
    new_h = int(height / n - 1)

    new_image = Image.new('RGB', (new_w, new_h))
    for x in range(new_w):
        for y in range(new_h):
            pix = img.getpixel((x * n, y * n))
            new_image.putpixel((x, y), pix)
    return new_image


def resampling(img, m, n):
    """
    m: increase
    n: decrease
    """
    width = img.size[0]
    height = img.size[1]
    new_w = int(width * m / n - 1)
    new_h = int(height * m / n - 1)

    new_image = Image.new('RGB', (new_w, new_h))
    for x in range(new_w):
        for y in range(new_h):
            pix = img.getpixel((x * n / m, y * n / m))
            new_image.putpixel((x, y), pix)
    return new_image


def resampling_one(img, k):

    width = img.size[0]
    height = img.size[1]
    new_w = int(width * k - 1)
    new_h = int(height * k - 1)

    new_image = Image.new('RGB', (new_w, new_h))
    for x in range(new_w):
        for y in range(new_h):
            pix = img.getpixel((x / k, y / k))
            new_image.putpixel((x, y), pix)
    return new_image


def semitone_rgb(img):
    width = img.size[0]
    height = img.size[1]
    new_image = Image.new('RGB', (width, height))

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            sum_ = sum(pix) // 3
            new_image.putpixel((x, y), (sum_, sum_, sum_))
    return new_image


def semitone(img):
    width = img.size[0]
    height = img.size[1]
    new_image = Image.new('L', (width, height))

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            sum_ = sum(pix) // 3
            new_image.putpixel((x, y), sum_)
    return new_image


def mono(img):
    img = semitone(img)
    img.show()
    int_img = integral(img)
    int_img.show()
    width = img.size[0]
    height = img.size[1]
    new_image = Image.new('1', (width, height))
    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            int_pix = mid_s(img, x, y, width, height)
            if pix < int_pix:
                new_image.putpixel((x, y), 0)
            else:
                new_image.putpixel((x, y), 1)

    return new_image


def integral(img):

    width = img.size[0]
    height = img.size[1]
    int_img = Image.new('L', (width, height))

    l = [[0 for _ in range(height)] for _ in range(width)]

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            if x == 0 and y == 0:
                new_pix = pix

            elif x == 0 and y > 0:
                new_pix = pix + l[x][y - 1]

            elif x > 0 and y == 0:
                new_pix = pix + l[x-1][y]
            else:
                new_pix = pix - l[x-1][y-1] + l[x][y - 1] + l[x-1][y]

            int_img.putpixel((x, y), new_pix)
            l[x][y] = new_pix

    return int_img


def mid_s(img, x, y, width, heigjt):
    s = 4
    if x + s >= width and y + s >= heigjt :
        p = img.getpixel((x, y)) - img.getpixel((x - s, y)) \
            - img.getpixel((x, y - s)) + img.getpixel((x - s, y - s))
    elif y + s >= heigjt:
        p = img.getpixel((x + s, y)) - img.getpixel((x - s, y)) \
            - img.getpixel((x, y - s)) + img.getpixel((x - s, y - s))
    elif x + s >= width:
        p = img.getpixel((x, y + s)) - img.getpixel((x - s, y)) \
            - img.getpixel((x, y - s)) + img.getpixel((x - s, y - s))
    elif x > s and y > s:
        p = img.getpixel((x + s, y + s)) - img.getpixel((x - s, y))\
            - img.getpixel((x, y - s)) + img.getpixel((x - s, y - s))
    elif y < s < x:

        p = img.getpixel((x + s, y + s)) - img.getpixel((x - s, y))
    elif x < s < y:
        p = img.getpixel((x + s, y + s)) - img.getpixel((x, y - s))
    else:
        p = img.getpixel((x + s, y + s))
    return p *s
#
# def integral_(img):
#
#     width = img.size[0]
#     height = img.size[1]
#     int_img = Image.new('RGB', (width, height))
#     sum__x = 0
#     for x in range(width):
#         sum__x += img.getpixel((x, 0))[0]
#         sum_ = 0
#         for y in range(height):
#             pix = img.getpixel((x, y))[0]
#             sum_ += pix
#             int_img.putpixel((x, y), (sum_, sum_, sum_))
#     int_img.show()
#     return int_img


# def integral__(img):
#
#     width = img.size[0]
#     height = img.size[1]
#     int_img = Image.new('RGB', (width, height))
#
#     def l(x, y):
#         if x < 0 or y < 0:
#             return 0
#         pix = img.getpixel((x, y))[0]
#         new_pix = pix - l(x-1, y-1) + l(x, y - 1) + l(x-1, y)
#         int_img.putpixel((x, y), new_pix)
#         return new_pix
#
#     l(width - 1, height - 1)
#     int_img.show()
#     return int_img

#
# def mono(img, s=4):
#     img = semitone(img)
#     width = img.size[0]
#     height = img.size[1]
#     new_image = Image.new('RGB', (width, height))
#
#     int_ing = integral(img)
#
#     def get_s(x, y, s):
#         p = 0
#         if  0 < x < s and 0< y < s:
#             p = int_ing.getpixel((x + s, y + s))[0]
#             return p
#         elif 0 < x < s and y > s:
#             p = int_ing.getpixel((x + s, y + s))[0] - int_ing.getpixel((x, y - s))[0]
#             return p * 2 // s
#         elif x > s and 0 < y < s:
#             p = int_ing.getpixel((x + s, y + s))[0] - int_ing.getpixel((x - s, y))[0]
#             return p * 2 // s
#         elif x > s and y> s:
#             p = int_ing.getpixel((x + s, y + s))[0] - int_ing.getpixel((x- s, y))[0] - int_ing.getpixel((x, y- s))[0] + int_ing.getpixel((x - s, y - s))[0]
#         return p // (s*s)
#     # for x in range(width):
#     #     for y in range(height):
#     #         pix = img.getpixel((x, y))[0]
#     #
#     #         int_pix = get_s(x - 1, y - 1, s)
#     #         print(pix, int_pix)
#     #         if pix < int_pix:
#     #             new_image.putpixel((x, y), (0, 0, 0))
#     #         else:
#     #             new_image.putpixel((x, y), (255, 255, 255))
#
#     return new_image
