import os
import cv2
import cvlib
import numpy as np
import mediapipe as mp
import glob
from tqdm import tqdm
import codecs
from deepface import DeepFace
# from deepface.commons import functions, realtime, distance as dst
from deepface.modules import modeling, detection, preprocessing

"""
Working Gender Detection code for list of file in folder

"""
if os.name == "posix":
    print(f"MacOS detected")

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
          # face_224 = functions.preprocess_face(img=face, target_size=(224, 224), grayscale=False,
          #                                      enforce_detection=False)
          # face_224 = preprocessing.normalize_input(face_224)  # normalizing input
          # gender_prediction = gender_model.predict(face_224)[0, :]
          # if np.argmax(gender_prediction) == 0:
          #   g = "female"
          # elif np.argmax(gender_prediction) == 1:
          #   g = "male"
          # gender[g] += 1
          
          
          # deepface v0.0.84
          gdr = DeepFace.analyze(face, actions=['gender'])
          if gdr[0]['dominant-_gender'] == 'Man':
            g = "male"
          elif gdr[0]['dominant_gender'] == 'Woman':
            g = "female"
          gender[g] += 1

      if counter > 10:
        cap.release()
        return gender

def gender_detection_without_face_detection(path):
  # print(f'gender_detection_without_face_detection(): Reading file...')
  cap = cv2.VideoCapture(path)
  gender = {'male':0, 'female':0}
  counter = 0
  total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  if total_frames < 0:
    return None
  # print(f'gender_detection_without_face_detection(): Processing Frames...')
  while cap.isOpened():
    ret, frame = cap.read()
    if ret:
      gdr = DeepFace.analyze(img_path = frame, actions=['gender'], enforce_detection=False)
      if gdr[0]['dominant_gender'] == 'Man':
        g = "male"
      elif gdr[0]['dominant_gender'] == 'Woman':
        g = "female"
      gender[g] += 1
      counter += 1
      if counter > 10:
        cap.release()
        return gender
        
      
      



  
ID = '1134_1135'
all_processed_file = []
# read the list of files
if os.path.exists(f'./gender_split/gender_{ID}.txt'):
  with open(f'./gender_split/gender_{ID}.txt', 'r') as status_file:
    list_of_lines = status_file.readlines()
    for line in list_of_lines:
      all_processed_file.append(line.split(',')[0])
  
print(f'Total Files Processed: {len(all_processed_file)}')  
# if '/Volumes/ivsdccoa/VIDEOS/1003_1004/Video/2022-11-20/T054305000000.asf' in all_processed_file:
#   print("File already processed")
# exit()

video_files_directory = f'Y:/VIDEOS/{ID}/Video/'
if os.name =='posix':
  video_files_directory = video_files_directory.replace('Y:', '/Volumes/ivsdccoa')
list_of_files = glob.glob(video_files_directory+'**/*000.asf')

print(f"Total Videos: {len(list_of_files)}")
driver_gender = {}
for file in tqdm(list_of_files): #Change 0:1000
  skip = False
  file = '/'.join(file.split("\\"))
  print(file)
  try:
    # g = gender_detection(file)
    if file in all_processed_file:
      print(f"File already processed")
      skip = True
    else:
      g = gender_detection_without_face_detection(file)
      
  except Exception as e:
    print(f"Error.. {file} with Exception => {e}")
    continue
  
  # print(f"Driver_Gender (last-item): {g}")
  # # if g == None:
  #   driver_gender[file] = "None"
  # else:
  #   driver_gender[file] = max(g, key=g.get)
  
      
  # print(f"Driver_Gender: {driver_gender}")
  if skip == False:
    print(f"Driver_Gender (last-item): {g}")
    with open(f'./gender_split/gender_{ID}.txt', 'a+') as status_file:
      # status_file.write(','+str(driver_gender)+']') # use comma before writting the driver_gender
      if g == None:
        driver_gender[file] = "None"
        # status_file.write(f'{file}, None')
      else:
        # driver_gender[file] = max(g, key=g.get)
        status_file.write(f'{file}, {max(g, key=g.get)}')
      status_file.write('\n')


### DETECT THE FILE NAME WHICH HAVE TWO ID AND ONLY RUN THOSE OR MANUALLY RUN THE ONLY FOLDER WITH TWO IDs
