# README

## Requirements
Install the following on whatever computer you want the code to run on:

1. Anaconda2 with Python 2.7 (all packages do not work with python 3)
2. Then, run the following in conda prompt (from https://github.com/lupyanlab/lab-computer/wiki/Install-psychopy-on-Anaconda-python)
 ```
 conda install numpy scipy matplotlib pandas pyopengl wxpython lxml openpyxl xlrd configobj pyyaml gevent pillow greenlet msgpack-python psutil pytables requests seaborn future 
 conda install --channel conda-forge pyglet opencv python-bidi json_tricks
 (pip install moviepy pyosf psychopy_ext <- maybe not necessary)
 conda install --channel cogsci pygame psychopy
 conda install msgpack-numpy
 ```
3. Make sure everything works!
4. Pull the code from the repository to a separate folder. The code folder should have 'stimuli' and 'subjects' subfolders

## Code organisation
* runExperiment.py : Actual experiment script. NB: Change 'scriptloc' to point to where you have saved the code
* randSamples.py : code needed to randomise Faces-stimuli to blocks. Stimulus file name structure is hardcoded in makeBlocks to conform to file name logic on 1/11/2018, might need to be changed when we get new actors
* trialFunctions.py : helper functions to create and run trials
* videoFunctions.py : helper functions to run video recording in separate thread
* video_to_stream.py : Andrey's code to analyse video after the fact

In case there is issues with videoFunctions.py after a switch was added to enable capture as video or frame by frame, you can also use backed up versions videoFunctions_as_video.py (to capture data as one continuous video) or videoFunctions_by_frames.py (to save video frame by frame in separate files). If you use one of these, remember to update your import statement to point to the correct file and the function call to omit the argument defining if we should capture video or separate files.

## Random stuff to keep in mind
* mouse tracking gets upset if mouse is not in the window area when code is started - not a problem if you work with a single screen but can be an issue with dual screen
* if you want to test code *with* video recording, set record = True at the beginning of runExperiment.py. If you want video to record .avi, set byFrames = False. If you want video to record a separate .jpg for each frame, set byFrames=True.
* python starts indexing from 0!
* Frame by frame video capture timestamp is 100*unix timestamp to retain exact timing while avoiding unnecessary dots in file names

## TODO
* select good example images and mask them the way actual stimulus images are
* try to get the code to shut down more nicely (might be windows 10 specific)
* get instruction texts from a separate text file (not necessarily trivial, psychopy does not seem to want to show newline character when reading from file. needs to be trouble shooted.)

