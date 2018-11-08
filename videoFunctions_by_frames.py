# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:19:19 2018

@author: jsuvilehto
"""
import cv2
import threading
import time

e = threading.Event()

def startrecording(fileloc,e):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #out = cv2.VideoWriter(fileloc,fourcc, 20.0, (640,480))
    font = cv2.FONT_HERSHEY_SIMPLEX
    while(cap.isOpened()):
        if e.is_set():
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            e.clear()
        ret, frame = cap.read()
        t = time.time()
        if ret==True:
            filename = fileloc + '_'+ str(int(round(t,2)*100)) + '.jpg'
            cv2.rectangle(frame,(280,470),(0,420),(0,0,0),-1)
            cv2.putText(frame, str(t), (0,450), font, 1, (255,255,255), 2)
            #out.write(frame)
            cv2.imwrite(filename, frame)
        else:
            break

def startRecordingProc(fileloc):
    global p
    p = threading.Thread(target=startrecording, args=(fileloc,e,))
    p.start()
    
# -------end video capture and stop tk
def stoprecording():
    e.set()
    p.join()
