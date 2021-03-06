# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:44:03 2018

First version of experimental design related to Pathfinder project 2 

@author: jsuvilehto
"""

# Change this to True when you want to run video recording, e.g. when really collecting subjects
# Keeping it at false helps when you work on the code with computers with no webcam or cv2 package
record = False
byFrames = False

# change this to point to the folder where you keep the code
scriptloc= 'C:\\Projects\\Faces\\' #os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

import sys
sys.path.append(scriptloc)
import time
#import os
#import inspect
from psychopy import visual, event, core
import numpy as np
from trialFunctions import runFaceTrialPosNeg, runTextTrial, initSub
if record:
    from videoFunctions import stoprecording, startRecordingProc

mainDir = scriptloc 
subid, textTrials, faceTrials = initSub(mainDir)

video_loc = mainDir + '\\subjects\\'+str(subid) + '\\video\\'
beh_loc = mainDir + '\\subjects\\'+str(subid) + '\\behavioural\\'

# instructions are set here - you can find from the code where each gets called.
instrTexts = {'expstart' : "Thank you for participating in this study. \n\nThe video recording will start as soon as the experiment starts. Please press any key to start the experiment and the video recording.",
              'panasstart': 'The following task consists of a number of words that describe diferent feelings and emotions. Read each item and then indicate in the scale below to what extent you feel this way right now. \n\nPlease press any key to start',
              'facestart': 'You will soon start a new task where you are asked to evaluate facial expressions from photographs. \n\nThe faces will be presented in the centre of the screen and they will appear for about half a second only. For each face decide whether the expression on the face is a negative or a positive one. You may feel like you are guessing, and there are no right or wrong answers. Just answer as quickly as you can according to your gut reaction. \n\nThe next face will be presented after you have responded to the previous one or at the latest after 10 seconds since you saw the previous face. There will be a short practice first where your responses will not be scored and I will tell you when the real task starts. \n\nPlease press any key to continue.', 
              'faceinstr': 'Please place your hands on the keyboard so that your right index finger is on the \'j\' key and your left index finger is on the \'f\' key. \n\nPlease press  \'j\' or \'f\' to continue.',
              'posneginstr': 'If you think the mood of the person you see is negative, press \'f\' on your keyboard. If you think the mood of the person you see is positive, press \'j\' on your keyboard.',
              'posneginstrreverse': 'If you think the mood of the person you see is negative, press \'j\' on your keyboard. If you think the mood of the person you see is positive, press \'f\' on your keyboard.',
              'posnegarrows': '<--- negative \t\t\t positive --->',
              'posnegarrowsreverse': '<--- positive \t\t\t negative --->',
              'blockbegin': 'Next, you will start the actual experiment. Some of the facial expressions might be very subtle. \n\nRemember, you may feel like you are guessing, and there are no right or wrong answers. Just answer as quickly as you can according to your gut reaction. \n\nPlease press  \'j\' or \'f\' to start the actual task.',
              'blockbreak': 'Please press  \'j\' or \'f\' to continue the task.',
              'thankyou': 'Thank you subject ' + str(subid) + ',\nyou have now completed the whole experiment. \n\nPress any key to close this window.'}


exampleImages = [scriptloc + '\\example_images\\sad_example.JPG',
        scriptloc + '\\example_images\\happy_example.JPG',
        scriptloc + '\\example_images\\fear_example.JPG',
        scriptloc + '\\example_images\\surprise_example.JPG']


# randomise direction of pos/neg in faces
posNegDir = np.random.random() 
if (posNegDir <0.5):
    thisSubPosNegText = instrTexts['posneginstr']
    thisSubPosNegArrows = instrTexts['posnegarrows']
else:
    thisSubPosNegText = instrTexts['posneginstrreverse']
    thisSubPosNegArrows = instrTexts['posnegarrowsreverse']
##    
# Create the visual elements used in the experiment
# these are later modified to show different texts, instructions and stimuli
# 
# Karen! Change these when playing with fonts etc
##

generalTextSize = 30
generalWrapWidth = 850

win = visual.Window(
    size=[1000, 900],
    units="pix",
    fullscr=True,
    #color = [0.079,0.079,0.079]
    color = [0.4,0.4,0.4])

img = visual.ImageStim(win=win, mask=None,
                       interpolate=True, pos=(0,50))

fixation = visual.TextStim(win=win, pos=[0,50], text='+', height=150,
    color = 'black')

instructions = visual.TextStim(
    win=win,
    height = generalTextSize,
    wrapWidth=generalWrapWidth,
    pos = (0,300),
    color = 'black')

answerGuide = visual.TextStim(
    win=win,
    height = generalTextSize,
    wrapWidth=generalWrapWidth,
    pos = (0,-200),
    text = thisSubPosNegArrows,
    color = 'black')

stimText = visual.TextStim(
    win=win,
    wrapWidth=generalWrapWidth,
    pos = (0,180),
    height=5,
    color = 'black')

newTaskText = visual.TextStim(
    height = generalTextSize,
    win=win,
    wrapWidth=generalWrapWidth,
    pos = (0,350),
    color = 'black')

##
# Run the actual experiment
##
# Display welcome and warning about recording
newTaskText.setText(instrTexts['expstart'])
newTaskText.draw()
win.flip()
event.waitKeys()

#if running video, start recording after keyboard input (above)
if record:  
    videoOutfile = video_loc+'sub_'+str(subid)
    startRecordingProc(videoOutfile, byFrames)

# give the subject instructions for PANAS
newTaskText.setText(instrTexts['panasstart'])
newTaskText.draw()
win.flip()
event.waitKeys()

## make a text file to save data from text trials
timestr_text = time.strftime("%Y%m%d-%H_%M_%S")
textFileName = 'textResponses'

# make text files for outputting responses, name the columns
textDataFile = open(beh_loc+'sub_'+str(subid)+'_'+textFileName+'_'+timestr_text+'.csv', 'w')  
textDataFile.write('stimulusWord,showOrder,response,stimulusTimeStamp,timeToResponse\n')
##run text trials
for currTrial in textTrials:
    #mouseRecord = []
    res = runTextTrial(currTrial, win, instructions, stimText)
    rating = (res['rating'] or -1) #returns -1 in case rating wasn't done within the specified time frame
    textDataFile.write('%s,%i,%i,%.5f,%.5f\n' %(res['stimText'], res['showOrder'], rating,res['startTime'], res['timeStamp']))
    #mousePosFile.writelines('%.5f,%i,%i,%i,%i,%s,%s,%s\n' % (mousePos[0], mousePos[1], mousePos[2], mousePos[3], mousePos[4], mousePos[5], mousePos[6], mousePos[7]) for mousePos in mouseRecord)
textDataFile.close()


## give the subject instructions for face rating task
## the instructions for faces are so long we need to shift the position of the text
newTaskText.setPos((0,50))
newTaskText.setText(instrTexts['facestart'])
newTaskText.draw()
win.flip()
event.waitKeys()
win.flip()
# moving text back after the long instructions
newTaskText.setPos((0,300))
img.setPos((0,30))
#win.flip()
#event.waitKeys()
#show instructions for faces-task plus example images to practice
faceTestDataFile = open(beh_loc+'sub_'+str(subid)+'_timestamps_for_face_tests.csv', 'w')  # a simple text file with 'comma-separated-values'
faceTestDataFile.write('stimFile,imageShowTime,key\n')
for i in range(len(exampleImages)+1):
    if i==0:
        newTaskText.setText(instrTexts['faceinstr'])
        newTaskText.draw()
        win.flip()
        event.waitKeys(keyList=['f','j','q'])
    else:
        event.clearEvents()
        newTaskText.setText(thisSubPosNegText)
        newTaskText.draw()
        answerGuide.draw()
        testImageTime = time.time()
        img.setImage(exampleImages[i-1])
        img.draw()
        win.flip()
        respKey = event.waitKeys(keyList=['f','j','q'])
        faceTestDataFile.write('%s,%.5f,%s\n' %(exampleImages[i-1], testImageTime, respKey[0]))
    win.flip()
faceTestDataFile.close()

#revert back to regular positioning of stimulus image
img.setPos((0,50))
# make a text file to save data from face trials
timestr_face = time.strftime("%Y%m%d-%H_%M_%S")
faceFileName = 'faceResponses'
faceDataFile = open(beh_loc+'sub_'+str(subid)+'_'+faceFileName+'_'+timestr_face+'.csv', 'w')  # a simple text file with 'comma-separated-values'
faceDataFile.write('stimFile,block,showOrder,response,startTime,timeToResponse\n')
#run face trials
for n, trialBlock in enumerate(faceTrials):
    if n == 0:
        newTaskText.setText(instrTexts['blockbegin'])
    else:
        newTaskText.setText(instrTexts['blockbreak'])
    newTaskText.draw()
    win.flip()
    event.waitKeys(keyList=['f','j'])
    win.flip()
    for currTrial in trialBlock:
        startTime = time.time()
        res = runFaceTrialPosNeg(currTrial, win, img, instructions, answerGuide, fixation, posNegDir)
        rating = (res['rating'] or 0) #returns 0 in case rating wasn't done within the specified time frame
        faceDataFile.write('%s,%i,%i,%i,%.5f,%.5f\n' %(res['stimFile'], n, res['showOrder'], rating ,res['startTime'],res['reactionTime']))
faceDataFile.close()

newTaskText.setText(instrTexts['thankyou'])
newTaskText.draw()
win.flip()
event.waitKeys()
if record:
    stoprecording()

win.close()
core.quit()
    
print('Done')