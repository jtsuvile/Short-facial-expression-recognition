# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:34:35 2018

@author: jsuvilehto
"""
from psychopy import visual,event,core
import os
import numpy as np

def runFaceTrial(currTrial, win, img, instructions):
    for key in event.getKeys():
        if key in ['escape']:
            core.quit() # quit if they press escape
            win.close()
    print(currTrial)
    win.flip()
    instructions.setText(currTrial['promptText'])
    img.setImage(currTrial['trialImage'])
    ratingScale = visual.RatingScale(win, low=1, high=7, pos=(0,-50), showAccept = False, singleClick = True,size=1.5, textSize=0.5, tickHeight = 0.5,  
                                     acceptKeys='return', acceptSize=1.0, scale=' ', markerColor ='Yellow', labels=['negative','positive'])
    win.flip()
    clock = core.Clock()
    while ratingScale.noResponse and clock.getTime() <= 10.0:
        img.draw()
        instructions.draw()
        ratingScale.draw()
        win.flip()
        if ratingScale.noResponse:
            rating = None
        else:
            rating = ratingScale.getRating()
        decisionTime = ratingScale.getRT()
        choiceHistory = ratingScale.getHistory()
    fullRating = {'stimFile':currTrial['trialImage'],'showOrder': currTrial['trialIndex'],'rating': rating, 'timeStamp':decisionTime, 'choiceHistory':choiceHistory}
    return fullRating

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
    stimulusTime = core.getAbsTime()
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

def runFaceTrialPosNeg(currTrial, win, img, instructions, answerGuide, fixation):
    for key in event.getKeys():
        if key in ['escape']:
            core.quit() # quit if they press escape
            win.close()
    #print(currTrial)
    instructions.setText(currTrial['promptText'])
    event.clearEvents()
    win.flip()
    instructions.draw()
    answerGuide.draw()
    RT = core.Clock() 
    img.setImage(currTrial['trialImage'])
    img.draw()
    win.flip()
    stimulusTime = core.getAbsTime()
    RT.reset()
    core.wait(0.5)
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
            print(thisKey)
            if thisKey[0]=='f':
                thisResp = -1            # negative
                reactionTime = thisKey[1]
            elif thisKey[0]=='j':
                thisResp = 1             # positive
                reactionTime = thisKey[1]
            elif thisKey[0] in ['q', 'escape']:
                core.quit()  # abort experiment
    fullRating = {'stimFile':currTrial['trialImage'],'showOrder': currTrial['trialIndex'],'rating': thisResp, 'startTime': stimulusTime, 'timeStamp':reactionTime}
    print(fullRating)
    return fullRating