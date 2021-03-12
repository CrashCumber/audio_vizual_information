from PIL import Image

from laba_1.utils import semitone

t = 2


def roberts(img):
    """Оператор Робертса"""
    if str(img.mode) != 'L':
        img = semitone(img)
        img.save(f'images/people_s.png')

    width = img.size[0]
    height = img.size[1]
    new_image = Image.new('L', (width, height))
    df_max = 0
    for x in range(width-1):
        for y in range(height-1):
            G1 = img.getpixel((x+1, y+1)) - img.getpixel((x, y))
            G2 = img.getpixel((x, y+1)) - img.getpixel((x-1, y))
            df = abs(G2) + abs(G1)
            if df > df_max:
                df_max = df

    df_max = 255 / df_max

    for x in range(width-1):
        for y in range(height-1):
            G1 = img.getpixel((x+1, y+1)) - img.getpixel((x, y))
            G2 = img.getpixel((x, y+1)) - img.getpixel((x-1, y))
            df = abs(G2) + abs(G1)
            df_norm = df * df_max
            if df_norm > t:
                new_image.putpixel((x, y), 255)
            else:
                new_image.putpixel((x, y), 0)
    return new_image


image = Image.open(f'images/people_s.png')
image_r = roberts(image)
image_r.save(f'result_images/people_t{str(t)}.png')
