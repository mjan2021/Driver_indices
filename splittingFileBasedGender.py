
import json
import os
import fnmatch
import shutil
import tqdm



# find all occurence of a item in a list
def find_all_occurence(list, item):
    return [i for i, x in enumerate(list) if x == item]


def Copy_gender_files_into_seperate_folders(txtfile, participantId, gender, rootFolder):
    """
    Description: This function copies all files from a list of files into a seperate folder
    
    :param 
        txtfile: txt file containing the list of files
        participantId: Seperate Id of the participant
        gender:  gender of the participant
        rootFolder: root folder containing all files
    
    :return
        None
    """

    # root_folder = 'Z:/VIDEOS/1013 1014/'
    root_folder = rootFolder
    test_folder = f'Y:/VIDEOS/{participantId}_{gender}/'
    
    print(f'==========Creating seperate directories for participants ====================================================')
    if os.path.exists(test_folder):
        print('Test Folder Exists')
    else:
        os.mkdir(test_folder)
        print('Test Folder Created')
        
    root_folder = 'Z:/VIDEOS/1013 1014/'

    # check For Main folders
    if os.path.exists(test_folder+'Video/'):
        print('Video Folder Exists')
    else:
        os.mkdir(test_folder+'Video/')
        print('Video Folder Created')

    if os.path.exists(test_folder+'Disk_files/'):
        print('Disk Folder Exists')
    else:
        os.mkdir(test_folder+'Disk_files/')
        print('Disk Folder Created')
    
    print(f'==========Directories created================================================================================')

    debug = os.listdir(root_folder+'Disk_files/debug/')

    debug_files = set()

    # Read the txtFile for gender
    with open(txtfile) as f:
        list_of_files = json.load(f)

    # print(f'Copying Video Files: {len(list_of_files[0])+len(list_of_files[1])}')
    counter = 0
    for file in list_of_files:
        counter += 1 
        print(f'Current Object : {counter}/{len(list_of_files)}')
        for file, gdr in tqdm.tqdm(file.items()):
            front_camera = ''
            if gdr == gender:
                sep_date = file.split('/')[4]
                date = "".join(file.split('/')[4].split("-"))
                time = "".join(list(file.split('/')[5])[1:7])
                
                matches = fnmatch.filter(debug, f'dbglog-{date}-*.log')
                debug_files.update(matches)
                # print(f'{file} : {matches}')
                
                path = '/'.join(file.split('/')[:-1])
                name = list(file.split('/')[-1].split('.')[0])[:-3]
                front_camera = path+'/'+"".join(name)+str('100.asf')
                
                # copying the video files
                if os.path.exists(test_folder+'Video/'+sep_date):
                    shutil.copy(file, test_folder+'Video/'+sep_date)
                    try:
                        shutil.copy(front_camera, test_folder+'Video/'+sep_date)
                    except FileNotFoundError:
                        with open('error.txt', 'a') as f:
                            f.write(str(front_camera)+'\n')
                    
                else:
                    os.mkdir(test_folder+'Video/'+sep_date)
                    shutil.copy(file, test_folder+'Video/'+sep_date)
                    try:
                        shutil.copy(front_camera, test_folder+'Video/'+sep_date)
                    except FileNotFoundError:
                        with open('error.txt', 'a') as f:
                            f.write(str(front_camera)+'\n')

    # copy debug files to test folder
    print(f'Copying Debug Files: {len(debug_files)}')
    for debug_file in tqdm.tqdm(debug_files):
        if os.path.exists(test_folder+'Disk_files/debug/'):
            shutil.copy(root_folder+'Disk_files/debug/'+debug_file, test_folder+'Disk_files/debug/')
        else:
            os.mkdir(test_folder+'Disk_files/debug/')
            shutil.copy(root_folder+'Disk_files/debug/'+debug_file, test_folder+'Disk_files/debug/')

if __name__ == "__main__":
    Copy_gender_files_into_seperate_folders(txtfile='gender_1013_1014.txt', participantId='1013', gender='male', rootFolder='Z:/VIDEOS/1013 1014/')