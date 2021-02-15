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
    l = integral(img)
    width = img.size[0]
    height = img.size[1]

    new_image = Image.new('1', (width, height))
    for x in range(width):
        for y in range(height):

            pix = img.getpixel((x, y))
            int_pix = mid_pix(l, x, y, width, height)
            print(pix, int_pix)
            if pix < int_pix:
                new_image.putpixel((x, y), 0)
            else:
                new_image.putpixel((x, y), 1)

    return new_image


def integral(img):

    width = img.size[0]
    height = img.size[1]
    l = [[0 for _ in range(width)] for _ in range(height)]

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            if x == 0 and y == 0:
                new_pix = pix
            elif x == 0 and y > 0:
                new_pix = pix + l[y - 1][x]
            elif x > 0 and y == 0:
                new_pix = pix + l[y][x - 1]
            else:
                new_pix = pix - l[y-1][x-1] + l[y - 1][x] + l[y][x-1]
            l[y][x] = new_pix
    return l


def mid_pix(l, x, y, width, height, s=40):

    # if x > s and y > s and y + s < height and x + s < width:
    #     return (l[y + s][x + s] - l[y - s][x + s] - l[y + s][x - s] + l[y - s][x - s]) // ((s * 2 + 1)**2)
    if y + s >= height or x + s >= width:
        x_ = width - x
        y_ = height - y
        if y + s >= height and x + s >= width:
            x = width - 1
            y = height - 1
            p = l[y][x] - l[y - s][x] - l[y][x - s] + l[y - s][x - s]
            sqrt = (s + 1) ** 2

        elif y + s >= height:
            y = height - 1
            p = l[y][x] - l[y - s][x + s] - l[y][x - s] + l[y - s][x - s]
            sqrt = (y_ + 1) * (s * 2 + 1)

        elif x + s >= width:
            x = width - 1
            p = l[y][x] - l[y - s][x] - l[y + s][x - s] + l[y - s][x - s]
            sqrt = (x_ + 1) * (s * 2 + 1)

        return p // sqrt

    p = l[y + s][x + s]
    if x > s and y > s:
        p = p - l[y - s][x + s] - l[y + s][x - s] + l[y - s][x - s]
        sqrt = (s * 2 + 1)**2
    elif y <= s <= x:
        p -= l[y + s][x - s]
        sqrt = (y + 1) * (s * 2 + 1)
    elif x <= s <= y:
        p -= l[y - s][x + s]
        sqrt = (x + 1) * (s * 2 + 1)
    elif x < s and y < s:
        p = l[y][x]
        sqrt = (x + 1) * (y + 1)
    print(x, y)
    return p // sqrt
