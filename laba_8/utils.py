import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
num_fig = 0


def get_semitone_asarray(matrix):
    return np.sum(matrix, axis=2) // 3


def get_hist(matrix, nm):
    global num_fig
    matrix = get_semitone_asarray(matrix)
    sh = np.reshape(matrix, (1, -1))
    plt.figure(num_fig)
    plt.hist(sh[0], bins=256)
    plt.savefig(f"hists/{nm}.png")
    num_fig += 1


def normalize(matrix):
    max_image = np.max(matrix, axis=1)
    max_rgb = np.max(max_image, axis=0)

    return matrix / max_rgb, max_rgb


def contrast(matrix, c, f, y):
    norm_matrix, max_rgb = normalize(matrix)

    norm_new_matrix = (c * (norm_matrix + f) ** y)
    new_matrix = (norm_new_matrix * max_rgb).astype("uint8")
    Image.fromarray(new_matrix, mode="RGB").save(f"results/{name+str(c)+str(f)+str(y)}.png")

    return Image.fromarray(new_matrix, mode="RGB"), new_matrix


name = input()
format = input()
img = Image.open(f"images/{name}.{format}")
matrix = np.asarray(img, dtype='uint8')
get_hist(matrix, name)


values = (
    (1, 0, 0.1),
    (1, 0, 0.5),
    (1, 0, 1.5),
    (1, 0, 2),
    (1, 0, 2.5),

    (0.1, 0, 1),
    (0.8, 0, 1),
    (2, 0, 1),
    (0.5, 0, 1),
    (1.5, 0, 1),

    (1, -10, 1),
    (1, 10, 1),
    (1, 100, 1),
    (1, 50, 1),
    (1, 256, 1),
)

for i in values:
    c, f, y = i
    new, matrix_new = contrast(matrix, float(c), float(f), float(y))
    # new.show()
    get_hist(matrix_new, name + str(c) + str(f) + str(y))
# get_hist(matrix)


