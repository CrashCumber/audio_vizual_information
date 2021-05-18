from PIL import Image

from laba_2.utils import difference_images


img_name = input("Enter name of image:")
img_name_res = input("Enter result name of image:")
img_res_name = input("Enter name of diff image:")

image_1 = Image.open(f"result_images/{img_name}")
image_2 = Image.open(f"result_images/{img_name_res}")


diff = difference_images(image_1, image_2)
diff.save(f"result_images/diff/{img_res_name}.png")
