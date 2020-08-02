
import pygame, sys
import time
import scoreChart
pygame.init()
screen = pygame.display.set_mode([640, 480])


#constants
#fonts
myfont = pygame.font.SysFont('ArialBold', 32)
#colors
highscoreColorRed = True
white=(255 ,255, 255)
blue= (0, 170, 255)
#fps
FPS = 1
#scores
BESTSCORE = 0
BEST_OVERALL_SCORE = 0
highscores = open('highscores.txt', 'a+')
#points
BLACK_HIT_POINTS = 5
BLUE_HIT_POINTS = 10
RED_HIT_POINTS = 15
YELLOW_HIT_POINTS = 30
#positions/cordnates
TARGET_COLOR_HEIGHT = 20
TARGET_WIDTH = 20
TARGET_SIZE = 68
TARGET_SPEED = 6
ARROW_SPEED = 20
ARROW_LENGTH = 30
TARGET_X = 590
ARCHER_X = 10
SHOT_OFFSET_X = 20
SHOT_OFFSET_Y = 28
ARROW_HEIGHT = 5
#images
SCORE_CHART_IMAGE = pygame.image.load("resized_line_chart.png")
# SCORE_CHART_IMAGE= pygame.transform.scale(SCORE_CHART_IMAGE,(640, 480))
MENU_SCREEN_IMAGE = pygame.image.load("hallway.jpg")
BACKGROUND_IMAGE = pygame.image.load("pixel-castle.png")
ARCHER_STANDING = pygame.image.load("archer5.png")
ARCHER_SHOOTING1 = pygame.image.load("archer1.png")
ARCHER_SHOOTING2 = pygame.image.load("archer2.png")
ARCHER_SHOOTING3 = pygame.image.load("archer3.png")
ARCHER_SHOOTING4 = pygame.image.load("archer4.png")
archer_image = 0


#game logic
playerLetter = "A"
score = 0
target_y = 200
target_direction = 'down'
archer_y = 170
menu_screen_toggled = True
firstTime = True
drawing_bow = False
autoshoot = False
arrows_x = []
arrows_y = []


def playSound():
    soundObj = pygame.mixer.Sound('swoosh.wav')
    soundObj.play()
def soundDelay():
    for arrowX in arrows_x:
        if arrowX > 105 and arrowX < 115:
            playSound()

#Menu screen functions
def drawMenuScreenUI():
    screen.blit(MENU_SCREEN_IMAGE, (0, 0))
    drawMenuButtons()
    buttonLabel = myfont.render('player A', 1, pygame.color.THECOLORS['white'])
    screen.blit(buttonLabel, (0, 425))

    buttonLabel2 = myfont.render('player B', 1, pygame.color.THECOLORS['white'])
    screen.blit(buttonLabel2, (552, 425))

    MenuScreenText = myfont.render("Welcome To ", 1, pygame.color.THECOLORS['white'])
    screen.blit(MenuScreenText, (240, 180))

    MenuScreenText2 = myfont.render("Archery Game!", 1, pygame.color.THECOLORS["white"])
    screen.blit(MenuScreenText2,(240, 240))

def getPlayerButtonColor():
    global playerLetter
    pixelColor = screen.get_at(pygame.mouse.get_pos())
    if pixelColor == pygame.color.THECOLORS['blue']:
        playerLetter = "B"
        return True
    elif pixelColor == pygame.color.THECOLORS['red']:
        playerLetter = "A"
        return True
    else:
        return False


#drawing player buttons
def drawMenuButtons():
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['red'],(0, 390, 90, 90))
    pygame.draw.ellipse(screen, pygame.color.THECOLORS['blue'], (550, 390, 90, 90))

def drawScoreChart():
    screen.blit(SCORE_CHART_IMAGE, (0, 0))
    scoreChartInstructions = myfont.render('click to continue',1, pygame.color.THECOLORS['white'])
    screen.blit(scoreChartInstructions, (10,0))

#drawing the target
def drawTarget():
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['black'],(TARGET_X,target_y,40,70))
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['blue'],(TARGET_X+6,target_y+10,28,50))
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['red'],(TARGET_X+11,target_y+20,18,30))
    pygame.draw.ellipse(screen,pygame.color.THECOLORS['yellow'],(TARGET_X+16,target_y+29,8,13))

def moveTarget():
    global target_direction, target_y
    if target_direction == 'down':
        target_y += TARGET_SPEED
    else:
        target_y -= TARGET_SPEED

    #check if it should change directions
    if target_y <= 0:
        target_direction = 'down'
    elif target_y >= 410: #screen height
        target_direction = 'up'

