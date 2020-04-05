from PIL import Image, ImageFilter
import PIL.ImageOps

img = Image.open("dog.png")

img = img.filter(ImageFilter.BLUR)

img.save("modified_image.png")