import pygame, sys,os.path
import filters

pygame.init()
screen = pygame.display.set_mode([1000, 700])

def scaledImage(img):
    sz = img.get_rect().size
    factor = 800/sz[0] # try scaling in horizontal direction
    if sz[1]*factor > 600:
        factor = 600/sz[1] # else, scale in the vertical direction
    scaledImg = pygame.transform.rotozoom(img, 0, factor)
    #scaledImg = pygame.transform.scale(img, (800, 600))
    return scaledImg

#bools
dragging = False
dark_mode = False
#constants
buttons=[]
sliders=[]
arrows=[]
arrowTitles=["rot L", "rot R","flip"]
titles=["Black & White","Blur","Invert","Sharpen","Edge Detection","Sepia","Reset", "New Image","Save Final"]
sliderTitles=["Saturation", "Brightness"]
#fonts
myfont = pygame.font.SysFont('ArialBold', 24)
#colors
white=(255 ,255, 255)
grey = (77, 77, 77)


FILENAME = "dog.png"


def input_check():
    global FILENAME
    while True:
        USER_INPUT = input("What image do you want to upload? ")
        if os.path.isfile(USER_INPUT):
            FILENAME = USER_INPUT
            break
        else:
            print("file does not exist try checking your spelling and try again")

PREV_FILENAME = FILENAME
IMAGE_ORIGINAL = pygame.image.load(FILENAME)
IMAGE_ORIGINAL = scaledImage(IMAGE_ORIGINAL)
BUTTON_IMG = pygame.image.load("button.png")
BUTTON_DARK = pygame.image.load("button_dark.png")
CURRENT_BUTTON = BUTTON_IMG
IMAGE_CURRENT = IMAGE_ORIGINAL
ARROW_RIGHT_IMG=pygame.image.load("blueArrowRight.png")
ARROW_LEFT_IMG=pygame.image.load("blueArrowLeft.png")
ARROW_FLIP_IMG= pygame.image.load("flip.png")
arrowImages = [ARROW_LEFT_IMG, ARROW_RIGHT_IMG,ARROW_FLIP_IMG]

class Button:
    def __init__(self, x, y, title):
        self.title = title
        self.x = x
        self.y = y
        self.w = 160
        self.h = 47

class Arrow:
    def __init__(self, x, y, title):
        self.title = title
        self.x = x
        self.y = y
        self.w = 75
        self.h = 75

class Slider:
    def __init__(self, x, y, title):
        self.title=title
        self.x = x
        self.y = y

        self.lineWidth = 150
        self.lineHeight = 5
        self.ellipseHeight = 25
        self.ellipseWidth = 25

        self.middleX = self.x + self.lineWidth /2 - self.ellipseWidth/2
        self.middleY = self.y + self.lineHeight / 2 - self.ellipseHeight / 2

        self.Ex = self.middleX
        self.Ey = self.middleY

for i in range(2):
    slider = Slider(75+i * 200,650,sliderTitles[i])
    sliders.append(slider)

#buttons
for i in range(9):
    button = Button(820, 47+i * 75,titles[i])
    buttons.append(button)

for i in range(3):
    arrow = Arrow(465+i*80,620, arrowTitles[i])
    arrows.append(arrow)



#Menu screen functions
def drawUI():
    for i in range(len(arrows)):
        screen.blit(arrowImages[i],(arrows[i].x,arrows[i].y))

    for slider in sliders:
        pygame.draw.rect(screen, (0, 0, 0), (slider.x, slider.y, slider.lineWidth, slider.lineHeight), 0)
        pygame.draw.ellipse(screen, (0, 0, 100), (slider.Ex, slider.Ey, slider.ellipseHeight, slider.ellipseWidth), 0)

    for button in buttons:
        screen.blit(CURRENT_BUTTON, (button.x,button.y))
        buttonLabel = myfont.render(button.title, 1, pygame.color.THECOLORS['black'])
        screen.blit(buttonLabel, (button.x+10, button.y+12))

def pointInRect(pt_x, pt_y, rect_x, rect_y, rect_w, rect_h):
    if (pt_x > rect_x) and (pt_x < rect_x + rect_w) and (pt_y > rect_y) and (pt_y < rect_y + rect_h):
        return True
    else:
        return False

