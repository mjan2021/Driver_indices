import os
import cv2
import os
import json
import glob
import imghdr
# import jsonify
import metaData
from datetime import datetime
import argparse
# import pandas as pd
import urllib.request
from tqdm import tqdm
from jinja2 import defaults
from moviepy.editor import *
from flask import Flask, flash
import flask
from datetime import datetime as dt
from werkzeug.utils import secure_filename
# from pandas.io.json import _normalize as json_normalize
from flask import render_template, request, redirect, url_for, abort, send_from_directory, send_file
from markupsafe import escape
import pandas as pd
import metaData
import ffmpeg
import subprocess

"""
Flask App defaults
"""

# Local Video Address
# app = Flask(__name__, static_folder='Z:/VideoPlayback')

# Server Video Address
# this can't be modified with function parameter
# app = Flask(__name__, static_folder='/mnt/ivsdccoa/VideoPlayback')
# app = Flask(__name__, static_folder='Y:/VideoPlayback')

FFMPEG = './assets/ffmpeg/bin/ffmpeg.exe'
app = Flask(__name__, static_folder='./static/')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.json',]
app.config['UPLOAD_PATH'] = 'assets/uploads/'
path = 'data/data/cam_test/alerts'
excluded_list = ['1003 1004-nonAI', '1005-nonAI', '1073', '2062', '1082']

"""
# For Server
# videos_url = '/mnt/ivsdccoa/VIDEOS'
# video_playback = '/mnt/ivsdccoa/VideoPlayback/'
# For Mounted Drive
# videos_url = 'Z:/VIDEOS'
# video_playback = 'Z:/VideoPlayback/'

# For Internal Use
# video_playback ='videplayback/'
"""

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def get_driving_hours(jsonfile):
    with open(jsonfile, 'r') as json_file:
        data = json.load(json_file)
    dr_hours = {}

    # this line was changed for tqdm
    for index in tqdm(range(0, len(data['data']))):
        id = data['data'][index]['id']
        duration = data['data'][index]['duration']
        if id not in dr_hours.keys():
            dr_hours[id] = [1, round(duration / 60)]
        else:
            dr_hours[id][0] += 1  # Days
            dr_hours[id][1] += round(duration / 60)  # hours
    return dr_hours

@app.route('/api')
def api():
    data = jsonify(pd.read_csv('data_storage.json'))
    
    
    return "data.keys()"

@app.errorhandler(413)
def too_large(e):
    print(f"File too large")
    return "File is too large...", 413


@app.errorhandler(404)
def notFound(e):
    print(f"{e}")
    return "NotFoundError"


@app.route('/db')
def display():
    with open('data_storage.json', 'r') as json_file:
        data = json.load(json_file)     
    return render_template('index.html', data=data)

# data-tabel ajax call to get the data from json file
@app.route('/data_storage.json')
def ajax():
    with open('data_storage.json') as file:
        data = json.load(file)
    return data

@app.route('/dashboard')
def dashboard():
    with open('data_storage.json') as file:
        yawn, labels = list(), list()
        data = json.load(file)
        for index in range(0, len(data['data'])):
            if data['data'][index]['id'] == '1215':
                yawns = data['data'][index]['yawn']['total']
                yawn.append(yawns)
                labels.append(data['data'][index]['day'])
    
    return render_template('dashboard.html', data=data['data'])


@app.route('/uploading')
def index():
    files = os.listdir(app.config['UPLOAD_PATH']+'convertedExcel/')
    return render_template('uploading.html', files=files)


@app.route('/statistics')
def statistics():
    with open('data_storage.json', 'r') as json_file:
        data = json.load(json_file)
    datafile = {}

    for index in range(0, len(data['data'])):
        id = data['data'][index]['id']
        duration = data['data'][index]['duration']

        if id not in datafile.keys():
            datafile[id] = [1, round(duration / 60)]

        else:
            datafile[id][0] += 1
            datafile[id][1] += round(duration / 60)

    path = videos_url + '/**/Video/**/*.asf'
    files = glob.glob(path, recursive=True)
    # print(f"Files List: {glob.glob(path, recursive=True)}")
    for file in files:
        id = file.split('\\')[1]
        # print(id)
        file_meta = metaData.get_meta(file)
        # print(file_meta['filesize'])
        # print(f"{datafile}")
        if id in datafile.keys():
            # print(f"{len(datafile[id])}")
            if len(datafile[id]) < 3:
                size = file_meta['filesize'] / 1073741824
                datafile[id].append(round(size, 2))
                # print(datafile)
            else:
                size = file_meta['filesize'] / 1073741824
                datafile[id][2] += round(size, 2)
    # print(datafile)

    return render_template('Statistics.html', files=datafile)


