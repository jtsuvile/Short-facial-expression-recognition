# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:07:49 2018

This file contains the helper functions to create four blocks from the face stimuli used in the Faces experiment

Each image will only be used once, each trial will contain one example of each level for each emotion, and the 
same actor is never shown twice in a row.

@author: jsuvilehto
"""
import numpy as np

def makeBlocks():
    emotionNames = ['Happy','Sad','Fear','Surprise']
    femaleActors = ['F3','F4','F5','F6']
    maleActors = ['M3','M4','M5','M6']
    if len(maleActors) >2 or len(femaleActors) > 2:
        # below, select 2 male and 2 female actors to use for this sub
        # not super pretty but works for piloting
        mtemp = [maleActors[i] for i in np.random.choice(len(maleActors), size=2, replace=False)]
        ftemp =  [femaleActors[i] for i in np.random.choice(len(maleActors), size=2, replace=False)]
        actorNames = mtemp + ftemp
    else:
        actorNames = femaleActors + maleActors
    levelNames = ['02','03','04','05','06']
    blocks =[[' '] * 20 for i in range(4)]
    levels = range(5)
    emoOrder = np.random.permutation(emotionNames)
    actorOrder = np.random.permutation(4)
    actorOrdered = [actorNames[i] for i in actorOrder]
    #allActors = np.tile(actorOrdered, 5)
    for counter in range(len(emotionNames)):
        for level in levels:
            runningNumber = counter*5+level
            for ind in range(4):
                blocks[ind][runningNumber] = actorOrdered[ind] +'_Neutral_'+ emoOrder[counter] + levelNames[level] + '.png'
            actorOrdered.insert(0, actorOrdered.pop())
    return blocks

# shuffle the order of stimuli so that we don't have any cases where the same actor is shown on two consequent trials

def permuteBlocks(blocks):
    permutedBlocks = [[' '] * 20 for i in range(4)]
    for num, block in enumerate(blocks):
        nRepeats = 1
        while nRepeats>0:
            perm = np.random.permutation(block)
            permStrip = [i.split('_', 1)[0] for i in perm]
            nRepeats = 0
            for i in range(len(permStrip)-1):
                if(permStrip[i] == permStrip[i+1]):
                    nRepeats+=1
            #print nRepeats
        permutedBlocks[num] = perm
    return permutedBlocks

def saveBlocks(permutedBlocks, subfolder):
    for n in range(4):
        filename = subfolder + 'block_'+str(n)+'.txt'
        with open(filename, 'wb') as outputfile:
            outputfile.writelines("%s;" % stimulus for stimulus in permutedBlocks[n])
        outputfile.close()
    return True