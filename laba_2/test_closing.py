from PIL import Image

from laba_2.utils import close

img_name = input("Enter name of image:")
img_res_name = input("Enter name of res image:")

img = Image.open(f"images/{img_name}")
res = close(img, img_res_name)

res.save(f"result_images/{img_res_name}.png")
