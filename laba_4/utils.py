import csv

from PIL import Image, ImageDraw, ImageFont


white = 255
black = 0
allCharact=[]


def count1(fname):
    img = Image.open(fname)
    pix = img.load()
    width = img.size[0]
    height = img.size[1]

    size, size1, countblack, normalblack, xcen, xcenter, xrel, ycen, ycenter, yrel = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


    for i in range(width):
        for j in range(height):
            if (pix[i, j] == black):
                countblack += 1
                xcen +=i
                ycen +=j


    size = width * height
    normalblack = countblack / size
    xcenter = xcen / countblack
    xrel = (xcenter - 1) / (width - 1)
    ycenter = ycen / countblack
    yrel = (ycenter - 1) / (height - 1)

    print("вес="+str(size))
    print("удельный вес=" + str(countblack))
    print("нормальный вес="+str(normalblack))
    print("x центр="+ str(xcenter))
    print("x норм =" + str(xrel))
    print("y центр="+ str(ycenter))
    print("y норм="+ str(yrel))

    return countblack,normalblack,xcenter,ycenter,xrel,yrel


def count2(fname):
    img = Image.open(fname)
    pix = img.load()
    width = img.size[0]
    height = img.size[1]

    counblack,normalblack,xcenter,ycenter,xrel,yrel=count1(fname)
    size1=0
    Ixcenter, Ixrel, Iycenter, Iyrel, I45center, I45rel, I135center, I135rel = 0, 0, 0, 0, 0, 0, 0, 0


    for i in range(width):
        for j in range(height):
            if (pix[i, j] == black):
                Ixcenter = ((j - ycenter) ** 2)
                Iycenter = ((i - ycenter) ** 2)
                I45center = ((j - ycenter - i + xcenter) ** 2) /2
                I135center = ((j - ycenter + i - xcenter) ** 2) /2

    size1 = width * width + height * height
    Ixrel = Ixcenter / size1
    Iyrel = Iycenter / size1
    I45rel = I45center / size1
    I135rel = I135center / size1

    print("x момент="+ str(Ixcenter))
    print("x момент норм="+ str(Ixrel))
    print("у момент="+ str(Iycenter))
    print("у момент норм="+ str(Iyrel))
    print("45 момент="+ str(I45center))
    print("45 момент норм ="+ str(I45rel))
    print("135 момент="+ str(I135center))
    print("135 момент норм="+ str(I135rel))
    print("-------------------------------")

    return Ixcenter,Ixrel,Iycenter,Iyrel,I45center,I45rel,I135rel,I135center

def mat(fname):
    counblack, normalblack, xcenter, ycenter, xrel, yrel = count1(fname)
    Ixcenter, Ixrel, Iycenter, Iyrel, I45center, I45rel, I135rel, I135center=count2(fname)

    lett= (str(fname)[0:1])+' ' + str(counblack) +' '+ str(normalblack)+' '+ str(xcenter)+' '+ str(xrel)+' '+ str(ycenter)+' '+ str(yrel)+' '+ \
            str(Ixcenter)+','+ str(Ixrel)+' '+ str(Iycenter)+' '+ str(Iyrel)+' '+ str(I45center)+' '+ str(I45rel)+' '+ str(I135center)+' '+ str(I135rel)
    print(lett)

    allCharact.append([(str(fname)[0:1]),normalblack, xcenter, xrel, ycenter, yrel, Ixcenter, Ixrel, Iycenter, Iyrel, I45center, I45rel, I135center,I135rel])

    with open('charact.csv', 'w', newline='') as csv_file:
        fieldnames = ['normalblack', 'xcenter', 'xrel', 'ycenter', 'yrel', 'Ixcenter', 'Ixrel', 'Iycenter', 'Iyrel', 'I45center', 'I45rel', 'I135center','I135rel']
        csv_writer = csv.writer(csv_file, fieldnames, delimiter=';')
        for item in allCharact:
            csv_writer.writerow(item)


def return_opt_size(font, alphabet):
    img = Image.new("1", (50, 50), "white")
    draw = ImageDraw.Draw(img)
    wmax, hmax = -1, -1
    for c in alphabet:
        sz = draw.textsize(str(c), font)
        wmax, hmax = max(wmax, sz[0]), max(hmax, sz[1])
    return wmax, hmax

def gen_letters_images(alphabet, save_to_file):
    font = ImageFont.truetype(font="arm.ttf", size=40)
    sz = return_opt_size(font, alphabet)
    lst = []
    i = 0
    for c in alphabet:
        img = Image.new("1", sz, "white")
        draw = ImageDraw.Draw(img)
        cursz = draw.textsize(str(c), font)
        pos = ((sz[0] - cursz[0]) // 2, (sz[1] - cursz[1]) // 2)
        draw.text((pos[0], 0), str(c), font=font)
        img = clip_image(img)
        if save_to_file:
            img.save("res/" + str(c) + ".bmp")
        i += 1
        lst.append(img)
    return lst


def clip_image(img):
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

    #new_sz = (x0, 0, x1, height)
    new_sz = (x0, y0, x1, y1)
    return img.crop(new_sz)


gen_letters_images('աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցուփքեւօֆ', True)

for c in 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցուփքեւօֆ':

        count1("res/"+str(c)+'.bmp')
        count2("res/"+str(c)+'.bmp')
        mat("res/"+str(c)+'.bmp')

















# import string
#
# from PIL import Image, ImageDraw, ImageFont
#
# for c in string.ascii_lowercase:
#     fontPath = "font.ttf"
#     sans16 = ImageFont.truetype(fontPath, 40)
#
#     im = Image.new("1", (50, 50), "white")
#     draw = ImageDraw.Draw(im)
#     draw.text((10, 0), str(c), font=sans16, fill="black")
#
#     im.save(str(c) + ".jpg")