@app.route('/')
def db():
    # try:
            
    # print(f"Page visited")
    # try:
    print()

    with open('Datafiles/storage_stats.json') as json_file:
        data_file = json.load(json_file)
    labels, dataset = [], []
    start_end_date = {}
    total_storage = 0

    for idx in tqdm(range(0, len(data_file))):
        total = 0
        data = data_file[idx]['data']
        for idx_files in range(0, len(data)):
            files = data_file[idx]['data'][idx_files]['files']
            for all_file in files.values():
                total += all_file
        labels.append(data_file[idx]['driver_id'])
        dataset.append(int(total))
        total_storage += total

    # if item is not a directory then it will be not added to the list
    total_drivers = []
    for folder in os.listdir(videos_url):
        if os.path.isdir(os.path.join(videos_url, folder)):
            total_drivers.append(folder)
    
    hours = get_driving_hours('data_storage.json')
    print(f"Chart: {labels},\n Data : {dataset}, \n Hours: {hours}")
    # print(f" Hours: {hours}")
        
    for count in total_drivers:
        if count not in excluded_list:
            min_max = metaData.min_max_date(count, videos_url)
            start_end_date[count] = min_max

    print(f"Min_Max: {start_end_date}")
    
        # This Snipped will get rid of ZeroDvisionError for Average Driving hours Chart
    list_of_zero_value_drivers = []
    for key, value in hours.items():
        if 0 in value:
            list_of_zero_value_drivers.append(key)

    print(f"Driver with Zero Value Error: {list_of_zero_value_drivers}")
    
    for item in list_of_zero_value_drivers:
        hours.pop(item, None)

    print(f"<<<<<<<<< \n {hours} \n >>>>>>>>>>")
    Total_videos = len(glob.glob(videos_url+'/**/Video/*/*100.asf'))
    return render_template('db.html', data=[labels, dataset], hours=hours, total=round(total_storage / 1000, 2),
                            total_drivers=len(total_drivers), start_end_date=start_end_date, Total_videos=Total_videos)
    # except Exception as e:
    #     return f"Oops! Something went wrong..... /n{e}"

