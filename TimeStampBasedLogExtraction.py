import os
import json
import random
import metaData
import argparse
from tqdm import tqdm
import datetime
import pandas as pd

if os.name == 'nt':
    root = 'Y:/VIDEOS'
elif os.name == 'posix':
    root = '/Volumes/ivsdccoa/VIDEOS'
def extract_indices_from_log(filePath,file):
    alarmsDict = {'NOBODY': 0, 'LOOKING_DOWN': 0, 'SMOKING': 0, 'CALLING':0, 'LDW': 0, 'EYE_CLOSED': 0, 'LDW_R': 0, 'LDW_L':0, 'FCW':0, 'camera cover!':0, 'infrared block!': 0 }
    alarmsTimeStamp = {'NOBODY': [], 'LOOKING_DOWN': [], 'SMOKING': [], 'CALLING':[], 'LDW': [], 'EYE_CLOSED': [], 'LDW_R': [], 'LDW_L':[], 'FCW':[], 'camera cover!':[], 'infrared block!': [] }
    # alarmsDict = {'alarm_type 5': 0, 'alarm_type 4': 0, 'alarm_type 3': 0, 'alarm_type 1': 0, 'alarm_type 2': 0, 'alarm_type 17': 0, 'alarm_type 18': 0, 'alarm_type 27':0, 'alarm_type 16':0, 'alarm_type 9':0, 'alarm_type 7': 0 }
    # alarmsTimeStamp = {'alarm_type 5': [], 'alarm_type 4': [], 'alarm_type 3': [], 'alarm_type 1': [], 'alarm_type 2': [], 'alarm_type 17': [], 'alarm_type 18': [], 'alarm_type 27':[], 'alarm_type 16':[], 'alarm_type 9':[], 'alarm_type 7': [] }
    
    error_files = []
    # print(f"Processing debug file {filePath+file}")
    with open(os.path.join(filePath, file), 'r', encoding='utf-8', errors='ignore') as logFile:
        # lines = logFile.read().splitlines()
        lines = logFile.readlines()
        for line in lines:
            words = line.split(" ")
            """
            Retrieve alarm will be here
            """
            for alarm in alarmsDict.keys():
                if alarm in words:
                    alarmsDict[alarm] += 1
                    # below is date extraction so needs to be corrected****** --> currently is this -->[20210504-140826][03][baseIVS]
                    try:
                        timestamp = "".join(words[0].split('[')[1].split('-')).strip(']')
                        alarmsTimeStamp[alarm].append(timestamp)
                    except Exception:
                        error_files.append(file)

        # logFile.close()
        # print(alarmsDict)
    return alarmsDict, alarmsTimeStamp, error_files

excluded_list = ['1003 1004','1031 1017','1011 1012','1043 1044','1013 1014','1003 1004-nonAI', '1005-nonAI', '1073', '2062']
ids = []
for item in os.listdir(root):
    if item not in excluded_list:
        ids.append(item)

jsonfile = []
mapping = {'NOBODY': 0,
           'LOOKING_DOWN': 1,
           'SMOKING': 2, 
           'CALLING': 3, 
           'LDW': 5, 
           'EYE_CLOSED': 4, 
           'LDW_R': 5, 
           'LDW_L':5, 
           'FCW':6, 
           'camera cover!':0, 
           'infrared block!': 0 }

print(f'Number of drivers: {len(ids)}\nIDs: {ids}')
for each_driver in tqdm(ids):
    
    logFolder = f'{root}/{each_driver}/Disk_files/debug/'
    if os.path.exists(logFolder):
        for logfile in os.listdir(logFolder):
            # print(f'file: {logfile}')
            driverid = each_driver
            if logfile.endswith('.log'):
                alarmdict, alarmtimestamp, err = extract_indices_from_log(logFolder, logfile)
                for key, value in alarmtimestamp.items():
                    for ts in value:
                        if key != 'NOBODY':
                            id = driverid
                            alarm_type = key
                            date = ts[:9]
                            
                            transform_dict = {'id': id, 'date': date, 'timestamp': ts, 'type': mapping[alarm_type]}
                            jsonfile.append(transform_dict)

with open('./Datafiles/Timestamps_data_Dec23.json', 'w') as jsonf:
    json.dump(jsonfile, jsonf)
    
        
        