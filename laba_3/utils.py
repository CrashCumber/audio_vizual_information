from PIL import Image
from laba_1.utils import semitone

t = 2


def get_matrix(img):
    if str(img.mode) != "L":
        img = semitone(img)
    width, height = img.size[0], img.size[1]
    new_image_y = Image.new("L", (width, height))
    new_image_x = Image.new("L", (width, height))
    new_image_x_y = Image.new("L", (width, height))

    for x in range(width - 1):
        for y in range(height - 1):
            G1 = img.getpixel((x + 1, y + 1)) - img.getpixel((x, y))
            G2 = img.getpixel((x, y + 1)) - img.getpixel((x - 1, y))
            df = abs(G2) + abs(G1)

            new_image_x.putpixel((x, y), G1)
            new_image_y.putpixel((x, y), G2)
            new_image_x_y.putpixel((x, y), df)

    new_image_x.save("result_images/GX.png")
    new_image_y.save("result_images/GY.png")
    new_image_x_y.save("result_images/G.png")


def roberts(img):
    """Оператор Робертса"""
    if str(img.mode) != "L":
        img = semitone(img)
        img.save(f"images/people_s.png")

    width = img.size[0]
    height = img.size[1]
    new_image = Image.new("L", (width, height))
    df_max = 0
    for x in range(width - 1):
        for y in range(height - 1):
            G1 = img.getpixel((x + 1, y + 1)) - img.getpixel((x, y))
            G2 = img.getpixel((x, y + 1)) - img.getpixel((x - 1, y))
            df = abs(G2) + abs(G1)
            if df > df_max:
                df_max = df

    df_max = 255 / df_max

    for x in range(width - 1):
        for y in range(height - 1):
            G1 = img.getpixel((x + 1, y + 1)) - img.getpixel((x, y))
            G2 = img.getpixel((x, y + 1)) - img.getpixel((x - 1, y))
            df = abs(G2) + abs(G1)
            df_norm = df * df_max
            if df_norm > t:
                new_image.putpixel((x, y), 255)
            else:
                new_image.putpixel((x, y), 0)
    return new_image

file = input()
image = Image.open(f"images/{file}.png")
get_matrix(image).save(f'result_images/{file}_t{str(t)}.png')
