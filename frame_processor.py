import os
import cv2
import numpy as np
import imutils


# make sure to enter sub_directory name if there is any
# if main_directory is not named "media_files", make sure to change that as well
# specify file_type to "mp4" or it will return all types of file
def read_files(*args, folder_name="media_files", file_type=None):
    
    # processes targated directory path
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, folder_name)
    if len(args) != 0:
        for arg in args:    
            directory_path = os.path.join(directory_path, arg)
    
    # reads files within targated directory
    all_files = []
    print("."*100)
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if file_type == None:
            all_files.append(file_path)
        # if file_type is specified 
        elif file_type != None:
            if file.split(".")[-1] == file_type:
                all_files.append(file_path)
                print(f"file '{file}' is of type '{file_type}'")
            else:
                print(f"file '{file}' not of type '{file_type}'")
    print("."*100)

    return all_files
#   returned a list of file_paths 




 
def load_video(video_path):
    capture = cv2.VideoCapture(video_path)
    return capture
 



def frame_resizer(frame, max_height=1000, max_width=None): 
    if max_width:
        resized_frame = imutils.resize(frame, width=max_width) 
    else: 
        resized_frame = imutils.resize(frame, height=max_height) 
    return resized_frame




 


def extract_transform(capture):
    transforms = []

    # this is just a way around of taking the first frame as the reference point for once
    # inside the while loop the frames will start from the second frame
    ret, previous_frame = capture.read()
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = frame_resizer(previous_frame_gray)

    while True:
        ret, current_frame = capture.read()
        if not ret:
            break
        

        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        current_frame_gray = frame_resizer(current_frame_gray)

        # cv2.goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance)
        previous_frame_points = cv2.goodFeaturesToTrack(previous_frame_gray, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3)

        # status gives an array of 1s and 0s 
        # based on successful tracing of a point from previous_frame_gray to current_frame_gray
        current_frame_points , status, err = cv2.calcOpticalFlowPyrLK(previous_frame_gray, current_frame_gray, previous_frame_points, None)

        # numpy magic to turn 1s into True
        #                 and 0s into false
        index = status == 1

        # skips coordinates with false value in status
        previous_frame_points = previous_frame_points[index]
        current_frame_points = current_frame_points[index]

        # # to visualize transform of points  
        # temp_frame = previous_frame_gray.copy()
        # for i in range(len(previous_frame_points)):
        #     x1, y1 = previous_frame_points[i].ravel()
        #     x2, y2 = current_frame_points[i].ravel()

        #     cv2.circle(temp_frame, (int(x2), int(y2)), 3, 255, -1)
        #     cv2.line(temp_frame, (int(x1), int(y1)), (int(x2), int(y2)), 255, 1)

        # cv2.imshow("corners", temp_frame)
        # cv2.waitKey(1)

        m , _ = cv2.estimateAffine2D(previous_frame_points, current_frame_points)
        # returned matrix form
        #     [a b tx]
        #     [c d ty]
        dx = m[0,2]
        dy = m[1,2]
        da = np.arctan2(m[1,0], m[0,0])
        
        transforms.append([dx, dy, da])

        previous_frame_gray = current_frame_gray


    # cv2.destroyAllWindows()
    capture.release()
    return np.array(transforms)
 




