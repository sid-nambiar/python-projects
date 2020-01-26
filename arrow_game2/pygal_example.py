import pygal

import subprocess

def readHighScores():
    global BESTSCORE
    highscores_read = open('highscores.txt', 'r')
    file_lines=highscores_read.readlines()
    scores = []
    for line in file_lines:
        scores.append(int(line))
    BESTSCORE = max(scores)

def returnScores():
    highscores_read = open('highscores.txt', 'r')
    file_lines = highscores_read.readlines()
    scores = []
    for line in file_lines:
        scores.append(int(line))
    return scores

line_chart = pygal.Line()
line_chart.title = 'Browser usage evolution (in %)'
num_scores = 15
line_chart.x_labels = [num for num in range(num_scores+1)]
scores = returnScores()
line_chart.add('Sid', scores)
line_chart.render()
line_chart.render_to_file('line_chart.svg')

readHighScores()