def checkButtons():
    global IMAGE_CURRENT, PREV_FILENAME,USER_INPUT, FILENAME, IMAGE_ORIGINAL
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    for button in buttons:
        if pointInRect(x, y, button.x, button.y, button.w, button.h):
            if button.title == "Black & White":
                blackAndWhitePhoto = filters.blackAndWhite(PREV_FILENAME) # call function in filters.py file
                IMAGE_CURRENT = pygame.image.load(blackAndWhitePhoto)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                PREV_FILENAME = blackAndWhitePhoto
            elif button.title == "Blur":
                bluredPhoto = filters.blur(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(bluredPhoto)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                filters.blurRadius += 1
                PREV_FILENAME = bluredPhoto
            elif button.title == "Invert":
                invertedPhoto = filters.Invert(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(invertedPhoto)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                PREV_FILENAME = invertedPhoto
            elif button.title == "Edge Detection":
                demonicPhoto = filters.findEdge(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(demonicPhoto)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                PREV_FILENAME = demonicPhoto
            elif button.title == "Sharpen":
                sharpPhoto = filters.sharpen(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(sharpPhoto)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                filters.sharpness += 2.5
                PREV_FILENAME = sharpPhoto
            elif button.title == "Sepia":
                sepiaPhoto = filters.diySepia(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(sepiaPhoto)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                PREV_FILENAME = sepiaPhoto
            elif button.title == "Reset":
                for slider in sliders:
                    slider.Ex= slider.middleX
                IMAGE_CURRENT = IMAGE_ORIGINAL
                PREV_FILENAME = FILENAME

            elif button.title == "New Image":
                input_check()
                PREV_FILENAME = FILENAME
                IMAGE_ORIGINAL = pygame.image.load(FILENAME)
                IMAGE_ORIGINAL = scaledImage(IMAGE_ORIGINAL)
                IMAGE_CURRENT = IMAGE_ORIGINAL
            elif button.title == "Save Final":
                filters.saveFinal(PREV_FILENAME)

def changeSaturationLevel(mouse_x,slider):
    #left = -
    #right = +
    global IMAGE_CURRENT, PREV_FILENAME

    diff = mouse_x-slider.middleX

    if diff > 0:
        half=slider.lineWidth/2
        distPercent=diff/half
        newSaturationLevel = distPercent*10
        filters.saturationLevel =  newSaturationLevel
    elif diff < 0:
        filters.saturationLevel = 0.5

    '''saturatedPhoto = filters.saturation(PREV_FILENAME)
    IMAGE_CURRENT = pygame.image.load(saturatedPhoto)
    IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
    PREV_FILENAME = saturatedPhoto'''

    saturatedPhoto = filters.saturation(PREV_FILENAME)
    IMAGE_CURRENT = pygame.image.load(saturatedPhoto)
    IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
    #PREV_FILENAME = saturatedPhoto

def changeBrightnessLevel(mouse_x,slider):
    global IMAGE_CURRENT, PREV_FILENAME
    diff = mouse_x-slider.middleX
    half = slider.lineWidth / 2
    distPercent = abs(diff / half)
    if diff >= 0:
        newBrightnessLevel = min(distPercent + 1, 1.95)
        filters.brightnessLevel = newBrightnessLevel
    elif diff < 0:
        newBrightnessLevel = max(0.55, 1-distPercent)
        filters.brightnessLevel = newBrightnessLevel


    brightPhoto = filters.brightness(PREV_FILENAME)
    IMAGE_CURRENT = pygame.image.load(brightPhoto)
    IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
    #PREV_FILENAME = brightPhoto

def checkSlider(mouse_x, mouse_y):
    global checkingSaturation, checkingBrightness

    for slider in sliders:
        if pointInRect(mouse_x, mouse_y, slider.x, slider.y,slider.lineWidth, slider.ellipseHeight):
            slider.Ex = mouse_x
            if slider.title =="Saturation":
                checkingSaturation = True
                changeSaturationLevel(mouse_x, slider)
            elif slider.title ==  "Brightness":
                checkingBrightness = True
                changeBrightnessLevel(mouse_x, slider)


def checkArrow(mouse_x, mouse_y):
    global IMAGE_CURRENT,PREV_FILENAME
    for arrow in arrows:
        if pointInRect(mouse_x, mouse_y, arrow.x, arrow.y, arrow.w, arrow.h):
            if arrow.title == "rot L":
                filters.angle += 90
                if filters.angle > 360 or filters.angle < -360:
                    filters.angle = 0
                rotatedPhotoL =filters.rotation(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(rotatedPhotoL)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                PREV_FILENAME = rotatedPhotoL
            if arrow.title == "rot R":
                filters.angle += -90
                if filters.angle > 360 or filters.angle < -360:
                    filters.angle = 0
                rotatedPhotoR = filters.rotation(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(rotatedPhotoR)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                PREV_FILENAME = rotatedPhotoR
            if arrow.title == "flip":
                mirroredPhoto = filters.flip(PREV_FILENAME)
                IMAGE_CURRENT = pygame.image.load(mirroredPhoto)
                IMAGE_CURRENT = scaledImage(IMAGE_CURRENT)
                PREV_FILENAME = mirroredPhoto
            


running = True
checkingSaturation = False
checkingBrightness = False
#game loop
while running:
    if dark_mode == False:
        screen.fill(white)
        CURRENT_BUTTON = BUTTON_IMG
    else:
        screen.fill(grey)
        CURRENT_BUTTON = BUTTON_DARK
        

    for event in pygame.event.get():
        #check if you've exited the game
        if event.type == pygame.QUIT:
            running = False
    
        #check if you clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if checkingSaturation==True:
                checkingSaturation = False
                PREV_FILENAME = "saturated.png"
            if checkingBrightness==True:
                checkingBrightness = False
                PREV_FILENAME = "bright.png"
            dragging = True
            checkButtons()
            mouse_x,mouse_y= event.pos
            checkArrow(mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging == True:
                mouse_x, mouse_y = event.pos
                checkSlider(mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            if dark_mode == False:
                dark_mode = True
            else:
                dark_mode= False

    screen.blit(IMAGE_CURRENT, (0,0))

    #drawing components
    drawUI()

    #label = myfont.render("Welcome!", 1, pygame.color.THECOLORS['black'])
    #screen.blit(label, (180, 10))

    #update the display
    pygame.display.update()


pygame.quit()
