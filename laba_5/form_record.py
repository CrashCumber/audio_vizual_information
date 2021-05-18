import sys
import os

from PIL import ImageChops, Image

root, dirs, files = list(os.walk("results"))[0]
files.sort()


root_h, dirs_h, files_h = list(os.walk("hists"))[0]
files_h.sort()
#
# _, _, files_i = list(os.walk("inverts_letters"))[0]
# files_i.sort()


with open("README.md", "a") as file:
    img = Image.open(f"string.bmp")
    img = ImageChops.invert(img)
    img.save("invert_string.bmp")

    for i in range(len(files)):
        title = f"{i+1}. \n\n"
        h = f"![](hists/{i}.png)\n\n"
        j = f"![](results/{i}.bmp)\n\n"
        img = Image.open(f"results/{i}.bmp")
        img = ImageChops.invert(img)
        img.save("invert_letters/" + str(i) + ".bmp")
        i_ = f"![](invert_letters/{i}.bmp)\n\n"
        file.writelines([title, j, i_, h])
