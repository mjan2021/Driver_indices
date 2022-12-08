import os
import json
import random
import metaData
import argparse
from tqdm import tqdm

# Argument Parsers
parser = argparse.ArgumentParser()
parser.add_argument('-id','--id', dest='id', help='Driver id to be stored in file')
parser.add_argument('-f', '--i'  'file', dest='ifile', help='Indices File Location with path')
parser.add_argument('-videofolder','--vfolder', dest='vfolder', help='video folder for duration extraction')
parser.add_argument('-logfolder', '--lfolder', dest='logfolder', help='Path for log folder')

args = parser.parse_args()
filePath = args.logfolder
driverID = args.id
# driverID = "1213"

# create a function that take string path of excel file and read it as dataframe


def extract_indices_from_log(file):
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
    with open(os.path.join(filePath, file), 'r') as logFile:
        lines = logFile.read().splitlines()
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


def get_list_of_days():
    days_list = {}
    days = []
    for i, d in enumerate(data['data'][:500]):
        if d['id'] in days_list.keys():
            days_list[d['id']].append(d['day'])
        elif d['id'] not in days_list.keys():
            days_list[d['id']] = list()
            days_list[d['id']].append(d['day'])
    return days_list


def read_data_from_json(file):
    with open(file) as jsonFile:
        indices = json.load(jsonFile)
    return indices['data']


# update the duration of video by day
def update_duration(path):
    """
    Description: Get total time duration for driver and append to each driver per day. Duration is in hours
    :param path :type string - path of the video folder with raw video files

    return None - duration are appended to the JSON datafile
    """
    print(f"Getting total durations by day...")
    duration = metaData.get_duration(path)
    for iterator in range(0, len(jsonIndices)):
        for index_duration in duration.keys():
            if index_duration.split('/')[-1] == jsonIndices[iterator]['day']:
                if jsonIndices[iterator]['duration'] == 0.0:
                    jsonIndices[iterator]['duration'] = round(((duration[index_duration])/60)/4, 2)

    return duration

jsonIndices = read_data_from_json(args.ifile)
fileList = os.listdir(filePath)
fileName = []

# getting list of log files
for f in fileList:
    # indices = extract_indices_from_log(f)
    fileName.append(str(f.split("-")[1]))

print(fileName)
dates_list = []
for idx in range(0, len(jsonIndices)):
    if jsonIndices[idx]['id'] == args.id:
        dates_list.append(jsonIndices[idx]['day'])

print(f"List of days: {dates_list}")

# adding the list of log files as day to datafile
for i in set(fileName):
    if i not in dates_list:
        jsonIndices.append({
            "id": driverID,
            "day": i,
            "duration": 0.0,
            "yawn": {"total": 0, "timestamp": []},
            "smoking": {"total": 0, "timestamp": []},
            "mobilephone": {"total": 0, "timestamp": []},
            "distraction": {"total": 0, "timestamp": []},
            "eyeclosing": {"total": 0,  "timestamp" : []},
            "crossinglane": {"total": 0,"timestamp" : []},
            "nearcollision": {"total": 0, "timestamp" : []},
            "stopsign": {"total": 0, "timestamp": []},
            "redlight": {"total": 0, "timestamp": []},
            "pedestrian": {"total": 0, "timestamp": []}
             })

print(f"{len(jsonIndices)}")

# appending the indices in the logfiles to datafile
for index_counter in tqdm(range(0, len(jsonIndices))):
    for list_of_files in os.listdir(filePath):
        if str(list_of_files.split("-")[1]) == jsonIndices[index_counter]['day'] and jsonIndices[index_counter]['id'] == driverID:
            indices, indicesTimestamps, error_files_list = extract_indices_from_log(list_of_files)
            jsonIndices[index_counter]['smoking']['total'] = int(jsonIndices[index_counter]['smoking']['total']) + int(indices['SMOKING'])
            jsonIndices[index_counter]['distraction']['total'] = int(jsonIndices[index_counter]['distraction']['total']) + int(indices['LOOKING_DOWN'])
            jsonIndices[index_counter]['eyeclosing']['total'] = int(jsonIndices[index_counter]['eyeclosing']['total']) + int(indices['EYE_CLOSED'])
            jsonIndices[index_counter]['crossinglane']['total'] = int(jsonIndices[index_counter]['crossinglane']['total']) + int(indices['LDW']) + int(indices['LDW_L']) + int(indices['LDW_R'])
            jsonIndices[index_counter]['nearcollision']['total'] = int(jsonIndices[index_counter]['nearcollision']['total']) + int(indices['FCW'])
            jsonIndices[index_counter]['mobilephone']['total'] = int(jsonIndices[index_counter]['mobilephone']['total']) + int(indices['CALLING'])

            jsonIndices[index_counter]['smoking']['timestamp'].extend(indicesTimestamps['SMOKING'])
            jsonIndices[index_counter]['mobilephone']['timestamp'].extend(indicesTimestamps['CALLING'])
            jsonIndices[index_counter]['distraction']['timestamp'].extend(indicesTimestamps['LOOKING_DOWN'])
            jsonIndices[index_counter]['eyeclosing']['timestamp'].extend(indicesTimestamps['EYE_CLOSED'])
            jsonIndices[index_counter]['crossinglane']['timestamp'].extend(indicesTimestamps['LDW'])
            jsonIndices[index_counter]['crossinglane']['timestamp'].extend(indicesTimestamps['LDW_L'])
            jsonIndices[index_counter]['crossinglane']['timestamp'].extend(indicesTimestamps['LDW_R'])
            jsonIndices[index_counter]['nearcollision']['timestamp'].extend(indicesTimestamps['FCW'])

"""
Above code add the indices but from the start, upgrade must be made so it only adds the new data not the old.
possible solution for now: re-Run the file from start 
future possible solution: should check for the date, if it exists in the json then ignore that date indices
"""
# updating the durations
# duration = metaData.get_duration('C:/Users/tanve/Downloads/Research_Data/JoAnn_Video/827000/')
# for index_counter in range(0, len(jsonIndices)):
#     for index_duration in duration.keys():
#         if index_duration.split('/')[-1] == jsonIndices[index_counter]['day']:
#             jsonIndices[index_counter]['duration'] = (duration[index_duration])/60
# print(duration)
# update_duration('C:/Users/tanve/Downloads/Research_Data/JoAnn_Video/827000/')


update_duration(args.vfolder)

data = {"data": jsonIndices}

# Writing the indices to the json file
with open(args.ifile, 'w') as jsonfile:
    json.dump(data, jsonfile)

print(f"Length : {len(jsonIndices)}")
print(f"Files with Errors -> {error_files_list}")




