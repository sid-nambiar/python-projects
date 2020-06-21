from PIL import Image, ImageFilter,ImageEnhance
import PIL.ImageOps

blurRadius = 2.5
sharpness= 10
saturationLevel = 1
brightnessLevel = 1

angle = 0



def diySepia(filename):
    new_name = "sepia.png"
    img = Image.open(filename)
    width, height = img.size
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x,y))
            newRed = int((r * .393) + (g * .769) + (b * .189))
            newGreen = int((r * .349) + (g * .686) + (b * .168))
            newBlue = int((r * .272) + (g * .534) + (b * .131))
            pixels[x,y] =(newRed,newGreen, newBlue)
    img.save(new_name)
    return new_name

def brightness(filename):
    new_name = "bright.png"
    img = Image.open(filename)
    converter = PIL.ImageEnhance.Brightness(img)
    img2 = converter.enhance(brightnessLevel)
    img2.save(new_name)
    return new_name



def saturation(filename):
    new_name = "saturated.png"
    img = Image.open(filename)
    converter = PIL.ImageEnhance.Color(img)
    img2 = converter.enhance(saturationLevel)
    img2.save(new_name)
    return new_name

def Invert(filename):
    new_name = "inverted.png"
    img = Image.open(filename)
    width, height = img.size
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            newRed = int(255-r)
            newGreen = int(255-g)
            newBlue = int(255-b)
            pixels[x, y] = (newRed, newGreen, newBlue)
    img.save(new_name)
    return new_name
    #new_name = "inverted.png"
    #img = Image.open(filename)
    #img = PIL.ImageOps.invert(img)
    #img.save(new_name)
    return new_name

def findEdge(filename):
    new_name = "demonic.png"
    img = Image.open(filename)
    img = img.filter(ImageFilter.FIND_EDGES)
    img.save(new_name)
    return new_name

def blackAndWhite(filename):
    #new_name = "blackAndWhite.png"
    #img = Image.open(filename)
    #img = img.convert('LA')
    #img.save(new_name)
    #return new_name
    new_name = "blackAndWhite.png"
    img = Image.open(filename)
    width, height = img.size
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            newImg= int((r+g+b)/3)
            pixels[x, y] = (newImg, newImg, newImg)
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

def rotation(filename):
    new_name = "rotated.png"
    img = Image.open(filename)
    img2 = img.rotate(angle)
    img2.save(new_name)
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
