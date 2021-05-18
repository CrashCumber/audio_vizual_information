import os

root, dirs, files = list(os.walk("reference"))[0]
files.sort()


root_h, dirs_h, files_h = list(os.walk("hists"))[0]
files_h.sort()

_, _, files_i = list(os.walk("inverts_letters"))[0]
files_i.sort()

with open("README.md", "w") as file:

    for i in range(len(files)):
        title = f"{i+1}. \n\n"
        h = f"![](hists/{files_h[i]})\n\n"
        s = f"![](reference/{files[i]})\n\n"
        i = f"![](inverts_letters/{files_i[i]})\n\n"

        file.writelines([title, s, i, h])
