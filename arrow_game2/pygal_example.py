import pygal
import numpy as np
from pygal.style import Style, DarkColorizedStyle

import subprocess

SCORE_INCREMENT = 5

def scoreProgress():
    progressAmount = 0
    pastScores =  returnScores()
    scoresRead = []
    levels=[]
    median = 0
    for i in range(0, len(pastScores)):
        if pastScores[i] > median:
            progressAmount += SCORE_INCREMENT
        else:
            progressAmount -= SCORE_INCREMENT
        levels.append(progressAmount)
        scoresRead.append(pastScores[i])
        median = np.median(scoresRead)
        median = int(round(median))

    return levels


'''def readHighScores():
    global BESTSCORE,highscores_read
    file_lines=highscores_read.readlines()
    scores = [1,2,3,4,5]
    for line in file_lines:
        scores.append(int(line))
    BESTSCORE = max(scores)'''

def returnScores():
    highscores_read = open('highscores.txt', 'r')
    file_lines = highscores_read.readlines()
    scores = []
    for line in file_lines:
        scores.append(int(line))
    return scores


'''line_chart = pygal.Line(fill=True, style=DarkColorizedStyle)
line_chart.title = 'score increase'
num_scores = 19
line_chart.x_labels = [num for num in range(num_scores+1)]
scores = returnScores()
line_chart.add('Sid', scores)
line_chart.render()
line_chart.render_to_file('line_chart.svg')'''

line_chart = pygal.Line(fill=True, style=DarkColorizedStyle)
line_chart.title = 'score increase'
num_scores = len(returnScores())
line_chart.x_labels = [num for num in range(num_scores+1)]
levels = scoreProgress()
line_chart.add('Sid', levels)
line_chart.render()
line_chart.render_to_file('line_chart.svg')
