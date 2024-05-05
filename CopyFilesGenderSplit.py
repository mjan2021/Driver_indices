import os
import re
import cv2
import glob
import shutil
import pandas as pd
from datetime import datetime


def add_seconds_to_time(time_str, seconds):
    # Parse time string to datetime object
    time_obj = datetime.datetime.strptime(time_str, '%H%M%S')
    # Add seconds
    time_obj += datetime.timedelta(seconds=seconds)
    # Format back to time string
    new_time_str = time_obj.strftime('%H%M%S')
    return new_time_str

# convert string to time
def to_time(time_str):
    return datetime.datetime.strptime(time_str, '%H%M%S').time()

# Function to extract date and time from file paths
def extract_date_time_from_logs(file_path):
    file_path = file_path.replace('\\', '/')
    date = file_path.split('-')[1]
    time = file_path.split('-')[2].split('.')[0]
    print(f'Logs => Date: {date}, Time: {time}')
    return date, time

def extract_date_time_from_videos(file_path):
    file_path = file_path.replace('\\', '/')
    date = "".join(file_path.split('/')[-2].split('-'))
    start_time = file_path.split('/')[-1].split('.')[0][1:5]
    
    cap = cv2.VideoCapture(file_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_seconds = total_frames / cap.get(cv2.CAP_PROP_FPS)
    end_time = add_seconds_to_time(start_time, total_seconds)
    print(f'Video => Date: {date}, start_time: {start_time}, end_time: {end_time}')
    return date, start_time, end_time

# ===========================================
# For MacOS
# base_directory = '/Volumes/ivsdccoa/VIDEOS/'

# For Windows
base_directory = '/Volumes/ivsdccoa/VIDEOS/'
# ===========================================

juan = pd.read_csv('./GenderFilesSplitted/juan_replaced.csv')
alex = pd.read_csv('./GenderFilesSplitted/alex.csv')
tanveer = pd.read_csv('./GenderFilesSplitted/tanveer_replaced.csv')

#combine datafranes
df = pd.concat([juan, alex, tanveer], axis=0)
df['Verifyied'].replace({'f':'female', 'm':'male'}, inplace=True)
# print(df['Verifyied'].value_counts())
filtered_df = df[df['Verifyied'].isin(['male', 'female'])]
print(filtered_df['Verifyied'].value_counts())

data = {
    'male': [1004, 1010, 1012, 1013, 1031, 1044, 1055, 1070, 1075, 1099, 1112, 1135],
    'female': [1003, 1009, 1011, 1014, 1017, 1043, 1056, 1071, 1074, 1100, 1113, 1134]
}

print(filtered_df.head())
print(filtered_df['Verifyied'].value_counts())

# Iterate over DataFrame rows
counter = 0
total_files = len(filtered_df['Combined'])
g = {'male': 0, 'female': 0}
for index, row in filtered_df.iterrows():
    counter +=1
    gender = row['Verifyied']
    ID = "_".join(row['Combined'].split('_')[1:3])
    ID1 = row['Combined'].split('_')[1]
    ID2 = row['Combined'].split('_')[2]
    folder = row['Combined'].split('_')[3]
    filename = ".".join(row['Combined'].split('_')[4].split('.')[:-1])
    
    # this is for copying front-facing video
    file_front = f'{filename[:-8]}0100.asf'
    
    
    if int(ID1) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID1}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID1}_{gender}/Video/{folder}')
        
        src = f'{base_directory}{ID}/Video/{folder}/{file_front}'
        dst = f'{base_directory}{ID1}_{gender}/Video/{folder}/{file_front}' 
        shutil.copyfile(src, dst)   
        print(f'{counter}/{total_files} file -> {base_directory}{ID1}_{gender}/Video/{folder}/{file_front}')
        

    elif int(ID2) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID2}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID2}_{gender}/Video/{folder}')
        
        src = f'{base_directory}{ID}/Video/{folder}/{file_front}'
        dst = f'file -> {base_directory}{ID2}_{gender}/Video/{folder}/{file_front}'
        shutil.copyfile(src, dst)
        print(f'{counter}/{total_files} file -> {base_directory}{ID2}_{gender}/Video/{folder}/{file_front}')
       
    g[gender] += 1
    # counter += 1
