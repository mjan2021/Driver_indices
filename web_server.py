import glob
from  tqdm import tqdm
import cv2
import metaData
from flask import Flask
from flask import render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
import imghdr
import os
import metaData
import json
from moviepy.editor import *


"""
Flask App defaults
"""
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.mp4', '.asf', '.3gpp']
app.config['UPLOAD_PATH'] = 'C:/Users/tanve/PycharmProjects/Drowsiness_detection/uploads'
path = 'data/data/cam_test/alerts'
excluded_list = ['1003 1004-nonAI', '1005-nonAI',]

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

    print(f"Extracting total driving hours...")
    # this line was changed for tqdm
    for index in tqdm(range(0,len(data['data']))):
        id = data['data'][index]['id']
        duration = data['data'][index]['duration']
        if id not in dr_hours.keys():
            dr_hours[id] = [1, round(duration/60)]
        else:
            dr_hours[id][0] += 1 #Days
            dr_hours[id][1] += round(duration/60) #hours
    return dr_hours

@app.errorhandler(413)
def too_large(e):
    print(f"File too large")
    return "File is too large", 413

@app.errorhandler(404)
def notFound(e):
    print(f"Page Not found")
    return render_template('index.html')

@app.route('/db')
def display():
    # files  = metaData.get_mp4_files(path)
    # print(files)
    with open('data_storage.json','r') as json_file:
        data = json.load(json_file)
    # print(type(data))
    return render_template('index.html', data = data)

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
        for index in range(0,len(data['data'])):
            if data['data'][index]['id'] == '1215':
                yawns = data['data'][index]['yawn']['total']
                yawn.append(yawns)
                labels.append(data['data'][index]['day'])
    # print([yawn, labels])
    return render_template('dashboard.html', data=data['data'])

@app.route('/uploading')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('uploading.html', files=files)

@app.route('/statistics')
def statistics():
    with open('data_storage.json', 'r') as json_file:
        data = json.load(json_file)
    datafile = {}

    for index in range(0,len(data['data'])):
        id = data['data'][index]['id']
        duration = data['data'][index]['duration']

        if id not in datafile.keys():
            datafile[id] = [1, round(duration/60)]

        else:
            datafile[id][0] += 1
            datafile[id][1] += round(duration/60)

    path = 'Z:/VIDEOS/**/Video/**/*.asf'
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
                size = file_meta['filesize']/1073741824
                datafile[id].append(round(size,2))
                # print(datafile)
            else:
                size = file_meta['filesize']/1073741824
                datafile[id][2] += round(size,2)
    # print(datafile)

    return render_template('statistics.html', files=datafile)

@app.route('/')
def db():
    # print(f"Page visited")
    with open('Datafiles/storage_stats.json') as json_file:
        data_file = json.load(json_file)
    labels, dataset = [],[]
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

    total_drivers = os.listdir('Z:/VIDEOS')
    hours = get_driving_hours('data_storage.json')
    # print(f"Chart: {labels},\n Data : {dataset}, \n Hours: {hours}")
    print(f" Hours: {hours}")
    for count in total_drivers:
        if count not in excluded_list:
            min_max = metaData.min_max_date(count)
            start_end_date[count] = min_max

    # print(f"Min_Max: {start_end_date}")
    return render_template('db.html', data=[labels, dataset], hours=hours, total=round(total_storage/1000,2), total_drivers=len(total_drivers), start_end_date =start_end_date)

@app.route('/uploading', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204

@app.route('/timestamp')
def timestamp():
    ts = request.args.get('timestamp') #indice timestamp
    id = request.args.get('id') # driver id
    time = ''.join(list(ts)[8:]) # time extracted from indice timestamp
    date = "".join(list(ts)[:8]) # date extracted from indice timestamp
    playback_path = 'Z:/VideoPlayback'

    driver = 'Z:/VIDEOS/' + id + '/**/*000.asf'
    front = 'Z:/VIDEOS/' + id + '/**/*100.asf'  # Hard coded path - make sure it exist

    # driver = 'D:/'+id+'/**/*000.asf'
    # front = 'D:/'+id+'/**/*100.asf' # Hard coded path - make sure it exist
    driver_files = glob.glob(driver, recursive=True) # list of video for selected driver from driver facing camera
    front_files = glob.glob(front, recursive=True) # list of videos for selected driver from front facing camera
    differences_list = [] # nested list containing file indexes and difference of seconds from indice

    # Cleaning the naming convention for files
    for idx in range(0, len(driver_files)):
        cleanup_date = "".join(driver_files[idx].split("\\")[-2].split('-'))
        # matching date of indice with the folder with date
        if cleanup_date == date:
            cleanup_filename = "".join(list(driver_files[idx].split('\\')[-1].split('.')[0])[1:7])
            print(f"CleanUpfilename: {cleanup_filename}, time: {time}")
            if int(cleanup_filename) < int(time):
                d = int(time) - int(cleanup_filename)
                differences_list.append([int(idx), d])

    print(f"Differences_list : {differences_list}")
    min_val = differences_list[0][1]
    # print(f"Min_val: {min_val}")
    for item in differences_list:
        index = 0
        if item[1] < min_val:
            min_val = item[1]
            index = item[0]

    # print(f"{index} - : {min_val}")
    clip = VideoFileClip(driver_files[index]).subclip(d-10, d+10)
    clip_front = VideoFileClip(front_files[index]).subclip(d - 10, d + 10)
    # clip.write_gif('C:/Users/tanve/PycharmProjects/Drowsiness_detection/test_gif.gif')
    clipped_video_folder = os.listdir('Z:/VideoPlayback/')
    clip.write_videofile('Z:/VideoPlayback/test.mp4', fps=15, audio=False)
    clip_front.write_videofile('Z:/VideoPlayback/test_front.mp4', fps=15, audio=False)

    print(f"Time : {time} - CleanupTime : {driver_files[index]} - Difference: {d}")

    # print(f"{time} : time - {date} : date - {id} : ID")
    # print(driver_files)
    filename = glob.glob('Z:/VideoPlayback/')
    return render_template('display.html', data=[filename])



if __name__=='__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)