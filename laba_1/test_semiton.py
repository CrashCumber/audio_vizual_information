from laba_1.utils import semitone, Image


def semitone_test(img, img_name):
    img_s = semitone(img)
    img_s.save(f"result_images/{img_name}_s.png")


img_name = input("Enter name of image:")
img = Image.open(f"images/{img_name}.jpg")
semitone_test(img, img_name)
