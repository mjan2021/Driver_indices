import cv2
import cvlib
import numpy as np
import mediapipe as mp
import glob
from tqdm import tqdm
import codecs
from deepface import DeepFace
from deepface.commons import functions, realtime, distance as dst

"""
Working Gender Detection code for list of file in folder

"""

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
gender_model = DeepFace.build_model('Gender')
def gender_detection(path):
    
  # For video input:
  # path = 'C:/Users/tanve/Desktop/Selected-Data/T084652000000.asf'
  cap = cv2.VideoCapture(path)
  # cap = cv2.VideoCapture('D:/1011 1012/Video/2021-06-20/T084652000000.asf', cv2.CAP_DSHOW)

  gender = {'male':0, 'female':0}
  counter = 0
  ignore_counter = 0
  with mp_face_detection.FaceDetection(min_detection_confidence=0.7) as face_detection:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        # print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        ignore_counter += 1
        if ignore_counter >= 10:
          break
        continue

      image_rows, image_cols, image_ch = image.shape
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      image.flags.writeable = False
      results = face_detection.process(image)
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      if results.detections:
        counter += 1
        for detection in results.detections:
          keypoints = []
          for keypoint in detection.location_data.relative_keypoints:
            key_px = mp_drawing._normalized_to_pixel_coordinates(keypoint.x, keypoint.y,image_cols,image_rows)
            keypoints.append(key_px)

          # 40 & 70 are the offsets for the face detection box
          cv2.rectangle(image, (keypoints[4][0]-40,keypoints[4][1]-70),(keypoints[3][0]+70, keypoints[5][1]+70), (0, 255, 0), 2)
          p1x = keypoints[4][0]-40
          p1y = keypoints[4][1]-70

          p2x = keypoints[3][0]+70
          p2y = keypoints[5][1]+70

          w = p2x - p1x
          h = p2y - p1y

          face = image[p1y:p1y+h, p1x:p1x+w]

          # deepface gender detection - works much better that cvlib
          face_224 = functions.preprocess_face(img=face, target_size=(224, 224), grayscale=False,
                                               enforce_detection=False)
          gender_prediction = gender_model.predict(face_224)[0, :]
          if np.argmax(gender_prediction) == 0:
            g = "female"
          elif np.argmax(gender_prediction) == 1:
            g = "male"
          gender[g] += 1

      if counter > 10:
        cap.release()
        return gender



video_files_directory = 'Z:/VIDEOS/1013 1014/Video/'
list_of_files = glob.glob(video_files_directory+'**/*000.asf')

print(f"Total Videos: {len(list_of_files)}")
driver_gender = {}
for file in tqdm(list_of_files[:1000]): #Change 0:1000
      
      file = '/'.join(file.split("\\"))
      
      print(file)
      try:
        g = gender_detection(file)
      except:
        print(f"Error.. {file}")
        continue
      
      print(f"Driver_Gender (last-item): {g}")
      if g == None:
        driver_gender[file] = "None"
      else:
        driver_gender[file] = max(g, key=g.get)
      
      
# print(f"Driver_Gender: {driver_gender}")
with open('gender_deepface_1013_1014.txt', 'a+') as file:
  file.write(','+str(driver_gender)+']') # use comme before writting the driver_gender


### DETECT THE FILE NAME WHICH HAVE TWO ID AND ONLY RUN THOSE OR MANUALLY RUN THE ONLY FOLDER WITH TWO IDs