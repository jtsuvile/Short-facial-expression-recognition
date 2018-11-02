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
    actorNames = ['F1','F2','M1','M2']
    levelNames = ['02','03','04','05','06']
    #def makeSamples():
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
                blocks[ind][runningNumber] = actorOrdered[ind] +'_Neutral_'+ emoOrder[counter] + levelNames[level] + '.jpg'
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