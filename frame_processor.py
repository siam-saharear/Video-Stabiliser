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
 



