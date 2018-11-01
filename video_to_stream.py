import cv2
import os
import io
import sys
from io import BytesIO
import glob
import requests

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from PIL import Image

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 200)

# global default vars to use the MS service
SUBSCRIPTION_KEY = "4b9224f7d3e1447db4bcf5c75e63db3f"
assert SUBSCRIPTION_KEY

# face_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/detect'
FACE_MSF_API_URL = "https://uksouth.api.cognitive.microsoft.com/face/v1.0/detect"

# headers
FACE_MSF_API_HEADERS  = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY, 
                         "Content-Type": "application/octet-stream" }

FACE_MSF_API_PARAMS = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}



def video_to_emostream(path_to_video, path_out='output_frames', 
                        face_recognition_url = FACE_MSF_API_URL, 
                        face_recognition_header = FACE_MSF_API_HEADERS,
                        face_recognition_params = FACE_MSF_API_PARAMS, 
                        save_frames_to_disk=False, 
                        subsampled_frame=None):
    
    """
    
    - Extract frames from video and applies Microsoft Face Recognition API to extract emotions.
    - The default subsampling is to output 5 frames: [0, 25, 0.5, 0.75, 1.0] (every 25%)
    - This code makes a very important assumption, that a face is aligned with largest dimension
    
    
    INPUT VARS:
    
    - path_to_video: specify a path on a disk to the video you want to convert to emo stream
    - path_out: specify a path to save the extracted frames
    - {face_recognition_url, 
       face_recognition_header,
       face_recognition_params} : standard parameters to work with the MSF Face service
       
    - save_frames_to_disk: save file to disk or not
    - subsampled_frame: subsampling ratio
        
        
    OUTPUT VARS:
    
    - frames            :  a list with frames in numpy.array() format
    - emo_vector        :  a list of emotion attributes extracted from the return JSON file from MSF service
    - faces_vector      :  a list with JSON outputs as returned from the MSF service
    - frame_ids         :  a list of frames used in the analysis (extracted frames)
    - Pandas dataframe with the indexed emotions from frames
        
    """
    
   
    if save_frames_to_disk:
        try:
            # Create target directory
            os.mkdir(path_out)
            print "Directory " + path_out +  " created " 
        except FileExistsError:
            print "Directory " + path_out +  " already exists"
    
    cap = cv2.VideoCapture(path_to_video)
    
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print('Video length: ', video_length, ' frames.')
    
    frames = []
    faces_vector = []
    emo_vector = []
    
    if cap.isOpened() and video_length > 0:
        if subsampled_frame is None:
            frame_ids = [0]
            # default subsampling
            if video_length >= 4:
                frame_ids = [0, 
                             round(video_length * 0.25), 
                             round(video_length * 0.5),
                             round(video_length * 0.75),
                             video_length - 1]
        else:
            frame_ids = range(video_length)[::30]

        print 'frame_ids: ' +str(frame_ids)
        count = 0
        
        success, image_i = cap.read()
        # 'image_i' is in np.array() format !
        
        # if there is an image, then go on
        while success:
            # if 'count' in the specified index, then extract emotions, if not -> skip
            if count in frame_ids:
                # make sure the image is in a portrait mode (a face is aligned with the larges dimention)
                #if image_i.shape[1] > image_i.shape[0]:
                #    image_i = np.swapaxes(image_i, 0,1)
                    

                # collect a frame and add to the list of frames
                frames.append(image_i)

                # convert np.array() into 'jpg' binary string format,
                # save into the buffer ('buf')
                # to send to the MSF service
                
                buf = io.BytesIO()
                plt.imsave(buf, image_i, format='jpg')
                

                # send  a frame to MSF
                print 'making request to MSF...'
                response = requests.post(face_recognition_url, 
                                         params=face_recognition_params, 
                                         headers=face_recognition_header, 
                                         data=buf.getvalue())
                
                # store the returned data in JSON format
                faces = response.json()
                buf.close()
                if len(faces) == 0:
                    print('ERROR: faces are empty!')
                else:
                    print('...success')

                faces_vector.append(faces)
                emo_vector.append(faces[0]['faceAttributes']['emotion'])
                
        
 
                #############################
                path_and_file_name = os.path.join(path_out, "frame{:05d}.jpg".format(count))
                if save_frames_to_disk:
                    print '...saving to disk ' + path_and_file_name
                    cv2.imwrite(path_and_file_name, image_i)  # save frame as JPEG file
            
            # if 'count' is not in the index, skip the current frame and go to the next one
            success, image_i = cap.read()
            count += 1
    return frames, emo_vector, faces_vector, frame_ids, pd.concat([pd.DataFrame(emo_vector), pd.DataFrame([i for i in frame_ids], columns=['frame_indx'])], axis=1)



#frs, emo_vector, faces_vector, frame_indx, nice_df = video_to_emostream(path_to_video='IMG_9774.MOV', save_frames_to_disk=False)

