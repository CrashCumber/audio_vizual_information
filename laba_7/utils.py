import numpy as np
from PIL import Image
from laba_1.utils import semitone

m = 0
n = 0
l = 256

name = "5"
img = Image.open(f"images/{name}_s.png")
img = semitone(img)
img.save(f"images/{name}_s.png")


def get_hararic(img):
    img_matrix = np.asarray(img).transpose()
    width = img.size[0]
    height = img.size[1]
    matrix = np.zeros((l, l))
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            pix = img_matrix[x, y]

            up_pix = img_matrix[x, y - 1]
            down_pix = img_matrix[x, y + 1]
            left_pix = img_matrix[x - 1, y]
            right_pix = img_matrix[x + 1, y]

            matrix[pix, up_pix] += 1
            matrix[pix, down_pix] += 1
            matrix[pix, left_pix] += 1
            matrix[pix, right_pix] += 1

    max_ = np.max(matrix)
    if max_ > 256:
        matrix = (matrix * 256) // max_
    for i in matrix:
        print(i[-1])

    return Image.fromarray(matrix), matrix


img_res, matrix_res = get_hararic(img)
img_res = img_res.convert("L")
img_res.save(f"results/{name}.png")

k = np.sum(matrix_res)
norm_matrix_res = matrix_res / k


def attribute(matrix):
    energy = np.sum(matrix ** 2)
    mrp = np.max(matrix)
    sub_matrix = matrix.copy()
    sub_matrix[sub_matrix == 0] = 1
    ent = -np.sum(np.multiply(np.log2(sub_matrix), matrix))
    tr = np.sum(np.diagonal(matrix))
    return energy, mrp, ent, tr


attributes = attribute(norm_matrix_res)
print(attributes)
