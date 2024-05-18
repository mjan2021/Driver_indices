import os
import pandas as pd
import shutil


# ===========================================
# For MacOS
# base_directory = '/Volumes/ivsdccoa/VIDEOS/'

# For Windows
base_directory = 'Y:/VIDEOS/'
# ===========================================

juan = pd.read_csv('./GenderFilesSplitted/juan_replaced.csv')
alex = pd.read_csv('./GenderFilesSplitted/alex.csv')
tanveer = pd.read_csv('./GenderFilesSplitted/tanveer_replaced.csv')
csv_3500 = pd.read_csv('./GenderFilesSplitted/gender_3500.csv')
#combine datafranes
df = pd.concat([juan, alex, tanveer, csv_3500], axis=0)
df['Verifyied'].replace({'f':'female', 'm':'male'}, inplace=True)
# print(df['Verifyied'].value_counts())
filtered_df = df[df['Verifyied'].isin(['male', 'female'])]
print(filtered_df['Verifyied'].value_counts())

data = {
    'male': [1004, 1010, 1012, 1013, 1031, 1044, 1055, 1070, 1075, 1099, 1112, 1135],
    'female': [1003, 1009, 1011, 1014, 1017, 1043, 1056, 1071, 1074, 1100, 1113, 1134]
}

print(filtered_df.head())
print(filtered_df['Verifyied'].value_counts())

# Iterate over DataFrame rows
counter = 0
total_files = len(filtered_df['Combined'])
g = {'male': 0, 'female': 0}
copiedFiles = open('copiedFiles.txt', 'w+')
copiedFilesList = copiedFiles.readlines()
filesNotFound = open('filesNotFound.txt', 'w+')
for index, row in filtered_df.iterrows():
    counter +=1
    gender = row['Verifyied']
    ID = "_".join(row['Combined'].split('_')[1:3])
    ID1 = row['Combined'].split('_')[1]
    ID2 = row['Combined'].split('_')[2]
    folder = row['Combined'].split('_')[3]
    filename = ".".join(row['Combined'].split('_')[4].split('.')[:-1])
    file_front = f'{filename[:-8]}0100.asf'
    
    # if f'{base_directory}{ID}/Video/{folder}/{file_front}\n' not in copiedFilesList:
    #     print()
    
    if int(ID1) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID1}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID1}_{gender}/Video/{folder}')
        
        src = f'{base_directory}{ID}/Video/{folder}/{filename}'
        dst = f'{base_directory}{ID1}_{gender}/Video/{folder}/{filename}'
        try:
            if not os.path.exists(dst):
                shutil.copyfile(src, dst)
        
        except Exception as e:
            if dst+'\n' in copiedFilesList:
                print(f'========= File Already Copied: ========= ')
                
            else: 
                print(f'========= File Not Found: ========= ')
                filesNotFound.write(f'{src}\n')
                continue
        print(f'{counter}/{total_files} file -> {base_directory}{ID1}_{gender}/Video/{folder}/{filename}')
        # break

    elif int(ID2) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID2}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID2}_{gender}/Video/{folder}')
        
        src = f'{base_directory}{ID}/Video/{folder}/{filename}'
        dst = f'{base_directory}{ID2}_{gender}/Video/{folder}/{filename}'
        
        try:
            if not os.path.exists(dst):
                shutil.copyfile(src, dst)
        
        except Exception as e:
            if dst+'\n' in copiedFilesList:
                print(f'========= File Already Copied: ========= ')
            else:
                    
                print(f'========= File Not Found: ========= ')
                filesNotFound.write(f'{src}\n')
                continue
        print(f'{counter}/{total_files} file -> {base_directory}{ID2}_{gender}/Video/{folder}/{filename}')
        # break
    if dst+'\n' not in copiedFilesList:
        copiedFiles.write(f'{dst}\n')
    
    g[gender] += 1
    # counter += 1

filesNotFound.close()
copiedFiles.close()
