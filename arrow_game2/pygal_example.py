import pygal
import numpy as np
from pygal.style import Style, DarkColorizedStyle

import subprocess

SCORE_INCREMENT = 5

def scoreProgress(scores):
    progressAmount = 0
    scoresRead = []
    levels=[]
    median = 0
    for i in range(0, len(scores)):
        if scores[i] > median:
            progressAmount += SCORE_INCREMENT
        else:
            progressAmount -= SCORE_INCREMENT
        levels.append(progressAmount)
        scoresRead.append(scores[i])
        median = np.median(scoresRead)
        median = int(round(median))

    return levels

def returnScores():
    highscores_read = open('highscores.txt', 'r')
    file_lines=highscores_read.readlines()
    scoresA = []
    scoresB = []
    for line in file_lines:
        letterRemoved = line[1:]
        if line[0] == "A":
            scoresA.append(int(letterRemoved))
        elif line[0] == "B":
            scoresB.append(int(letterRemoved))
    return scoresA, scoresB




line_chart = pygal.Line(fill=True, style=DarkColorizedStyle)
line_chart.title = 'score increase'
num_scores = len(returnScores())
line_chart.x_labels = [num for num in range(num_scores+1)]


scoresA, scoresB =  returnScores()
Alevels = scoreProgress(scoresA)
Blevels = scoreProgress(scoresB)

line_chart.add('Sid', Alevels)
line_chart.add('player2', Blevels)

line_chart.render()
line_chart.render_to_file('line_chart.svg')