def moveArrows():
    for index in range(len(arrows_x)):
        arrows_x[index] += ARROW_SPEED

def writeHighScore():
    if score != 0:
        finalStringScore = playerLetter + str(score)  + '\n'
        highscores.write(finalStringScore)

def readHighScores():
    global BESTSCORE, BEST_OVERALL_SCORE
    highscores_read = open('highscores.txt', 'r')
    file_lines=highscores_read.readlines()
    scores = []
    all_scores = []
    for line in file_lines:
        letterRemoved = line[1:]
        all_scores.append(int(letterRemoved))
        if line[0] == playerLetter:
            scores.append(int(letterRemoved))
    BEST_OVERALL_SCORE = max(all_scores)
    BESTSCORE = max(scores)

def seeIfHitTarget():
    global score
    target_center_y = target_y + TARGET_SIZE / 2

    for index in range(len(arrows_x)):
        shot_x = arrows_x[index]
        shot_y = arrows_y[index]
        if shot_x + ARROW_LENGTH == TARGET_X + ARROW_LENGTH:
            diff = abs(target_center_y - shot_y)
            if 0 <= diff <= 4:
                score += YELLOW_HIT_POINTS
            elif 4 <= diff <= 13:
                score += RED_HIT_POINTS
            elif 13 <= diff <= 23:
                score += BLUE_HIT_POINTS
            elif 23 <= diff <= 34:
                score += BLACK_HIT_POINTS
            else:
                score += 0  # Did not hit target


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
    archer_y = pygame.mouse.get_pos()[1] #returns the (x,y) of the mouse
    if archer_y > 420: #restricts player going off the screen
        archer_y = 420

def drawArrows():
    global arrows_x, arrows_y
    newArrowsX = []
    newArrowsY = []

    for index in range(len(arrows_x)):
        pygame.draw.rect(screen,pygame.color.THECOLORS['tan3'],(arrows_x[index],arrows_y[index],ARROW_LENGTH,ARROW_HEIGHT))
        pygame.draw.rect(screen,pygame.color.THECOLORS['gray'],(arrows_x[index]+ARROW_LENGTH,arrows_y[index]-1,4,4))
        if arrows_x[index] < 640:
            newArrowsX.append(arrows_x[index])
            newArrowsY.append(arrows_y[index])
    arrows_x = newArrowsX
    arrows_y = newArrowsY


chart_showing = True
play_sound = True
running = True
#game loop
while running:
    #finds out if menu screen is toggled
    if menu_screen_toggled == True:
        drawMenuScreenUI()

        if chart_showing == True:
            drawScoreChart()

        for event in pygame.event.get():
            #check if you've exited the game
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if chart_showing == True:
                    chart_showing = False
                elif getPlayerButtonColor() == True:
                    menu_screen_toggled = False

    # if the user has clicked one of the buttons then start game
    else:
        if firstTime == True:
            readHighScores()

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
                if archer_image >= 10:
                    drawing_bow = False
                    arrows_x.append(ARCHER_X + SHOT_OFFSET_X)
                    arrows_y.append(archer_y + SHOT_OFFSET_Y)
                else:
                    autoshoot = True

        screen.blit(BACKGROUND_IMAGE, (0,0))

        #game logic
        moveArcher()
        moveTarget()
        moveArrows()
        soundDelay()


        #have to cycle through the images before allowing the firing the arrow
        if drawing_bow == True:
            archer_image += 1 #this variable is used by the drawArcher function
            if archer_image >= 10 and autoshoot == True:
                drawing_bow = False
                arrows_x.append(ARCHER_X + SHOT_OFFSET_X)
                arrows_y.append(archer_y + SHOT_OFFSET_Y)
                autoshoot = False

        #drawing components
        highestScore = myfont.render('Best overall score: ' + str(BEST_OVERALL_SCORE),1, pygame.color.THECOLORS['black'])
        label = myfont.render("Score: " + str(score),1, pygame.color.THECOLORS['black'])
        highScoreLabel= myfont.render(str(playerLetter)+"'s "+'highscore: ' + str(BESTSCORE), 1, pygame.color.THECOLORS['black'])


        screen.blit(label, (180, 10))
        screen.blit(highScoreLabel, (300, 10))
        screen.blit(highestScore,(180,450))
        drawArcher()
        drawArrows()
        drawTarget()

        #handle collisions after updating dispay
        seeIfHitTarget()
        firstTime= False

    #update the display
    pygame.display.update()


pygame.quit()