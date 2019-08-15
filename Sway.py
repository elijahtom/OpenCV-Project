import numpy as np
import cv2
import statistics

vid = cv2.VideoCapture("reactor.mpg")

if(not vid.isOpened()):
    print("Error: Could not load video file")
    exit()

stream, frame = vid.read()
h = frame.shape[0]
w = frame.shape[1]
sway_coords = []

while(vid.isOpened()):
    if(stream):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for i in range(100,150): #approximate pixel range for the tracked feature
            if(frame[int((h/2)),i] > 103): # tracks the left edge of the reactor core
               sway_coords.append(i)                                            
               break #done parsing through this frame
    else:
        break
    stream, frame = vid.read()
    if(len(sway_coords) > 1000): #stops at the 1000th frame for brevity
        break

with open("sway.txt", "w") as txt_file: #saves to a text file for further analysis
    for j in range(0,len(sway_coords)):
            txt_file.write(str((sway_coords[j])) + '\n')



