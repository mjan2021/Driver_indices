import os
import glob
import metaData
# def update_duration(path):
#     """
#     Description: Get total time duration for driver and append to each driver per day. Duration is in hours
#     :param path :type string - path of the video folder with raw video files
#
#     return None - duration are appended to the JSON datafile
#     """
#     print(f"Getting total durations by day...")
#     duration = metaData.get_duration(path)
#     for iterator in range(0, len(jsonIndices)):
#         for index_duration in duration.keys():
#             if index_duration.split('/')[-1] == jsonIndices[iterator]['day']:
#                 if jsonIndices[iterator]['duration'] == 0.0:
#                     jsonIndices[iterator]['duration'] = round(((duration[index_duration])/60)/4, 2)
#
#     return duration
#

path = 'Z:/VIDEOS'

driver_camera_files = glob.glob(path+'/*/Video/**/*000.asf')
front_camera_files = glob.glob(path+'/*/Video/**/*100.asf')

file_dict = {}

for idx in range(0,len(front_camera_files)):
    size  = os.path.getsize(driver_camera_files[idx])

# print(driver_camera_files)

