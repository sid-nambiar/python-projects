#IT SHOULD ALLOW FOR HOLDING OF THE MOUSE BUTTON TO COCK BACK THE BOW
    #change to drawing_bow bool
#IT SHOULD ALLOW FOR MULTIPLE ARROWS
    #still have to remove them from the list when hit target or go off the screen


import pygame, sys
pygame.init()
screen = pygame.display.set_mode([640,480])
white = [255, 255, 255]

#constants
firstTime = True
BESTSCORE = 0
highscores = open('highscores.txt', 'a+')
TARGET_COLOR_HEIGHT = 10
TARGET_X = 590
TARGET_WIDTH = 10
TARGET_SPEED = 6
ARROW_SPEED = 20 #don't change, otherwise collision detection might break
ARROW_LENGTH = 20 #don't change, otherwise collision detection might break
BLACK_HIT_POINTS = 5
BLUE_HIT_POINTS = 10
RED_HIT_POINTS = 15
YELLOW_HIT_POINTS = 30
ARCHER_X = 10 #don't change, otherwise collision detection might break
BACKGROUND_IMAGE = pygame.image.load("castle.png")
ARCHER_STANDING = pygame.image.load("archer5.png")
ARCHER_SHOOTING1 = pygame.image.load("archer1.png")
ARCHER_SHOOTING2 = pygame.image.load("archer2.png")
ARCHER_SHOOTING3 = pygame.image.load("archer3.png")
ARCHER_SHOOTING4 = pygame.image.load("archer4.png")
SHOT_OFFSET_X = 20 #don't change, otherwise collision detection might break
SHOT_OFFSET_Y = 28


#the game's variables
score = 0
myfont = pygame.font.SysFont('Arial', 22)
target_y = 200
target_direction = 'down'
archer_y = 170
drawing_bow = False
autoshoot = False
arrows_x = []
arrows_y = []


#draw the side view of a target that goes black, blue, red, yellow (outside to inside)
#should use the target_y as the top of the target
#make it 3d by drawing ellipses inside each other
def drawTarget():
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['black'],(TARGET_X,target_y,40,70))
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['blue'],(TARGET_X+6,target_y+10,28,50))
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['red'],(TARGET_X+11,target_y+20,18,30))
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['yellow'],(TARGET_X+16,target_y+29,8,13))



def moveTarget():
    global target_direction, target_y #need to do this if we want to change a global variable in a function
    if target_direction == 'down':
        target_y += TARGET_SPEED
    else:
        target_y -= TARGET_SPEED

    #check if it should change directions
    if target_y <= 0:
        target_direction = 'down'
    elif target_y >= 410: #screen height (480) minus target height (70)
        target_direction = 'up'

def moveArrows():
    for index in range(len(arrows_x)):
        arrows_x[index] += ARROW_SPEED

def writeHighScore():
    highscores.write(str(score) + '\n')

def readHighScores():
    global BESTSCORE
    highscores_read = open('highscores.txt', 'r')
    file_lines=highscores_read.readlines()
    scores = []
    for line in file_lines:
        scores.append(int(line))
    BESTSCORE = max(scores)


def seeIfHitTarget():
    global score
    for index in range(len(arrows_x)):
        shot_x = arrows_x[index]
        shot_y = arrows_y[index]
        if shot_x + ARROW_LENGTH == TARGET_X + 20: #then it got to where the target is
            #see what the color is at that spot
            pixel_color = screen.get_at([shot_x + ARROW_LENGTH,shot_y])
            if pixel_color != pygame.color.THECOLORS['gray']: #it it something
                shooting = False
                if pixel_color == pygame.color.THECOLORS['black']:
                    score += BLACK_HIT_POINTS

                elif pixel_color == pygame.color.THECOLORS['blue']:
                    score += BLUE_HIT_POINTS

                elif pixel_color == pygame.color.THECOLORS['red']:
                    score += RED_HIT_POINTS

                elif pixel_color == pygame.color.THECOLORS['yellow']:
                    score += YELLOW_HIT_POINTS


def drawArcher():
    if drawing_bow == True:
        if archer_image <= 2:
            screen.blit(ARCHER_SHOOTING1, [ARCHER_X, archer_y])
        elif archer_image <= 4:
            screen.blit(ARCHER_SHOOTING2, [ARCHER_X, archer_y])
        elif archer_image <= 6:
            screen.blit(ARCHER_SHOOTING3, [ARCHER_X, archer_y])
        else:
            screen.blit(ARCHER_SHOOTING4, [ARCHER_X, archer_y])

    else:
        screen.blit(ARCHER_STANDING, [ARCHER_X, archer_y])


def moveArcher():
    global archer_y
    archer_y = pygame.mouse.get_pos()[1] #returns the (x,y) of the mouse position so we want the 1 spot
    if archer_y > 420: #don't let the archer go off the bottom of the screen
        archer_y = 420

def drawArrows():
    for index in range(len(arrows_x)):
        pygame.draw.rect(screen,pygame.color.THECOLORS['tan3'],(arrows_x[index],arrows_y[index],ARROW_LENGTH,2))
        pygame.draw.rect(screen,pygame.color.THECOLORS['gray'],(arrows_x[index]+ARROW_LENGTH,arrows_y[index]-1,4,4))



running = True
#game loop
while running:
    if firstTime == True:
        readHighScores()
        print(str(BESTSCORE))
    for event in pygame.event.get():
        #check if you've exited the game
        if event.type == pygame.QUIT:
            running = False
            writeHighScore()

        #check if you clicked
        if event.type == pygame.MOUSEBUTTONDOWN and drawing_bow == False:
            drawing_bow = True
            archer_image = 0

        if event.type == pygame.MOUSEBUTTONUP:
            #has to wait until fully drawn back
            if archer_image >= 10:
                drawing_bow = False
                arrows_x.append(ARCHER_X + SHOT_OFFSET_X)
                arrows_y.append(archer_y + SHOT_OFFSET_Y)
            else:
                autoshoot = True




    #make the screen completely white
    screen.fill(white)


    #game logic
    moveArcher()

    moveTarget()

    moveArrows()

    #have to cycle through the images before allowing the firing the arrow
    if drawing_bow == True:
        archer_image += 1 #this variable is used by the drawArcher function
        if archer_image >= 10 and autoshoot == True:
            drawing_bow = False
            arrows_x.append(ARCHER_X + SHOT_OFFSET_X)
            arrows_y.append(archer_y + SHOT_OFFSET_Y)
            autoshoot = False


    #draw everything on the screen
    label = myfont.render("Score: " + str(score), 1, pygame.color.THECOLORS['black'])
    screen.blit(label, (280, 10))
    screen.blit(BACKGROUND_IMAGE, (0,0))
    drawArcher()
    drawArrows()
    drawTarget() #want to draw on top of shot
    #update the entire display
    pygame.display.update()

    #handle collisions after updating displacy
    seeIfHitTarget()
    firstTime= False


pygame.quit()
