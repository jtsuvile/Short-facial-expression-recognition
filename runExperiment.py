# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:44:03 2018

First version of experimental design related to Pathfinder project 2 

@author: jsuvilehto
"""

import sys
sys.path.append('C:\\Users\\jsuvilehto\\Desktop\\Faces\\')

import time
import os
import inspect
from psychopy import visual,event,core
import numpy as np
from trialFunctions import runFaceTrialPosNeg, generateFaceTrials, runTextTrial, generateTextTrials
from videoFunctions import startrecording, stoprecording, startRecordingProc

scriptloc='C:\\Users\\jsuvilehto\\Desktop\\Faces\\' #os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

subid = np.random.randint(100, 999)
directory = scriptloc + '\\subjects\\'+str(subid)
audio_loc = directory+'\\audio\\'
video_loc = directory+'\\video\\'
beh_loc = directory+'\\behavioural\\'
if not os.path.exists(directory):
    os.makedirs(directory)
    os.makedirs(audio_loc)
    os.makedirs(video_loc)
    os.makedirs(beh_loc)
    

timestr_text = time.strftime("%Y%m%d-%H_%M_%S")    
videoOutfile = video_loc+'sub_'+str(subid)#+'_'+'video_'+timestr_text+'.avi'
startRecordingProc(videoOutfile)

#dummy stimuli, will be replaced with PANAS
stimuliList = ['Upset','Hostile','Alert','Ashamed','Inspired','Nervous','Determined','Attentive','Afraid','Active']
textTrials = generateTextTrials(10, stimuliList) #these are not randomised!

#points to file with stimulus images, currently populated with dummy images
mainDir = scriptloc #os.path.dirname(os.path.realpath(__file__))
stimuliPath = mainDir + 'stimuli\\'
# at the moment just randomised from the contents of the folder, TODO: 
# block randomisation for 4 separate runs
blockDir = scriptloc + 'block_0.txt'
faceTrials = generateFaceTrials(blockDir, stimuliPath) 

# create the visual elements that are then modified to show stuff
win = visual.Window(
    size=[1000, 900],
    units="pix",
    fullscr=False,
    color = [0.079,0.079,0.079])

img = visual.ImageStim(win=win, mask=None,
                       interpolate=True, pos=(0,150))
instructions = visual.TextStim(
    win=win,
    wrapWidth=500,
    pos = (0,300),
    color = 'black')
fixation = visual.TextStim(win=win, pos=[0,150], text='+', height=200,
    color = 'black')
answerGuide = visual.TextStim(
    win=win,
    wrapWidth=500,
    pos = (0,-10),
    text = '<--- negative \t\t\t positive --->',
    color = 'black')
stimText = visual.TextStim(
    win=win,
    wrapWidth=500,
    pos = (0,150),
    color = 'black')
newTaskText = visual.TextStim(
    win=win,
    wrapWidth=500,
    pos = (0,250),
    color = 'black')

#cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object

# #
# Actual experiment part below
# #

# give the subject instructions for PANAS
newTaskText.setText('Welcome to this experiment.\n\nThe following task consists of a number of words that describe diferent feelings and emotions. Read each item and then indicate in the scale below to what extent you feel this way right now. \n\nPlease press any key to start')
newTaskText.draw()
win.flip()
event.waitKeys()
#
## make a text file to save data from text trials
timestr_text = time.strftime("%Y%m%d-%H_%M_%S")
textFileName = 'textResponses'
textDataFile = open(beh_loc+'sub_'+str(subid)+'_'+textFileName+'_'+timestr_text+'.csv', 'w')  # a simple text file with 'comma-separated-values'
textDataFile.write('stimulusWord,showOrder,response,timeStamp,timeToResponse\n')
##run text trials
for currTrial in textTrials:
    res = runTextTrial(currTrial, win, instructions, stimText)
    rating = (res['rating'] or -1) #returns -1 in case rating wasn't done within the specified time frame
    textDataFile.write('%s,%i,%i,%i,%.5f\n' %(res['stimText'], res['showOrder'], rating,res['startTime'], res['timeStamp']))
textDataFile.close()

# give the subject instructions for face rating task
newTaskText.setText('You are now starting a new task, where you will be asked to rate pictures. \n\nPress any key to continue')
newTaskText.draw()
win.flip()
event.waitKeys()
win.flip()

# practice answering to face trials
newTaskText.setText('If you think the mood of the person you see is negative (for example sad or angry), press \'f\' on your keyboard.\n\n Please press \'f\' now.')
newTaskText.draw()
answerGuide.draw()
win.flip()
event.waitKeys(keyList=['f'])
win.flip()

newTaskText.setText('If you think the mood of the person you see is positive (for example happy), press \'j\' on your keyboard.\n\n Please press \'j\' now.')
newTaskText.draw()
answerGuide.draw()
win.flip()
event.waitKeys(keyList=['j'])
win.flip()

fixation.draw()
instructions.setText(faceTrials[0]['promptText'])
instructions.draw()
answerGuide.draw()
win.flip()
core.wait(2)
win.flip()
# make a text file to save data from face trials
timestr_face = time.strftime("%Y%m%d-%H_%M_%S")
faceFileName = 'faceResponses'
faceDataFile = open(beh_loc+'sub_'+str(subid)+'_'+faceFileName+'_'+timestr_face+'.csv', 'w')  # a simple text file with 'comma-separated-values'
faceDataFile.write('stimFile,showOrder,response,startTime,timeToResponse\n')
#run face trials
for currTrial in faceTrials:
    startTime = time.time()
    res = runFaceTrialPosNeg(currTrial, win, img, instructions, answerGuide, fixation)
    rating = (res['rating'] or 0) #returns 0 in case rating wasn't done within the specified time frame
    faceDataFile.write('%s,%i,%i,%i,%.5f\n' %(res['stimFile'], res['showOrder'], rating,res['startTime'], res['timeStamp']))
faceDataFile.close()

thankYouText = visual.TextStim(
        win=win,
        wrapWidth=500,
        pos = (0,250),
        text='Thank you subject ' + str(subid) + ',\nyou have now completed the whole experiment. \n\nPress any key to close this window.',
        height = 30,
        color = 'black')

thankYouText.draw()
win.flip()
event.waitKeys()

stoprecording()
win.close()
core.quit()
print('Done')