import os
import pandas as pd
import shutil


# ===========================================
# For MacOS
# base_directory = '/Volumes/ivsdccoa/VIDEOS/'

# For Windows
base_directory = '/Volumes/ivsdccoa/VIDEOS/'
# ===========================================

juan = pd.read_csv('./GenderFilesSplitted/juan_replaced.csv')
alex = pd.read_csv('./GenderFilesSplitted/alex.csv')
tanveer = pd.read_csv('./GenderFilesSplitted/tanveer_replaced.csv')

#combine datafranes
df = pd.concat([juan, alex, tanveer], axis=0)
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
for index, row in filtered_df.iterrows():
    counter +=1
    gender = row['Verifyied']
    ID = "_".join(row['Combined'].split('_')[1:3])
    ID1 = row['Combined'].split('_')[1]
    ID2 = row['Combined'].split('_')[2]
    folder = row['Combined'].split('_')[3]
    filename = ".".join(row['Combined'].split('_')[4].split('.')[:-1])
    
    if int(ID1) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID1}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID1}_{gender}/Video/{folder}')
        
        src = f'{base_directory}{ID}/Video/{folder}/{filename}'
        dst = f'{base_directory}{ID1}_{gender}/Video/{folder}/{filename}' 
        shutil.copyfile(src, dst)   
        print(f'{counter}/{total_files} file -> {base_directory}{ID1}_{gender}/Video/{folder}/{filename}')
        

    elif int(ID2) in data[gender]:
        if not os.path.exists(f'{base_directory}{ID2}_{gender}/Video/{folder}'): 
            os.makedirs(f'{base_directory}{ID2}_{gender}/Video/{folder}')
        
        src = f'{base_directory}{ID}/Video/{folder}/{filename}'
        dst = f'file -> {base_directory}{ID2}_{gender}/Video/{folder}/{filename}'
        shutil.copyfile(src, dst)
        print(f'{counter}/{total_files} file -> {base_directory}{ID2}_{gender}/Video/{folder}/{filename}')
       
    g[gender] += 1
    # counter += 1
