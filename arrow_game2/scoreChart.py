import pygal
import numpy as np

from pygal.style import Style, DarkColorizedStyle

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image

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



# aesthetics
line_chart = pygal.Line(fill=True, style=DarkColorizedStyle)
line_chart.title = 'score increase'


#returning scores
scoresA, scoresB =  returnScores()
Alevels = scoreProgress(scoresA)
Blevels = scoreProgress(scoresB)

# displaying chart
num_scores = max(len(Alevels),len(Blevels))
line_chart.x_labels = [num for num in range(num_scores+1)]

line_chart.add('player A', Alevels)
line_chart.add('player B', Blevels)

#rendering chart
line_chart.render()
line_chart.render_to_file('line_chart.svg')

drawing = svg2rlg("line_chart.svg")

#improving resolution
sx = sy = 10
drawing.width, drawing.height = drawing.minWidth() * sx, drawing.height * sy
drawing.scale(sx, sy)

renderPM.drawToFile(drawing, "line_chart.png", fmt="PNG")
#img = Image.open("line_chart.png")
#img.show()