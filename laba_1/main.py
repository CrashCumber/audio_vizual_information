import numpy as np

from laba_1.utils import *


def resize(img, m, n):
    m = int(input())
    n = int(input())
    img_up = upsampling(img, m)
    img_up.show()

    img_down = downsampling(img, n)
    img_down.show()

    k = m / n
    img_samp = resampling_one(img, k)
    img_samp.show()
    img_samp_2 = downsampling(img_up, n)
    img_samp_2.show()


def main(img):
    img_gray = mono(img)
    img_gray.show()

img = Image.open('images/eye.jpg')

main(img)
