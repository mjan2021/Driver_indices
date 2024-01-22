import flask
from flask import request
import json
from datetime import datetime
import pandas as pd
from tqdm import tqdm

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

def search_and_aggregate(data, start_datetime, end_datetime, target_id=None):
    result = {}

    # start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M")
    # end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M")

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

if __name__ == "__main__":
    with open('data_storage.json', 'r') as json_file:
            data_str = json_file.read()
    video_data = json.loads(data_str)
    telematic_data = pd.read_excel("./Data _for_Integration.xlsx", index_col=False)
    
    telematic_data['video_data'] = ''
    print(telematic_data.head())
    for each_row in tqdm(telematic_data.iterrows(), total= telematic_data.shape[0], desc='Processing'):
        if each_row[1]['PID'] not in ['1013 1014(2)', '1013 1014', '1009 1010']:
            
            pid = each_row[1]['PID']
            start = each_row[1]['trip start']
            end = each_row[1]['trip end']
        
            search_results = search_and_aggregate(video_data, start, end, pid)
            # print(search_results.values())
            telematic_data.loc[each_row[0], 'video_data'] = str(search_results.values())
            
            # print(telematic_data.head())
    
    telematic_data.to_excel('telematic_data.xlsx', index=False)
        
        
        
        
    

    
    