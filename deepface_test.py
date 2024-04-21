from deepface import DeepFace
import cv2
import glob

root = "/Volumes/ivsdccoa/VIDEOS/1003_1004/Video/2021-11-08/"
video = glob.glob(root+"*000.asf")

print(video)
cap = cv2.VideoCapture(video[0])

while cap.isOpened():
  ret, frame = cap.read()
  if ret:
    obj = DeepFace.analyze(img_path = frame, actions=['gender'], enforce_detection=False)
    
    

# obj = DeepFace.analyze(img_path = "./assets/gender.JPEG", actions=['gender'])

# print(obj)