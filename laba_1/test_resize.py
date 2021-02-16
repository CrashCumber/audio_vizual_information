from laba_1 import M, N
from laba_1.utils import *


def upsampling_test(img):
    img_up = upsampling(img, M)
    img_up.show()
    img_up.save("result_images/img_up")


def downsampling_test(img):
    img_down = downsampling(img, N)
    img_down.show()
    img_down.save("result_images/img_down")


def resampling_test(img):
    k = M / N
    img_samp = resampling(img, k)
    img_samp.show()
    img_samp.save("result_images/img_samp_one")


def resampling_two_step_test(img):
    img_samp = downsampling(upsampling(img, M), N)
    img_samp.show()
    img_samp.save("result_images/img_samp_two")


img_name = input("Enter name of image:")
img = Image.open(f'images/{img_name}.jpg')

upsampling_test(img)
downsampling_test(img)
resampling_test(img)
resampling_two_step_test(img)
