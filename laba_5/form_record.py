import sys
import os

root, dirs, files = list(os.walk("results"))[0]
files.sort()


root_h, dirs_h, files_h = list(os.walk("hists"))[0]
files_h.sort()
#
# _, _, files_i = list(os.walk("inverts_letters"))[0]
# files_i.sort()

with open('README.md', 'a') as file:

    for i in range(len(files)):
        title = f'{i+1}. \n\n'
        h = f'![](hists/{i}.png)\n\n'
        i = f'![](results/{i}.bmp)\n\n'

        file.writelines([title, i, h])

