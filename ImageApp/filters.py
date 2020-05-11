from PIL import Image, ImageFilter,ImageEnhance
import PIL.ImageOps

blurRadius = 2.5
sharpness= 10

def diySepia(filename):
    new_name = "sepia.png"
    img = Image.open(filename)
    width, height = img.size
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x,y))
            newRed = int(r*0.5)
            newGreen = int(g*0.5)
            newBlue = int(b*10)
            pixels[x,y] =(newRed,newGreen, newBlue)
    img.save(new_name)
    return new_name


def Invert(filename):
    new_name = "inverted.png"
    img = Image.open(filename)
    img = PIL.ImageOps.invert(img)
    img.save(new_name)
    return new_name

def findEdge(filename):
    new_name = "demonic.png"
    img = Image.open(filename)
    img = img.filter(ImageFilter.FIND_EDGES)
    img.save(new_name)
    return new_name

def blackAndWhite(filename):
    new_name = "blackAndWhite.png"
    img = Image.open(filename)
    img = img.convert('LA')
    img.save(new_name)
    return new_name

def sharpen(filename):
    new_name="sharp.png"
    img = Image.open(filename)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness)
    img.save(new_name)
    return new_name


def blur(filename):
    new_name = "blur.png"
    img = Image.open(filename)
    img = img.filter(ImageFilter.GaussianBlur(blurRadius))
    img.save(new_name)
    return new_name

def exampleFilters(filename):
    img = Image.open("dogs.jpg")
    width, height = img.size

    img0 = img.convert('LA')
    img1 = img.rotate(180)
    img = img.filter(ImageFilter.BLUR)
    img3 = img.resize((int(width/2), int(height/2)))
    img4 = img.transpose(Image.FLIP_LEFT_RIGHT)
    img5 = PIL.ImageOps.invert(img)

    img0.save("0.png")
