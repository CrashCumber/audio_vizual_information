from PIL import Image


k = 1 / 1.6

white = 255
black = 0


def cut(fname):
    img = Image.open(fname)
    width, height = img.size

    x_profile, y_profile = get_profiles(img)
    num = []
    eps = 0
    for i in range(len(x_profile)):
        if x_profile[i] <= eps:
            step = 0
        else:
            step += 1
            right = i
            left = right - step
            if x_profile[i + 1] <= eps:
                num.append((left, right))

    for i in range(len(num)):
        left, right = num[i]
        new_img = img.crop((left, 0, right + 2, height))

        new_img.save("letters/" + str(i) + ".bmp")
    for i in range(len(num)):
        img = crop("letters/" + str(i) + ".bmp")
        img.save("letters/" + str(i) + ".bmp")
    return len(num)


def crop(fname):
    img = Image.open(fname)
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

