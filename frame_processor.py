import cv2
import numpy as np
import imutils


 



def frame_resizer(frame, max_height=1000, max_width=None): 
    if max_width:
        resized_frame = imutils.resize(frame, width=max_width) 
    else: 
        resized_frame = imutils.resize(frame, height=max_height) 
    return resized_frame




 


