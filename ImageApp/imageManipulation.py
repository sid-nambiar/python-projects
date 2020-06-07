import pygame, sys
import filters

pygame.init()
screen = pygame.display.set_mode([1000, 700])
#bools
dragging = False
#constants
buttons=[]
sliders=[]
titles=["Black & White","Blur","Invert","Sharpen","Edge Detection","Sepia","Reset"]
sliderTitles=["Saturation", "Brightness"]
#fonts
myfont = pygame.font.SysFont('ArialBold', 24)
#colors
white=(255 ,255, 255)

#images
FILENAME = "dog.png"
IMAGE_ORIGINAL = pygame.image.load(FILENAME)
BUTTON_IMG = pygame.image.load("button.png")
IMAGE_CURRENT = IMAGE_ORIGINAL

class Button:
    def __init__(self, x, y, title):
        self.title = title
        self.x = x
        self.y = y
        self.w = 160
        self.h = 47

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
for i in range(7):
    button = Button(820,100+i * 75,titles[i])
    buttons.append(button)

#Menu screen functions
def drawUI():
    for slider in sliders:
        pygame.draw.rect(screen, (0, 0, 0), (slider.x, slider.y, slider.lineWidth, slider.lineHeight), 0)
        pygame.draw.ellipse(screen, (0, 0, 100), (slider.Ex, slider.Ey, slider.ellipseHeight, slider.ellipseWidth), 0)

    for button in buttons:
        screen.blit(BUTTON_IMG, (button.x,button.y))
        buttonLabel = myfont.render(button.title, 1, pygame.color.THECOLORS['black'])
        screen.blit(buttonLabel, (button.x+10, button.y+12))

def pointInRect(pt_x, pt_y, rect_x, rect_y, rect_w, rect_h):
    if (pt_x > rect_x) and (pt_x < rect_x + rect_w) and (pt_y > rect_y) and (pt_y < rect_y + rect_h):
        return True
    else:
        return False

def checkButtons():
    global IMAGE_CURRENT
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    for button in buttons:
        if pointInRect(x, y, button.x, button.y, button.w, button.h):
            print("Button clicked!")
            if button.title == "Black & White":
                blackAndWhitePhoto = filters.blackAndWhite(FILENAME) # call function in filters.py file
                IMAGE_CURRENT = pygame.image.load(blackAndWhitePhoto) # updates image
            elif button.title == "Blur":
                bluredPhoto = filters.blur(FILENAME)
                IMAGE_CURRENT = pygame.image.load(bluredPhoto)
                filters.blurRadius += 1
            elif button.title == "Invert":
                invertedPhoto = filters.Invert(FILENAME)
                IMAGE_CURRENT = pygame.image.load(invertedPhoto)
            elif button.title == "Edge Detection":
                demonicPhoto = filters.findEdge(FILENAME)
                IMAGE_CURRENT = pygame.image.load(demonicPhoto)
            elif button.title == "Sharpen":
                sharpPhoto = filters.sharpen(FILENAME)
                IMAGE_CURRENT = pygame.image.load(sharpPhoto)
                filters.sharpness += 2.5
            elif button.title == "Sepia":
                sepiaPhoto = filters.diySepia(FILENAME)
                IMAGE_CURRENT = pygame.image.load(sepiaPhoto)
            elif button.title == "Reset":
                IMAGE_CURRENT = IMAGE_ORIGINAL

def changeSaturationLevel(mouse_x,slider):
    #left = -
    #right = +
    global IMAGE_CURRENT

    diff = mouse_x-slider.middleX
    print(diff)

    if diff > 0:
        half=slider.lineWidth/2
        distPercent=diff/half
        newSaturationLevel = distPercent*10
        filters.saturationLevel =  newSaturationLevel
    elif diff < 0:
        filters.saturationLevel = 0.5

    saturatedPhoto = filters.saturation(FILENAME)
    IMAGE_CURRENT = pygame.image.load(saturatedPhoto)

def checkSlider(mouse_x, mouse_y):
    for slider in sliders:
        if pointInRect(mouse_x, mouse_y, slider.x, slider.y,slider.lineWidth, slider.ellipseHeight):
            slider.Ex = mouse_x
            if slider.title =="Saturation":
                changeSaturationLevel(mouse_x, slider)
            elif slider.title ==  "Brightness":
                pass



running = True
#game loop
while running:
    screen.fill(white)

    for event in pygame.event.get():
        #check if you've exited the game
        if event.type == pygame.QUIT:
            running = False

        #check if you clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            checkButtons()

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging == True:
                mouse_x, mouse_y = event.pos
                checkSlider(mouse_x,mouse_y)

    screen.blit(IMAGE_CURRENT, (0,0))

    #drawing components
    drawUI()

    #label = myfont.render("Welcome!", 1, pygame.color.THECOLORS['black'])
    #screen.blit(label, (180, 10))

    #update the display
    pygame.display.update()


pygame.quit()
