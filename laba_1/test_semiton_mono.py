from laba_1.utils import semitone, mono, Image


def semitone_test(img):
    img_s = semitone(img)
    img_s.save("result_images/img_s.png")


def mono_test(img):
    """Улучшенный алгоритм адаптивной бинаризации Бернсена."""
    img_s = mono(img)
    img_s.save("result_images/img_mono.png")


img_name = input("Enter name of image:")
img = Image.open(f'images/{img_name}.jpg')
semitone_test(img)
mono_test(img)