@app.route('/uploading', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    json_path = str(app.config["UPLOAD_PATH"])+'/jsonfiles/'
    excel_path = str(app.config["UPLOAD_PATH"])+'/convertedExcel/'
    uploaded_file.save(json_path+str(uploaded_file.filename))
    # filename = secure_filename(uploaded_file.filename)

    with open(json_path+str(uploaded_file.filename)) as f:
        jsonfile = json.load(f)
    to_dataframe = pd.DataFrame(jsonfile['data'])
    print(f'File Uploaded to : {excel_path} as {str(uploaded_file.filename.split(".")[0])+".xlsx"}')
    to_dataframe.to_excel(os.path.join(excel_path, str(uploaded_file.filename.split('.')[0])+".xlsx"))

    return send_file(f"assets/uploads/convertedExcel/{str(uploaded_file.filename.split('.')[0])}.xlsx", as_attachment=True)


@app.route('/download_excel')
def download_excel():
    try:
        file_path = request.args.get('file')
        with open(file_path) as f:
            jsonfile = json.load(f)
        to_dataframe = json_normalize(jsonfile['data'])
        to_dataframe.to_excel('assets/uploads/convertedExcel/data_storage.xlsx')
        return send_file('assets/uploads/convertedExcel/data_storage.xlsx', as_attachment=True)
    except:
        return "Resolve the Json_Normalize Error in the Code"

@app.route('/download_csv')
def download_csv():
    try:
        file_path = request.args.get('file')
        with open(file_path) as f:
            jsonfile = json.load(f)
        to_dataframe = json_normalize(jsonfile['data'])
        to_dataframe.to_csv('assets/uploads/convertedExcel/data_storage.csv', sep=',', encoding='utf-8')

        return send_file('assets/uploads/convertedExcel/data_storage.csv', as_attachment=True)
    except:
        return "Resolve the Json_Normalize Error in the Code"
       
@app.route('/download_json')
def download_json():
    file_path = request.args.get('file')
    return send_file('assets/uploads/convertedExcel/data_storage.json', as_attachment=True)


@app.route('/timestamp')
def timestamp():
    """
    Extract part of video based on the timestamp of the indice
    :return: render_template
    """
    # Empty Cache Directory

    # video_cache = os.listdir(app.static_folder)
    video_cache = os.listdir(video_playback)
    for file in video_cache:
        os.remove(os.path.join(video_playback, file))

    print(f'Cache Cleared...')

    ts = request.args.get('ts')  # indice timestamp
    id = request.args.get('id')  # driver id
    col = request.args.get('col')  # column name
    time = "".join(list(ts)[8:])  # time extracted from indice timestamp
    date = "".join(list(ts)[:8])  # date extracted from indice timestamp
    playback_path = video_playback
    print(f"URL Arguments >> Time: {time}, Date : {date} ")
    
    driver = videos_url + '/' + id + '/Video/**/*000.asf'
    front = videos_url + '/' + id + '/Video/**/*100.asf'  # Hard coded path - make sure it exist
    driver_files = glob.glob(driver, recursive=True)  # list of video for selected driver from driver facing camera
    front_files = glob.glob(front, recursive=True)  # list of videos for selected driver from front facing camera
    differences_list = {}
    
    # Cleaning the naming convention for files
    for idx in range(0, len(driver_files)):
        file_path = driver_files[idx].replace('\\', '/')
        cleanup_date = "".join(file_path.split('/')[-2].split('-'))
        cleanup_filename = file_path.split('/')[-1].split('.')[0][1:7]
    
        # matching date of indice with the folder date
        if cleanup_date == date:
    
            # matching Time of the indice with file name
            if int(cleanup_filename) < int(time):
                d = int(time) - int(cleanup_filename)
                differences_list[int(idx)] = d

    selected = min(differences_list.items(), key= lambda x:x[1])
    file_time = driver_files[selected[0]].replace('\\', '/')
    file_time_clean = file_time.split('/')[-1].split('.')[0][1:7]
    file_formated = datetime.datetime.strptime(file_time_clean, '%H%M%S').time()
    time_formated = datetime.datetime.strptime(time, '%H%M%S').time()
    minutes_diff = time_formated.minute - file_formated.minute
    seconds_diff = time_formated.second - file_formated.second
    total_diff = (minutes_diff * 60) + seconds_diff

    print(f"Difference (Seconds) : {total_diff}")
    clip = VideoFileClip(driver_files[selected[0]]).subclip(int(total_diff) - 10, int(total_diff) + 20)
    clip_front = VideoFileClip(front_files[selected[0]]).subclip(int(total_diff) - 10, int(total_diff) + 20)

    clipped_video_folder = os.listdir(video_playback)
    clip.write_videofile(video_playback+'test.mp4', fps=30, audio=False)
    clip_front.write_videofile(video_playback+'test_front.mp4', fps=30, audio=False)

    print(f"Time(url) : {time} - Time(filename) : {driver_files[selected[0]]} - Difference: {total_diff}")
    filename = glob.glob(playback_path+'*')

    # validated = check_validated_status(id, date, col, ts)
    validated= []
    return render_template('display.html', data=[filename], col=col, id=id, ts=ts, validation=validated)

# this is called in display.html to check status of validated/discard buttons
def check_validated_status(id, date, col, timestamp):
    print(f'Driver ID: {id}, Date: {date}, Column: {col}, Timestamp: {timestamp}')

    with open('validate.json', 'r') as val:
        validated = json.load(val)

    with open('discarded.json', 'r') as dis:
        discard = json.load(dis)

    # Check if the indice exists in validated.json
    for idx, val in enumerate(validated['data']):
        if val['id'] == id and val['day'] == date and timestamp in val[col].timestamp:
            return True
            
    # Check if the indice exists in discarded.json
    for idx, val in enumerate(discard['data']):
        if val['id'] == id and val['day'] == date and timestamp in val[col].timestamp:
            return True
    
    return False

@app.route('/validation')
def validation_indices():
    filename = './videoplayback/test.mp4'
    return render_template('validation.html', filename=filename)

@app.route('/valid')
def valid():
    """
    This is used for data vlidation and add seprate json file for validated data
    """
    col = str(request.args.get('col'))
    ts = str(request.args.get('ts'))
    id = str(request.args.get('id'))

    print(f'col: {col}, ts: {ts}, id: {id}')

    date = "".join(list(ts)[:8])

    with open('validate.json', 'r') as ds:
        valid = json.load(ds)

    # get all drivers:
    all_driver_ids = set()
    for val in valid['data']:
        all_driver_ids.add(val['id'])

    # get all dates and append to dictionary where keys = driver id and values = list of dates
    dates_list = {}
    for item in all_driver_ids:
        dates_list[item] = []

    # append all the dates to dictionary
    for val in valid['data']:
        dates_list[val['id']].append(val['day'])

    indice = {
        "id": '',
        "day": '',
        "duration": 0.0,
        "yawn": {"total": 0, "timestamp": []},
        "smoking": {"total": 0, "timestamp": []},
        "mobilephone": {"total": 0, "timestamp": []},
        "distraction": {"total": 0, "timestamp": []},
        "eyeclosing": {"total": 0, "timestamp": []},
        "crossinglane": {"total": 0, "timestamp": []},
        "nearcollision": {"total": 0, "timestamp": []},
        "stopsign": {"total": 0, "timestamp": []},
        "redlight": {"total": 0, "timestamp": []},
        "pedestrian": {"total": 0, "timestamp": []}
    }
    print(f'All Driver Dates: {dates_list}')
    for idx, value in enumerate(valid['data']):
        print(f'Index: {idx}, Value: {value["day"]} \n List of dates : {dates_list[value["id"]]}')

        if date not in dates_list[value['id']]:
            print(f'Not Present!')
            indice['id'] = str(id)
            indice['day'] = str(date)
            indice[str(col)]['total'] += 1
            indice[str(col)]['timestamp'].append(ts)
            dates_list[value['id']].append(date)


        elif date in dates_list[value['id']]:
            print(f'Date Present in List:  Matching..')
            if valid['data'][idx]['id'] == id and valid['data'][idx]['day'] == date:
                print(f'Matching Timestamps...')
                if ts not in valid['data'][idx][col]['timestamp']:
                    valid['data'][idx][col]['total'] += 1
                    valid['data'][idx][col]['timestamp'].append(ts)
                    print(f'Matched...')
                    break
    valid['data'].append(indice)
    print(f'Total Validated: {len(valid["data"])}')
    with open('validate.json', 'w') as ds:
        json.dump(valid, ds)

    return redirect('/db')

@app.route('/clean')
def clean_data():
    return render_template('clean.html')

@app.route('/clean.json')
def ajax_clean():
    with open('validate.json') as file:
        data = json.load(file)
    return data

@app.route('/discard')
def discarded_data():
    col = str(request.args.get('col'))
    ts = str(request.args.get('ts'))
    id = str(request.args.get('id'))

    print(f'col: {col}, ts: {ts}, id: {id}')

    date = "".join(list(ts)[:8])

    with open('discarded.json', 'r') as ds:
        discard = json.load(ds)

    # get all drivers:
    all_driver_ids = set()
    for val in discard['data']:
        all_driver_ids.add(val['id'])

    # get all dates and append to dictionary where keys = driver id and values = list of dates
    dates_list = {}
    for item in all_driver_ids:
        dates_list[item] = []

    # append all the dates to dictionary
    for val in discard['data']:
        dates_list[val['id']].append(val['day'])

    
    indice = {
        "id": '',
        "day": '',
        "duration": 0.0,
        "yawn": {"total": 0, "timestamp": []},
        "smoking": {"total": 0, "timestamp": []},
        "mobilephone": {"total": 0, "timestamp": []},
        "distraction": {"total": 0, "timestamp": []},
        "eyeclosing": {"total": 0, "timestamp": []},
        "crossinglane": {"total": 0, "timestamp": []},
        "nearcollision": {"total": 0, "timestamp": []},
        "stopsign": {"total": 0, "timestamp": []},
        "redlight": {"total": 0, "timestamp": []},
        "pedestrian": {"total": 0, "timestamp": []}
    }
    print(f'All Driver Dates: {dates_list}')
    for idx, value in enumerate(discard['data']):
        print(f'Index: {idx}, Value: {value["day"]} \n List of dates : {dates_list[value["id"]]}')

        if date not in dates_list[value['id']]:
            print(f'Not Present!')
            indice['id'] = str(id)
            indice['day'] = str(date)
            indice[str(col)]['total'] += 1
            indice[str(col)]['timestamp'].append(ts)
            dates_list[value['id']].append(date)


        elif date in dates_list[value['id']]:
            print(f'Date Present in List:  Matching..')
            if discard['data'][idx]['id'] == id and discard['data'][idx]['day'] == date:
                print(f'Matching Timestamps...')
                if ts not in discard['data'][idx][col]['timestamp']:
                    discard['data'][idx][col]['total'] += 1
                    discard['data'][idx][col]['timestamp'].append(ts)
                    print(f'Matched...')
                    break
    discard['data'].append(indice)
    print(f'Total Validated: {len(discard["data"])}')
    with open('validate.json', 'w') as ds:
        json.dump(discard, ds)

    return redirect('/db')

def date_difference_filter(date_str1, date_str2, format='%Y%m%d'):
    try:
        date1 = dt.strptime(str(date_str1), format).date()
        date2 = dt.strptime(str(date_str2), format).date()
        difference = (date2 - date1).days
    except Exception as e:
        print(f"date_difference_filter(): {e}")
        difference = 0
        
    return difference

@app.route('/charts')
def charts():
    with open('data_storage.json', 'r') as json_file:
        data = json.load(json_file)
    return render_template('visualize.html', data=data['data'])

@app.route('/search')
def search_aggregrated_data():
    data = ''
    
    
    
    return render_template('get_aggregate_data.html', data=data)

def search_and_aggregate(data, start_datetime, end_datetime, target_id=None):
    result = {}

    start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M")
    end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M")

    for entry in data["data"]:
        entry_day = entry["day"]
        entry_datetime = datetime.strptime(entry_day, "%Y%m%d")

        # Check if the entry is within the specified date and time range
        if start_datetime <= entry_datetime <= end_datetime:
            # Check if the entry matches the target ID if specified
            if target_id is None or entry["id"] == target_id:
                for event_type, event_data in entry.items():
                    if event_type not in ["id", "day", "duration"]:
                        result[event_type] = result.get(event_type, 0) + event_data["total"]

    return result

@app.route('/aggregate', methods=['GET'])
def aggregate():
    try:
        with open('data_storage.json', 'r') as json_file:
            data_str = json_file.read()
            
        # Replace this with your actual data
        # data_str = '{"data": [{"id": "1001", "day": "20210920", "duration": 35.86, "yawn": {"total": 0, "timestamp": []}, "smoking": {"total": 1, "timestamp": ["20210920103721"]}, "mobilephone": {"total": 0, "timestamp": []}, "distraction": {"total": 0, "timestamp": []}, "eyeclosing": {"total": 0, "timestamp": []}, "crossinglane": {"total": 0, "timestamp": []}, "nearcollision": {"total": 0, "timestamp": []}, "stopsign": {"total": 0, "timestamp": []}, "redlight": {"total": 0, "timestamp": []}, "pedestrian": {"total": 0, "timestamp": []}}, {"id": "1001", "day": "20210921", "duration": 39.76, "yawn": {"total": 0, "timestamp": []}, "smoking": {"total": 1, "timestamp": ["20210921103001"]}, "mobilephone": {"total": 0, "timestamp": []}, "distraction": {"total": 0, "timestamp": []}, "eyeclosing": {"total": 0, "timestamp": []}, "crossinglane": {"total": 0, "timestamp": []}, "nearcollision": {"total": 0, "timestamp": []}, "stopsign": {"total": 0, "timestamp": []}, "redlight": {"total": 0, "timestamp": []}, "pedestrian": {"total": 0, "timestamp": []}}]}'
        data = json.loads(data_str)

        target_id = request.args.get('target_id')
        start_datetime = request.args.get('start_datetime')
        end_datetime = request.args.get('end_datetime')

        result = search_and_aggregate(data, start_datetime, end_datetime, target_id)
        print(f"Result: {flask.jsonify(result)}")
        return flask.jsonify(result)
        
    except Exception as e:
        return flask.jsonify({'error': str(e)})

@app.route('/merge')
def merge_page():
    return render_template('merge.html')

@app.route('/merge', methods=['POST'])
def merge_data():
    uploaded_file = request.files['file']
    telematics_temp = pd.read_excel(uploaded_file.filename)
    # Conversion of formatted timestamps in json file 
    telematics_temp['trip start'] = pd.to_datetime(telematics_temp['trip start'])
    telematics_temp['trip end'] = pd.to_datetime(telematics_temp['trip end'])

    # Convert to the desired format
    telematics_temp['trip start formatted'] = telematics_temp['trip start'].apply(lambda x: x.strftime('%Y%m%d%H%M%S'))
    telematics_temp['trip end formatted'] = telematics_temp['trip end'].apply(lambda x: x.strftime('%Y%m%d%H%M%S'))

    # Convert Video data to timestamp based
    video_temp = flatten_json_timestamps('./data_storage.json')
    
    # save the files as csv
    telematics_temp.to_csv('telematics_temp.csv', index=False)
    video_temp.to_csv('video_temp.csv', index=False)
    
    # Read the csv files
    telematics_data = pd.read_csv('telematics_temp.csv')
    video_data = pd.read_csv('video_temp.csv')
    
    # Merge DataFrames based on timestamp
    merged_data = pd.merge(telematics_data, video_data, left_on="trip start formatted", right_on="timestamp", how="left")

    # Apply the function to create a new column in telematic_data
    telematics_data['count_per_type'] = telematics_data.apply(check_interval, args=[video_data], axis=1)

    # Expand the dictionary into separate columns
    count_per_type_df = telematics_data['count_per_type'].apply(pd.Series)

    # Merge the expanded data back to the original telematic DataFrame
    final_data = pd.concat([telematics_data, count_per_type_df], axis=1)

    # Drop the original 'count_per_type' column if needed
    final_data = final_data.drop('count_per_type', axis=1)

    # Fill NaN values with 0
    final_data = final_data.fillna(0)

    # Print or use the final DataFrame as needed
    final_data.to_csv('merged_data_dropper.csv', index=False)
    
    print(f'merge_data(): Data merged successfully')
    # return the file as a download
    return send_file('./merged_data_dropper.csv', as_attachment=True)
        
# Create a function to check if a timestamp is within a given interval
def check_interval(row, video_data):
        total = video_data[(video_data['id'] == row['PID']) & (video_data['timestamp'] >= row['trip start formatted']) & (video_data['timestamp'] <= row['trip end formatted'])]
        return total['type'].value_counts().to_dict()

def flatten_json_timestamps(json_file):
    with open(json_file) as f:
        data = json.load(f)

    flat_data = []

    for entry in data['data']:
        id_value = entry["id"]
        day = entry["day"]
        for key, value in entry.items():
            if key not in ["id", "day", "duration"]:
                if isinstance(value, dict):
                    total = value["total"]
                    timestamps = value["timestamp"]
                    for timestamp in timestamps:
                        flat_data.append({"id": id_value, "day": day, "type": key, "timestamp": timestamp})

    df = pd.DataFrame(flat_data)
    return df


@app.route('/sandbox')
def sandbox():
    data = {"front": "./GenderData/1001/Video/2021-11-09/T100504000100.asf",
            "driver": "./GenderData/1001/Video/2021-11-09/T100504000000.asf",
            "map": [],
            "plot": []}
    
    # data['driver'] = convert_asf_to_mp4(data['driver'], './static/driver.mp4')
    # data['front'] = convert_asf_to_mp4(data['front'], './static/front.mp4')
    
    
    return render_template('sandbox.html', data=data)

def get_telematic_plot_for_sandbox():
    
    return ""

def get_gps_data_for_sandbox():
    
    return ""

def convert_asf_to_mp4(input_file, output_file):
    """ Convert ASF to MP4 using FFmpeg """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return False

    try:
        result = subprocess.run(
            [FFMPEG, "-i", input_file, "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  
        )
        print(result.stdout)
        print(result.stderr) 

        if result.returncode == 0:
            print(f"Conversion successful! Saved as {output_file}")
            return output_file
        else:
            print("FFmpeg encountered an error.")
            return None

    except Exception as e:
        print(f"Error running FFmpeg: {e}")
        return None


if __name__ == '__main__':
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument('--type', help='server or local')
    args = argsparser.parse_args()
    video_url = ''
    if args.type == 'local':
        if os.name == 'nt':
            videos_url = 'Y:/VIDEOS'
            video_playback = 'Y:/VideoPlayback/'
        else:
            videos_url = '/Volumes/ivsdccoa/VIDEOS'
            video_playback = '/Volumes/ivsdccoa/VideoPlayback/'
    elif args.type == 'server':
        videos_url = '/mnt/ivsdccoa/VIDEOS'
        video_playback = '/mnt/ivsdccoa/VideoPlayback/'
    elif args.type =='test':
        video_url = './GenderData/1001/'
        video_playback = './static/'

    excluded_list.append([f for f in video_url if f.find('male') != -1 or f.find('female') != -1])
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    
app.jinja_env.filters['date_difference'] = date_difference_filter
#app.run(debug=True)
app.run(host='0.0.0.0', port=5001, debug=True)
