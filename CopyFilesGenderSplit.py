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

# Function to match log entries to corresponding videos
def match_logs_to_videos(video_path, log_paths, gender):
    video_date, video_start_time, video_end_time = extract_date_time_from_videos(video_path)
    for log_path in log_paths:
        with open(log_path, 'r') as log_file:
            log_content = log_file.readlines()

        log_date, log_time = extract_date_time_from_logs(log_path)
        # if not os.path.exists(f'./GenderData/1001_{gender}/debug'):
        #     os.makedirs(f'./GenderData/1001_{gender}/debug/')
            
        output_log = open(f"./GenderData/1001/Seperated_logs/{video_date}-{video_start_time}.log", 'a+')
        # output_log.write(f'Log file for video {video_path} from log {log_path}')
        match = False
        for log_entry in log_content:
            if log_entry[:1] == '[':
                    
                # print(f'log_entry: {log_entry} - date: {video_date}, time: {video_time} ')
                time_from_log_entry = log_entry.split(']')[0].split('-')[-1]
                
                # print(f'======== {time_from_log_entry} ========')
                
                # Handle cases where the time is one second off (+/- 1)
                if str(int(video_start_time) + 1) in log_entry or str(int(video_start_time) - 1) in log_entry:
                    match = True
                
                # if log time is in between video start and end time
                if to_time(time_from_log_entry) >= to_time(str(int(video_start_time) - 1)) and to_time(time_from_log_entry) <= to_time(str(int(video_start_time) + 1)):
                    match = True
                
                
                if video_date in log_entry and match == True:
                    print(f'log_entry: {log_entry} - date: {video_date}, time: {video_start_time} ')
                    output_log.write(f'{str(log_entry)}')
                    match = False
        
        output_log.close()
        # print(f"Created log file for video {video_path} from log {log_path}")

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
    log_files = [each_log.replace("\\","/") for each_log in glob.glob(f'{base_directory}/{ID}/Disk_files/debug/*.log')]
    
    if int(ID1) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID1}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID1}_{gender}/Video/{folder}')
        
        if not os.path.exists(f'{base_directory}{ID1}_{gender}/Disk_files/debug/'):
            os.makedirs(f'{base_directory}{ID1}_{gender}/Disk_files/debug/') 
        
        src = f'{base_directory}{ID}/Video/{folder}/{file_front}'
        dst = f'{base_directory}{ID1}_{gender}/Video/{folder}/{file_front}' 
        shutil.copyfile(src, dst)   
        print(f'{counter}/{total_files} file -> {base_directory}{ID1}_{gender}/Video/{folder}/{file_front}')
        
        # perform arranging the logs to the corresponding videos => match_logs_to_videos(src, log_files) in ipynb one
        # then copy the logs files since they match the videos now => shutil.copyfile(log_file, dst)
        

    elif int(ID2) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID2}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID2}_{gender}/Video/{folder}')
        
        src = f'{base_directory}{ID}/Video/{folder}/{file_front}'
        dst = f'file -> {base_directory}{ID2}_{gender}/Video/{folder}/{file_front}'
        shutil.copyfile(src, dst)
        print(f'{counter}/{total_files} file -> {base_directory}{ID2}_{gender}/Video/{folder}/{file_front}')

    g[gender] += 1
    # counter += 1
