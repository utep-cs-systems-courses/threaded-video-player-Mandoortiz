#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from PCQueue import PCQueue

def extractFrames(fileName, extractionFrames, maxFramesToLoad=9999):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print(f'Reading frame {count} {success}')
    while success and count < maxFramesToLoad:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        extractionFrames.put(image)
       
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    print('Frame extraction complete')
    extractionFrames.markEnd()

def convertToGrayscale(extractionFrames, conversionFrames):
    count = 0
    success = True
    while True:
        print(f'Converting frame {count}')
        frame = extractionFrames.get()
        if frame == 'end':
            break
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        conversionQueue.put(grayscale)
        count+=1

    print('Frame conversion complete')
    conversionQueue.markEnd()
        
    
def displayFrames(inputBuffer):
    # initialize frame count
    count = 0
    success = True
    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frame = inputBuffer.get()
        if frame == 'end':
            break

        print(f'Displaying frame {count}')

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        
        count += 1

    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()

file_name = 'clip.mp4'
extractionQueue = PCQueue()
conversionQueue = PCQueue()

extractThread = threading.Thread(target = extractFrames, args = (file_name, extractionQueue))
conversionThread = threading.Thread(target = convertToGrayscale, args = (extractionQueue,conversionQueue))
displayThread = threading.Thread(target = displayFrames, args = (conversionQueue,))

extractThread.start()
conversionThread.start()
displayThread.start()
