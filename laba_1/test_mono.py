from laba_1.utils import mono, Image


def mono_test(img, res):
    """Улучшенный алгоритм адаптивной бинаризации Бернсена."""
    img_s = mono(img)
    img_s.save(f"result_images/binary_images/{res}.png")


img_name = input("Enter name of image:")
img_name_res = input("Enter result of image:")

img = Image.open(f"images/{img_name}.jpg")
mono_test(img, img_name_res)
