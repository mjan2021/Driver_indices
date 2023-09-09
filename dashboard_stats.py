import os
import glob
import metaData
import json
from tqdm import tqdm
import argparse

# 1057 was removed from Excluded list and 1082 was added
def add_drivers_to_json(main_data_folder, json_file_path):
    # excluded_list = ['1003 1004-nonAI', '1005-nonAI', '1002', '1073', '2062', '1082']
    # excluded_list = ['1009 1010',
    #              '1011 1012',
    #              '1003 1004',
    #              '1031 1017',
    #              '1011 1012',
    #              '1043 1044',
    #              '1055 1056',
    #              '1074 1075',
    #              '1099 1100',
    #              '1013 1014',
    #              '1003 1004-nonAI',
    #              '1005-nonAI',
    #              '1073',
    #              '1082',
    #              '1094',
    #              '1097',
    #              '2002',
    #              '2062'
    #              ]

    # List with Zero Videos
    excluded_list = ['1003 1004-nonAI',
                 '1005-nonAI',
                 '1073',
                 '1082',
                 '1094',
                 '1097',
                 '2002',
                 '2062'
                ]   
    # ================================================ #
    # Folder/Paths validation
    if os.path.exists(main_data_folder):
        driver_ids = os.listdir(main_data_folder)
    else:
        print(f'add_drivers_to_json: {main_data_folder} does not exist...')
        return
    
    if os.path.exists(json_file_path):
       pass
    else:
        print(f'add_drivers_to_json: {json_file_path} does not exist...')
        return
    # ================================================ #
    
    
    with open(json_file_path) as json_file:
        stats = json.load(json_file)
    print(f'add_drivers_to_json(): Processing Folders...')
    for id in range(0, len(driver_ids)):
        if driver_ids[id] not in excluded_list:
            # print(f"Processing driver: {driver_ids[id]}")
            # condition must be inserted to check if the jsonfile have the driverID already
            # if id_from_json in json[index]['driver_id]
            #   not working -----
            stats.append({'driver_id': driver_ids[id], "data": []})
            path_to_dates = main_data_folder+ '/' + driver_ids[id] + '/Video/*'
            dates = glob.glob(main_data_folder+ '/' + driver_ids[id] + '/Video/*')
            # if os.path.exists(path_to_dates):
            #     dates = glob.glob(main_data_folder+ '/' + driver_ids[id] + '/Video/*')
            # else:
            #     print(f'add_drivers_to_json: {path_to_dates} does not exist...')
            #     return
            for date in dates:
                # print(f"Processing Date: {date}")
                date = date.split('\\')[-1]
                stats[-1]['data'].append({"date": date, "files": {}})
            del dates

    print(f'add_drivers_to_json(): Total Processed Folders: {len(stats)}')
    # Open Json file and dump stats 
    with open(json_file_path, 'w') as json_f:
        json.dump(stats, json_f)

    return "Total Drivers Added: "+str(len(stats))

def filling_driver_dates(path, json_file):

    # Get all the files from both cameras
    driver_camera_files = glob.glob(path + '/*/Video/**/*000.asf')
    front_camera_files = glob.glob(path + '/*/Video/**/*100.asf')

    file_dict = {}
    with open(json_file) as stats_file:
        stats = json.load(stats_file)
    print(f"filling_drivers_dates(): Total Drivers: {len(stats)}")

    # combine both lists
    combined_list = driver_camera_files + front_camera_files
    print(f"Total Files: {len(combined_list)}, DMS: {len(driver_camera_files)}, ADAS: {len(front_camera_files)}")
    # f = open(root_path+'/Datafiles/storage_stats.txt', "w+")
    for idx in tqdm(range(0, len(combined_list))):
        
        filename = combined_list[idx].split("\\")
        # print(filename)
        driver_id = filename[1]
        date = filename[3]
        file = filename[4]
        clean_filename = "/".join(filename)
        size = os.path.getsize(clean_filename)
        # print(stats)
        # f.write(f'filename: {filename}, size: {size/1048576}Mb\n')
        # print(f"driver: {driver_id}, date: {date}, filename: {file}, size: {size/1048576}Mb")
        for driver_idx in range(0, len(stats)):
            # print(json_idx['driver_id'])
            if stats[driver_idx]['driver_id'] == driver_id:
                # print(f'ID matches: {driver_id}')
                for date_idx in range(0, len(stats[driver_idx]['data'])):
                    if stats[driver_idx]['data'][date_idx]['date'] == date:
                        # print(f'Date matches: {date}')
                        stats[driver_idx]['data'][date_idx]['files'][file] = size / 1048576

    # f.close()
    print(f"Total Driver: {len(stats)}")
    # print(stats)
    
    with open(json_file, 'w+') as json_f:
        json.dump(stats, json_f)
        
        print(f"filling_driver_dates(): {json_file} updated")
    
    # with open(root_path+'/Datafiles/storage_stats.txt', "w+") as json_file:
    #     print(f'writing txt file...')
    #     json_file.write(str(stats))
        
    # return "Data processed...."

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-folder','--folder', dest='folder', type=str, default='Y:/VIDEOS')
    args = parser.parse_args()
    
    root_path = os.getcwd()
    
    if os.path.exists(args.folder):
        add_drivers_to_json(args.folder, root_path+'/Datafiles/storage_stats.json')
        filling_driver_dates(args.folder, root_path+'/Datafiles/storage_stats.json')
    else:
        print(f'main(): Incorrect path entered => {args.folder}')
        exit()
    