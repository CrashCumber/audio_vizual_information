from PIL import Image

from laba_1 import INDENT


def upsampling(img, m):
    """Increasing the image by m."""

    width = img.size[0]
    height = img.size[1]
    new_w = int(width * m - 1)
    new_h = int(height * m - 1)

    new_image = Image.new("RGB", (new_w, new_h))
    for x in range(new_w):
        for y in range(new_h):
            pix = img.getpixel((x / m, y / m))
            new_image.putpixel((x, y), pix)
    return new_image


def downsampling(img, n):
    """Reducing the image by n."""

    width = img.size[0]
    height = img.size[1]
    new_w = int(width / n - 1)
    new_h = int(height / n - 1)

    new_image = Image.new("RGB", (new_w, new_h))
    for x in range(new_w):
        for y in range(new_h):
            pix = img.getpixel((x * n, y * n))
            new_image.putpixel((x, y), pix)
    return new_image


def resampling(img, k):
    """Сhanging the image scale in k = m / n"""

    width = img.size[0]
    height = img.size[1]
    new_w = int(width * k - 1)
    new_h = int(height * k - 1)

    new_image = Image.new("1", (new_w, new_h))
    for x in range(new_w):
        for y in range(new_h):
            pix = img.getpixel((x / k, y / k))
            new_image.putpixel((x, y), pix)
    return new_image


def semitone(img):
    """Reducing the image to a semitone"""
    if str(img.mode) == "L":
        return img

    width = img.size[0]
    height = img.size[1]
    new_image = Image.new("L", (width, height))

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            sum_ = 0.3 * pix[0] + 0.59 * pix[1] + 0.11 * pix[2]
            # sum_ = sum(pix) // 3
            new_image.putpixel((x, y), int(sum_))
    return new_image


def mono(img):
    """Converting the image to black and white."""
    if str(img.mode) == "1":
        return img

    img = semitone(img)
    integral_img = integral(img)
    width = img.size[0]
    height = img.size[1]
    new_image = Image.new("1", (width, height))

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            int_pix = mid_pix(integral_img, x, y, width, height)
            if pix < int_pix:
                new_image.putpixel((x, y), 0)
            else:
                new_image.putpixel((x, y), 1)

    return new_image


def integral(img):
    """Calculating the integral image."""

    width = img.size[0]
    height = img.size[1]
    integral_img = [[0 for _ in range(width)] for _ in range(height)]

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            if x == 0 and y == 0:
                new_pix = pix
            elif x == 0 and y > 0:
                new_pix = pix + integral_img[y - 1][x]
            elif x > 0 and y == 0:
                new_pix = pix + integral_img[y][x - 1]
            else:
                new_pix = (
                    pix
                    - integral_img[y - 1][x - 1]
                    + integral_img[y - 1][x]
                    + integral_img[y][x - 1]
                )
            integral_img[y][x] = new_pix
    return integral_img


def mid_pix(integral_img, x, y, width, height, indent=INDENT):
    """Average value of a pixel on an area with an indent s."""

    sqrt = 0
    pix = 0

    if y + indent >= height or x + indent >= width:
        if y + indent >= height and x + indent >= width:
            x = width - 1
            y = height - 1
            pix = (
                integral_img[y][x]
                - integral_img[y - indent][x]
                - integral_img[y][x - indent]
                + integral_img[y - indent][x - indent]
            )
            sqrt = (x + 1 - (x - indent)) * (y + 1 - (y - indent))

        elif y <= indent <= x and x + indent >= width:
            pix = (
                integral_img[y + indent][width - 1]
                - integral_img[y + indent][x - indent]
            )
            sqrt = (width - 1 - (x - indent)) * (y + indent + 1)
        elif x <= indent <= y and y + indent >= height:
            pix = (
                integral_img[height - 1][x + indent]
                - integral_img[y - indent][x + indent]
            )
            sqrt = (x + indent + 1) * (height - 1 - (y - indent) + 1)

        elif y + indent >= height:
            pix = (
                integral_img[height - 1][x + indent]
                - integral_img[y - indent][x + indent]
                - integral_img[height - 1][x - indent]
                + integral_img[y - indent][x - indent]
            )
            sqrt = (x + indent - (x - indent)) * (height - 1 - (y - indent) + 1)

        elif x + indent >= width:
            pix = (
                integral_img[y + indent][width - 1]
                - integral_img[y - indent][width - 1]
                - integral_img[y + indent][x - indent]
                + integral_img[y - indent][x - indent]
            )
            sqrt = (width - (x - indent)) * (y + indent - (y - indent) + 1)
        return pix // sqrt

    pix = integral_img[y + indent][x + indent]
    if x > indent and y > indent:
        pix = (
            pix
            - integral_img[y - indent][x + indent]
            - integral_img[y + indent][x - indent]
            + integral_img[y - indent][x - indent]
        )
        sqrt = (indent * 2 + 1) ** 2

    elif y <= indent <= x:
        pix -= integral_img[y + indent][x - indent]
        sqrt = (x + indent - (x - indent) + 1) * (y + indent + 1)
    elif x <= indent <= y:
        pix -= integral_img[y - indent][x + indent]
        sqrt = (x + indent + 1) * (y + indent - (y - indent) + 1)

    elif x < indent and y < indent:
        pix = integral_img[y][x]
        sqrt = (x + 1) * (y + 1)
    return pix // sqrt
