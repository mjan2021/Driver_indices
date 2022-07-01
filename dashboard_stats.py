import os
import glob
import metaData
import json
from tqdm import tqdm
#
# excluded_list = ['1003 1004-nonAI', '1005-nonAI']
# path = 'Z:/VIDEOS'
#
# driver_camera_files = glob.glob(path+'/*/Video/**/*000.asf')
# front_camera_files = glob.glob(path+'/*/Video/**/*100.asf')
#
# file_dict = {}
# with open('./Datafiles/test.json') as stats_file:
#     stats = json.load(stats_file)
# print(f"Total Drivers Before: {len(stats)}")



# This chunk of code add the driver ids as the list to the json file.
#
# driver_ids = os.listdir(path)
# for id in driver_ids:
#     if id not in excluded_list:
#         print(f"Processing driver: {id}")
#         for idx in range(0, len(stats)):
#             if stats[idx]['driver_id'] == id:
#                 stats.append({'driver_id': id, "data": []})
#                 dates = glob.glob('Z:/VIDEOS/' + id + '/Video/*')
#                 for date in dates:
#                     # print(f"Processing Date: {date}")
#                     date = date.split('\\')[-1]
#                     stats[-1]['data'].append({"date": date, "files": {}})

#
#
# combined_list = driver_camera_files + front_camera_files
# print(f"Total Files: {len(combined_list)}, DMS: {len(driver_camera_files)}, ADAS: {len(front_camera_files)}")
# for idx in tqdm(range(0, len(combined_list))):
#     filename = combined_list[idx].split("\\")
#     # print(filename)
#     driver_id = filename[1]
#     date = filename[3]
#     file = filename[4]
#     clean_filename = "/".join(filename)
#     size = os.path.getsize(clean_filename)
#     # print(stats)
#     # print(f"driver: {driver_id}, date: {date}, filename: {file}, size: {size/1048576}Mb")
#     for driver_idx in range(0, len(stats)):
#         # print(json_idx['driver_id'])
#         if stats[driver_idx]['driver_id'] == driver_id:
#             for date_idx in range(0, len(stats[driver_idx]['data'])):
#                 if stats[driver_idx]['data'][date_idx]['date'] == date:
#                     stats[driver_idx]['data'][date_idx]['files'][file] = size/1048576
#
#
# print(f"Total Driver After: {len(stats)}, \n {stats}")
# with open('./Datafiles/test.json', 'w') as json_f:
#     json.dump(stats, json_f)

# print(f"{driver_ids}")
#
def add_drivers_to_json(main_data_folder, json_file_path):
    excluded_list = ['1003 1004-nonAI', '1005-nonAI']
    driver_ids = os.listdir(main_data_folder)
    with open(json_file_path) as json_file:
        stats = json.load(json_file)

    # for id in driver_ids:
    #     if id not in excluded_list:
    #         print(f"Processing driver: {id}")
    #         stats.append({'driver_id': id, "data": []})
    #         for idx in range(0, len(stats)):
    #             # if stats[idx]['driver_id'] == id:
    #             #     # stats.append({'driver_id': id, "data": []})
    #             dates = glob.glob('Z:/VIDEOS/' + id + '/Video/*')
    #             for date in dates:
    #                 # print(f"Processing Date: {date}")
    #                 date = date.split('\\')[-1]
    #                 stats[idx]['data'].append({"date": date, "files": {}})
    #             del dates
    #

    for id in range(0, len(driver_ids)):
        if driver_ids[id] not in excluded_list:
            print(f"Processing driver: {driver_ids[id]}")
            # condition must be inserted to check if the jsonfile have the driverID already
            # if id_from_json in json[index]['driver_id]
            #   not working -----
            stats.append({'driver_id': driver_ids[id], "data": []})
            dates = glob.glob('Z:/VIDEOS/' + driver_ids[id] + '/Video/*')
            for date in dates:
                # print(f"Processing Date: {date}")
                date = date.split('\\')[-1]
                stats[-1]['data'].append({"date": date, "files": {}})
            del dates

    print(stats)
    with open(json_file_path, 'w') as json_f:
        json.dump(stats, json_f)

    return "Total Drivers Added: "+str(len(stats))

def filling_driver_dates(path, json_file):

    driver_camera_files = glob.glob(path + '/*/Video/**/*000.asf')
    front_camera_files = glob.glob(path + '/*/Video/**/*100.asf')

    file_dict = {}
    with open(json_file) as stats_file:
        stats = json.load(stats_file)
    print(f"Total Drivers: {len(stats)}")

    combined_list = driver_camera_files + front_camera_files
    print(f"Total Files: {len(combined_list)}, DMS: {len(driver_camera_files)}, ADAS: {len(front_camera_files)}")
    for idx in tqdm(range(0, len(combined_list))):
        filename = combined_list[idx].split("\\")
        # print(filename)
        driver_id = filename[1]
        date = filename[3]
        file = filename[4]
        clean_filename = "/".join(filename)
        size = os.path.getsize(clean_filename)
        # print(stats)
        # print(f"driver: {driver_id}, date: {date}, filename: {file}, size: {size/1048576}Mb")
        for driver_idx in range(0, len(stats)):
            # print(json_idx['driver_id'])
            if stats[driver_idx]['driver_id'] == driver_id:
                for date_idx in range(0, len(stats[driver_idx]['data'])):
                    if stats[driver_idx]['data'][date_idx]['date'] == date:
                        stats[driver_idx]['data'][date_idx]['files'][file] = size / 1048576

    print(f"Total Driver: {len(stats)}")
    with open(json_file, 'w') as json_f:
        json.dump(stats, json_f)
    return "Data processed...."

# Run this first
# add_drivers_to_json('Z:/VIDEOS', './Datafiles/storage_stats.json')
#
# then Run this second seperately
filling_driver_dates('Z:/VIDEOS', 'Datafiles/storage_stats.json')