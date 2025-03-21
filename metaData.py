import os
from tinytag import TinyTag
import json
import PIL
import time
import tqdm
import glob

# path = 'data/data/cam_test/alerts'
path = 'C:/Users/tanve/Downloads/Research_Data/14072021/827000'

# For Mounted Drive
# videos_url = 'Z:/VIDEOS/'

# For Server
videos_url = '/mnt/ivsdccoa/VIDEOS/'

#     if file.split('.')[-1] == 'mp4':
#         print(file)
def get_jpg_files(path):
    data = []
    for file in os.listdir(path):
        if file.split('.')[-1] == 'jpg':
            # dir = os.path.abspath(os.getcwd())
            # p = os.path.join(dir, path)

            # alarm_type
            alarm = "".join(list(file.split(".")[0].split("_")[2])[2:])
            # if alarm == "01":
            #     print(alarm)

            # Timestamp
            timestamp = "".join(list(file.split(".")[0].split("_")[-1])[2:])
            timestamp = convert_timestamp(timestamp)
            print(timestamp)
            # meta = get_meta(file, p)
            data.append(timestamp)
            
            # if alarm == "01":
            #     with open('data_storage.json') as data_storage:
            #         json.dump(data, data_storage)
    print(len(data))
    return data

def get_mp4_files(path):
    data = []
    for file in os.listdir(path):
        if file.split('.')[-1] == 'mp4':
            # print(file)
            dir = os.path.abspath(os.getcwd())
            p = os.path.join(dir, path)
            meta = get_meta(file, p)
            # meta = get_timestamp(file, p)
            # c_timestamp = convert_timestamp(meta)
            # data.append(c_timestamp)
            data.append(meta['duration'])
    # print(data)
    return data

def get_timestamp(file, path):
    # print(file)
    timestamp = file.split('.')[0].split('_')[-1]
    return timestamp

def convert_timestamp(timestamp):
    time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)))
    return time_formatted

def get_duration(path):
    f_list, f_dict = [], {}
    # Glob - getting list of files
    counter = 0
    total_fileList = len(os.listdir(path))
    for directory, subdirectory, fileList  in os.walk(path):
        dur = 0
        # print(f"{directory} : {subdirectory} : {fileList}")
        # f_dict[directory] += f_dict[directory] + get_meta(os.path.join(directory, fileList))
        for f in fileList:
            p = os.path.join(directory, f)
            metas = get_meta(p)
            try:
                if metas['duration'] < 10000:
                    dur += int(metas['duration'])
            except:
                dur += 0
                print(f'get_duration()::Error During Processing: {f}')
        dir_split = "".join(directory.split("\\")[-1].split("-"))
        print(f'Processing : {counter}/{total_fileList}, File: {dir_split}')
        counter += 1
        f_dict[dir_split] = dur
    # print(f"Total File: {len(f_list)}")
    return f_dict

def get_duration_modified(path):
    f_dict = {}
    # Glob - getting list of files
    counter = 0
    total_fileList = len(glob.glob(path+'**/*000.asf'))
    
    for file in glob.glob(path+'**/*000.asf'):
        dur = 0
        file = file.replace('\\', '/')
        metas = get_meta(file)
        try:
            if metas['duration'] < 10000:
                dur += int(metas['duration'])
        except:
            # dur += 0
            print(f'get_duration()::Error During Processing: {file}')
        dir_split = "".join(file.split("/")[-1].split("-"))
        print(f'Processing : {counter}/{total_fileList}, File: {dir_split}')
        counter += 1
        f_dict[dir_split] = dur
    
    return f_dict
        
def get_meta(path):

    # path = os.path.join(path, file)
    video = TinyTag.get(path)
    video_dict = {"album" : video.album,
                  "albumartist": video.albumartist,
                  "artist" : video.artist,
                  "aurdio_offset": video.audio_offset,
                  "bitrate" : video.bitrate,
                  "comment" : video.comment,
                  "composer" : video.composer,
                  "disc" : video.disc,
                  "disc_total" : video.disc_total,
                  "duration" : video.duration,
                  "filesize" : video.filesize,
                  "genre" :video.genre,
                  "samplerate" : video.samplerate,
                  "title" : video.title,
                  "track" : video.track,
                  "track_total" : video.track_total,
                  "year" : video.year}

    # with open('indices.json', 'w') as json_file:
    #     json.dump(dict(video_dict), json_file)
    return video_dict

def indices_to_json(id, day, key, value):
    with open('indices.json') as file:
        data = json.load(file)
        # json.dump(dict([id][0][day][0][key]), file)
    try:
        data[id][0][day][0][key] = value
    except Exception:
        print("Driver ID not found...")
        print("Adding driver into the data file")
        data[id] = list()
        data[id].append(dict())
        data[id][0][day] = list()
        data[id][0][day].append({key:value})
        print(data[id][0][day])


    with open('indices.json', 'w') as file:
        json.dump(data, file)
    return data


def min_max_date(driver_id, url):
    """
    This gets the minimu date and maximum date for a driver_id folder
    """
    min_value, max_value = 0, 0
    # path = videos_url+driver_id+'/Video/'
    path = url +'/'+driver_id + '/Video/'
    list_of_dates = os.listdir(path)
    if len(list_of_dates) > 0: 
        # .DS_Store: handlign MacOS created files error
        int_list = [int("".join(date.split('-'))) for date in list_of_dates if date != '.DS_Store']
        print(f"metaData::min_max_date(): {driver_id}")
        min_value, max_value = min(int_list), max(int_list)
    else:
        print(f"Driver ID: {driver_id} has no data")
    # min_value, max_value = min(dateList), max(dateList)
    return [min_value, max_value]

# f = get_jpg_files(path)
# f = get_mp4_files(path)
# dir ='C:/Users/tanve/Downloads/Research_Data/14072021/827000/'
# f = get_duration(path)
# print(f)
# print(convert_timestamp(1624918688))

# total = 0
# for index in f:
#     if index < 10000:
        # total += index

# print(total)