import os
import json
import random
import metaData
import argparse
from tqdm import tqdm
from datetime import datetime


root = 'J:/DiskVautlData/Z/1122/Disk_files/debug'

def extract_indices_from_log(root, file):
    """
    Description: Extract indices from the log files

    Args:
        file :type string - file path

    Returns:
        dict(key: indice_type, value: indice_count
        dict(key: indice_type, value: list(indice_timestamps)
        list() : files with errors
    """

    alarmsDict = {'NOBODY': 0, 'LOOKING_DOWN': 0, 'SMOKING': 0, 'CALLING':0, 'LDW': 0, 'EYE_CLOSED': 0, 'LDW_R': 0, 'LDW_L':0, 'FCW':0, 'camera cover!':0, 'infrared block!': 0 }
    alarmsTimeStamp = {'NOBODY': [], 'LOOKING_DOWN': [], 'SMOKING': [], 'CALLING':[], 'LDW': [], 'EYE_CLOSED': [], 'LDW_R': [], 'LDW_L':[], 'FCW':[], 'camera cover!':[], 'infrared block!': [] }
    # alarmsDict = {'alarm_type 5': 0, 'alarm_type 4': 0, 'alarm_type 3': 0, 'alarm_type 1': 0, 'alarm_type 2': 0, 'alarm_type 17': 0, 'alarm_type 18': 0, 'alarm_type 27':0, 'alarm_type 16':0, 'alarm_type 9':0, 'alarm_type 7': 0 }
    error_files = []
    # print(f"Processing debug file {file}")
    with open(os.path.join(root, file), 'r') as logFile:
        lines = logFile.read().splitlines()
        for line in lines:
            words = line.split(" ")
            for alarm in alarmsDict.keys():
                if alarm in words:
                    alarmsDict[alarm] += 1
                    try:
                        timestamp = "".join(words[0].split('[')[1].split('-')).strip(']')
                        alarmsTimeStamp[alarm].append(timestamp)
                    except Exception:
                        error_files.append(file)
            
    return alarmsDict, alarmsTimeStamp, error_files

if __name__ == '__main__':
    start = datetime.now()
    for filename in os.listdir(root):
        if filename.endswith('.log'):
            alarmsDict, alarmsTimeStamp, error_files = extract_indices_from_log(root, filename)
            print(f'file: {filename} alarmDict: {alarmsDict} timestamps: {alarmsTimeStamp}')
    
    end = datetime.now()
    print(f'time taken: {end-start}')
    
            
            