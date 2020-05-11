import pygame, sys
import filters

pygame.init()
screen = pygame.display.set_mode([1000, 600])
#bools
dragging = False
#constants
buttons=[]
titles=["Black & White","Blur","Invert","Sharpen","Edge Detection","Sepia"]
#fonts
myfont = pygame.font.SysFont('ArialBold', 32)
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
    title = "Black & White"
    w = 160
    h = 47
    x = 820
    y = 100

class Slider:
    x = 500
    y = 300
    Ex = 562.5
    Ey = 287.5
    lineHeight = 5
    lineWidth = 150
    ellipseHeight = 25
    ellipseWidth = 25
slider = Slider()


#buttons
for i in range(6):
    button = Button(820,100+i * 75,titles[i])
    buttons.append(button)

#Menu screen functions
def drawUI():

    pygame.draw.rect(screen, (0, 0, 0), (slider.x,slider.y,slider.lineWidth,slider.lineHeight), 0)
    pygame.draw.ellipse(screen,(0,0,100),(slider.Ex, slider.Ey, slider.ellipseHeight,slider.ellipseWidth),0)

    for button in buttons:
        screen.blit(BUTTON_IMG, (button.x,button.y))
        buttonLabel = myfont.render(button.title, 1, pygame.color.THECOLORS['black'])
        screen.blit(buttonLabel, (button.x, button.y))

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
                bluePhoto = filters.diySepia(FILENAME)
                IMAGE_CURRENT = pygame.image.load(bluePhoto)



def checkSlider(mouse_x, mouse_y):
    #x = pygame.mouse.get_pos()[0]
    #y = pygame.mouse.get_pos()[1]
    if pointInRect(mouse_x, mouse_y, slider.x, slider.y,slider.lineWidth, slider.ellipseHeight):
        print("slider clicked!")
        print(mouse_x)
        slider.Ex = mouse_x


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

    label = myfont.render("Welcome!", 1, pygame.color.THECOLORS['black'])
    screen.blit(label, (180, 10))

    #update the display
    pygame.display.update()


pygame.quit()
