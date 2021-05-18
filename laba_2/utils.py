from PIL import Image, ImageChops
from laba_1.utils import integral, mono


def erode(img):
    """Сжатие"""

    width = img.size[0]
    height = img.size[1]
    integral_img = integral(img)
    new_image = Image.new("1", (width, height))

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            int_pix = sum_pix_area(integral_img, x, y, width, height) - pix
            if int_pix < 8:
                new_image.putpixel((x, y), 0)
            else:
                new_image.putpixel((x, y), 1)

    return new_image


def dilate(img):
    """Расширение"""

    width = img.size[0]
    height = img.size[1]
    integral_img = integral(img)
    new_image = Image.new("1", (width, height))

    for x in range(width):
        for y in range(height):
            pix = img.getpixel((x, y))
            int_pix = sum_pix_area(integral_img, x, y, width, height) - pix
            if int_pix > 0:
                new_image.putpixel((x, y), 1)
            else:
                new_image.putpixel((x, y), 0)

    return new_image


def close(img, img_res_name):
    """Закрытие - фильтрация"""
    if str(img.mode) != "1":
        img = mono(img)
        img.save(f"result_images/{img_res_name}_s.png")
    res_img = dilate(img)
    res_img.save(f"result_images/{img_res_name}_d.png")

    res_img = erode(res_img)
    return res_img


def sum_pix_area(integral_img, x, y, width, height, indent=1):
    """Sum value of a pixel on an area with an indent."""
    sum_ = 0

    if y + indent >= height or x + indent >= width:
        if y + indent >= height and x + indent >= width:
            x = width - 1
            y = height - 1
            sum_ = (
                integral_img[y][x]
                - integral_img[y - indent - 1][x]
                - integral_img[y][x - indent - 1]
                + integral_img[y - indent - 1][x - indent - 1]
            )

        elif y <= indent <= x and x + indent >= width:
            sum_ = (
                integral_img[y + indent][width - 1]
                - integral_img[y + indent][x - indent - 1]
            )
        elif x <= indent <= y and y + indent >= height:
            sum_ = (
                integral_img[height - 1][x + indent]
                - integral_img[y - indent - 1][x + indent]
            )

        elif y + indent >= height:
            sum_ = (
                integral_img[height - 1][x + indent]
                - integral_img[y - indent - 1][x + indent]
                - integral_img[height - 1][x - indent - 1]
                + integral_img[y - indent - 1][x - indent - 1]
            )

        elif x + indent >= width:
            sum_ = (
                integral_img[y + indent][width - 1]
                - integral_img[y - indent - 1][width - 1]
                - integral_img[y + indent][x - indent - 1]
                + integral_img[y - indent - 1][x - indent - 1]
            )
        return sum_

    if x > indent and y > indent:
        sum_ = (
            integral_img[y + indent][x + indent]
            - integral_img[y - indent - 1][x + indent]
            - integral_img[y + indent][x - indent - 1]
            + integral_img[y - indent - 1][x - indent - 1]
        )

    elif y <= indent <= x:
        sum_ -= integral_img[y + indent][x - indent - 1]
    elif x <= indent <= y:
        sum_ -= integral_img[y - indent - 1][x + indent]

    elif x < indent and y < indent:
        sum_ = integral_img[y][x]
    return sum_


def difference_images(img1, img2):
    """Разница изображений."""
    result = ImageChops.difference(img1, img2)
    inv_img = ImageChops.invert(result)
    return inv_img
