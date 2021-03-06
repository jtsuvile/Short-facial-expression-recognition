# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:34:35 2018

@author: jsuvilehto
"""
from psychopy import visual,event,core
import os
import time
import numpy as np
from randSamples import makeBlocks, permuteBlocks, saveBlocks

def getMouse(mouse, recordedMouse):
    currPos, posDelta = mouse.getPositionAndDelta()
    currButtons = mouse.getCurrentButtonStates()
    timestamp = time.time()
    mouseStatus = [timestamp, currPos[0], currPos[1], posDelta[0], posDelta[1], currButtons[0], currButtons[1], currButtons[2]]
    recordedMouse.append(mouseStatus)
    return 

def generateFaceTrials(blockDir, stimuliPath):
    trials = []
#    stimuli = [f for f in os.listdir(stimuliPath) if os.path.isfile(os.path.join(stimuliPath, f))]
#    trialsOrder = np.random.choice(len(stimuli), numTrials, replace=False)  
    f = open(blockDir,"r")
    stimuli = f.read()
    f.close()
    trialsOrder = stimuli.split(';')
    trialsOrder.pop()
    trialInd = 0   
    for trial in trialsOrder:
        trials.append({
                'trialIndex': trialInd,
                'trialImage': stimuliPath+trial,
                'promptText' :  "How do you think this person feels"
                })
        trialInd+=1
    return trials

def generateTextTrials(numTrials, stimuliList):
    trials = []
    trialsOrder = range(0,numTrials)   
    trialInd = 0    
    for trial in trialsOrder:
        trials.append({
                'trialIndex': trialInd,
                'stimulusText': stimuliList[trial],
                'promptText' :  "Please indicate in the scale below to what extent you feel this way right now"
                })
        trialInd+=1
    return trials

def runTextTrial(currTrial, win, instructions, stimText):  
    for key in event.getKeys():
        if key in ['escape']:
            core.quit() # quit if they press escape
            win.close()
    print(currTrial)
    win.flip()
    instructions.setText(currTrial['promptText'])
    stimText.setText(currTrial['stimulusText'])
    stimText.setHeight(100)
    ratingScale = visual.RatingScale(win, low=1, high=5, pos=(0,-50), showAccept = False, singleClick = True, size=1.5, textSize=0.5, tickHeight = 0.5, 
                                     acceptKeys='return', scale=' ', markerColor='green', labels=['not at all','very much'], textColor='black', lineColor='black')
    
    win.flip()
    stimulusTime = time.time()
    clock = core.Clock()
    while ratingScale.noResponse and clock.getTime() <= 10.0:
        stimText.draw()
        instructions.draw()
        ratingScale.draw()
        win.flip()
        if ratingScale.noResponse:
            rating = None
        else:
            rating = ratingScale.getRating()
        decisionTime = ratingScale.getRT()
        choiceHistory = ratingScale.getHistory()
    fullRating = {'stimText':currTrial['stimulusText'],'showOrder': currTrial['trialIndex'],'rating': rating, 'startTime': stimulusTime, 'timeStamp':decisionTime, 'choiceHistory':choiceHistory}
    return fullRating

def runFaceTrialPosNeg(currTrial, win, img, instructions, answerGuide, fixation, posNegDir):
    #print(currTrial)
    instructions.setText(currTrial['promptText'])
    #event.clearEvents()
    fixation.draw()
    instructions.draw()
    answerGuide.draw()
    win.flip()
    core.wait(0.8) # fixation cross before image
    event.clearEvents()
    instructions.draw()
    answerGuide.draw()
    RT = core.Clock()
    img.setImage(currTrial['trialImage'])
    img.draw()
    win.flip()
    stimulusTime = time.time()
    RT.reset()
    core.wait(0.5) # time to show stimfulus
    fixation.draw()
    instructions.draw()
    answerGuide.draw()
    win.flip()
    thisResp=0
    reactionTime = 10
    clock = core.Clock()
    while thisResp==0 and clock.getTime() <= 10.0:
        allKeys=event.getKeys(keyList=['f','j','q'],timeStamped=RT)
        for thisKey in allKeys:
            reactionTime = thisKey[1]
            if thisKey[0]=='f':
                if posNegDir < 0.5:
                    thisResp = -1            # negative
                else: # reverse coding
                    thisResp = 2            # positive, reverse coding
            elif thisKey[0]=='j':
                if posNegDir < 0.5:
                    thisResp = 1            # positive, normal direction
                else: 
                    thisResp = -2           # negative, reverse coding
            elif thisKey[0] in ['q', 'escape']:
                win.close()
                core.quit()
    fullRating = {'stimFile':currTrial['trialImage'],'showOrder': currTrial['trialIndex'], 'rating': thisResp, 'startTime': stimulusTime,'reactionTime': reactionTime}
    print(fullRating)
    return fullRating

def initSub(mainDir):
    ##
    # Generate subid and create necessary folders
    ##
    subid = np.random.randint(1000, 9999)
    while os.path.exists(mainDir + '\\subjects\\'+str(subid)):
        subid = np.random.randint(1000, 9999)
    directory = mainDir + '\\subjects\\'+str(subid)
    # video_loc = directory+'\\video\\'
    beh_loc = directory+'\\behavioural\\'
    os.makedirs(directory)
    #os.makedirs(video_loc)
    os.makedirs(beh_loc)
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
    return subid, textTrials, faceTrials