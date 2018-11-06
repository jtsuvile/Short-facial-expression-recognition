# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:44:03 2018

First version of experimental design related to Pathfinder project 2 

@author: jsuvilehto
"""

# Change this to True when you want to run video recording, e.g. when really collecting subjects
# Keeping it at false helps when you work on the code with computers with no webcam or cv2 package
record = False

import sys
sys.path.append('C:\\Projects\\Faces\\')

import time
import os
#import inspect
from psychopy import visual,event,core, iohub
import numpy as np
from trialFunctions import runFaceTrialPosNeg, generateFaceTrials, runTextTrial, generateTextTrials
if record:
    from videoFunctions import startrecording, stoprecording, startRecordingProc
from randSamples import makeBlocks, permuteBlocks, saveBlocks

scriptloc= 'C:\\Projects\\Faces\\' #os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
mainDir = scriptloc #os.path.dirname(os.path.realpath(__file__))

subid = np.random.randint(100, 999)
directory = scriptloc + '\\subjects\\'+str(subid)
video_loc = directory+'\\video\\'
beh_loc = directory+'\\behavioural\\'
if not os.path.exists(directory):
    os.makedirs(directory)
    os.makedirs(video_loc)
    os.makedirs(beh_loc)

# instructions are set here - you can find from the code where each gets called.
# todo: move instructions to a separate text file (not necessarily trivial, psychopy does not seem to want to show newline character when reading from file)
instrTexts = ['You will soon start a new task where you are asked to evaluate facial expressions from photographs. \n\nThe faces will be presented in the centre of the screen and they will appear for about half a second only. For each face decide whether the expression on the face is a negative or a positive one. You may feel like you are guessing, and there are no right or wrong answers. Just answer as quickly as you can according to your gut reaction. \n\nThe next face will be presented after you have responded to the previous one or at the latest after 10 seconds since you saw the previous face. There will be a short practice first where your responses will not be scored and I will tell you when the real task starts. \n\nPlease press any key to continue.', 
              'Please place your hands on the keyboard so that your right index finger is on the \'j\' key and your left index finger is on the \'f\' key. \n\nPlease press  \'j\' or \'f\' to continue.',
              'If you think the mood of the person you see is negative, press \'f\' on your keyboard.',
              'If you think the mood of the person you see is positive, press \'j\' on your keyboard.',
              'Next, you will start the actual experiment. Some of the facial expressions might be very subtle. \n\nRemember, you may feel like you are guessing, and there are no right or wrong answers. Just answer as quickly as you can according to your gut reaction. \n\nPlease press  \'j\' or \'f\' to start the actual task.',
              'Please press  \'j\' or \'f\' to continue the task.',
              'Thank you subject ' + str(subid) + ',\nyou have now completed the whole experiment. \n\nPress any key to close this window.']

exampleImages = [scriptloc + '\\happy_example.jpg',
                 scriptloc + '\\sad_example.jpg']

# use iohub and keyboard to capture key press events
io = iohub.launchHubServer()
keyboard = io.devices.keyboard

##
# Create all the tasks that will be shown to the subjects 
## 

# Make text based trials from PANAS words
stimuliList = ['Upset','Hostile','Alert','Ashamed','Inspired','Nervous','Determined','Attentive','Afraid','Active']
textTrials = generateTextTrials(10, stimuliList) #these are not randomised!

# Make face trials and randomise them to blocks
stimuliPath = mainDir + 'stimuli\\'
myBlocks = makeBlocks()
myPermuted = permuteBlocks(myBlocks)
#todo : add error handling
if saveBlocks(myPermuted, directory + '\\'):
    print 'successfully saved trial blocks for subject ' + str(subid)
faceTrials = []
for nBlock in range(4):
    blockDir = directory + '\\block_' + str(nBlock) +'.txt'
    faceTrials.append(generateFaceTrials(blockDir, stimuliPath))

##    
# Create the visual elements used in the experiment
# these are later modified to show different texts, instructions and stimuli
##
    
win = visual.Window(
    size=[1000, 900],
    units="pix",
    fullscr=True,
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

##
# Run the actual experiment
##

#Todo: add notification of video recording


if record:
    timestr_text = time.strftime("%Y%m%d-%H_%M_%S")    
    videoOutfile = video_loc+'sub_'+str(subid)#+'_'+'video_'+timestr_text+'.avi'
    startRecordingProc(videoOutfile)

## give the subject instructions for PANAS
#newTaskText.setText('Welcome to this experiment.\n\nThe following task consists of a number of words that describe diferent feelings and emotions. Read each item and then indicate in the scale below to what extent you feel this way right now. \n\nPlease press any key to start')
#newTaskText.draw()
#win.flip()
#event.waitKeys()
##
### make a text file to save data from text trials
#timestr_text = time.strftime("%Y%m%d-%H_%M_%S")
#textFileName = 'textResponses'
#textDataFile = open(beh_loc+'sub_'+str(subid)+'_'+textFileName+'_'+timestr_text+'.csv', 'w')  # a simple text file with 'comma-separated-values'
#textDataFile.write('stimulusWord,showOrder,response,timeStamp,timeToResponse\n')
###run text trials
#for currTrial in textTrials:
#    res = runTextTrial(currTrial, win, instructions, stimText)
#    rating = (res['rating'] or -1) #returns -1 in case rating wasn't done within the specified time frame
#    textDataFile.write('%s,%i,%i,%i,%.5f\n' %(res['stimText'], res['showOrder'], rating,res['startTime'], res['timeStamp']))
#textDataFile.close()

# give the subject instructions for face rating task
# the instructions for faces are so long we need to shift the position of the text
newTaskText.setPos((0,50))
newTaskText.setText(instrTexts[0])
newTaskText.draw()
win.flip()
keyboard.waitForKeys(clear=True, etype=keyboard.KEY_RELEASE)
print keyboard.state 
win.flip()

# moving text back after the long instructions
newTaskText.setPos((0,300))

#show instructions for faces-task plus example images to practice
for i in range(len(exampleImages)+1):
    newTaskText.setText(instrTexts[i+1])
    newTaskText.draw()
    if i is not 0:
        answerGuide.draw()
        img.setImage(exampleImages[i-1])
        img.draw()
    win.flip()
    key = keyboard.waitForKeys(keys=['f','j'],clear=True, etype=keyboard.KEY_RELEASE)
    print('got key press at ' + str(key[0].time))
    print keyboard.state 
    win.flip()

# make a text file to save data from face trials
timestr_face = time.strftime("%Y%m%d-%H_%M_%S")
faceFileName = 'faceResponses'
faceDataFile = open(beh_loc+'sub_'+str(subid)+'_'+faceFileName+'_'+timestr_face+'.csv', 'w')  # a simple text file with 'comma-separated-values'
faceDataFile.write('stimFile,block,showOrder,response,startTime,startTimeKeyStyle,keydownTime,keyupTime\n')
#run face trials
for n, trialBlock in enumerate(faceTrials):
    if n == 0:
        newTaskText.setText(instrTexts[4])
    else:
        newTaskText.setText(instrTexts[5])
    newTaskText.draw()
    win.flip()
    event.waitKeys(keyList=['f','j'])
    win.flip()
    for currTrial in trialBlock:
        startTime = time.time()
        res = runFaceTrialPosNeg(currTrial, win, img, instructions, answerGuide, fixation, keyboard)
        rating = (res['rating'] or 0) #returns 0 in case rating wasn't done within the specified time frame
        faceDataFile.write('%s,%i,%i,%i,%.5f,%.5f,%.5f,%.5f\n' %(res['stimFile'], n, res['showOrder'], rating ,res['startTime'],res['startTime2'], res['keydown'],res['keyup']))
faceDataFile.close()

newTaskText.setText(instrTexts[-1])
newTaskText.draw()
win.flip()
keyboard.waitForKeys(clear=True, etype=keyboard.KEY_RELEASE)

if record:
    stoprecording()

io.quit()
win.close()
core.quit()
print('Done')