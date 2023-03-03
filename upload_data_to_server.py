import shutil
import os
import tqdm
import glob

src = 'K:/Videos/1040/'
dest = 'K:/Z/1122/'

# transfer Files to Server
def transferFilesToServer(src, dest):
    # files = glob.glob(src, recursive=True)
    for root, dirs, files in os.walk(src):
        root = "/".join(root.split('\\'))
        after_root = "/".join(root.split('/')[3:])
        for each_dir in dirs:
            if not os.path.exists(dest+after_root+each_dir):
                os.mkdir(dest+after_root+'/'+each_dir)
        
        for file in files:
            shutil.copy(root+'/'+file, dest+after_root+'/')
        
    return f'Total File : {print(len(os.listdir(dest)))}'

def validation_of_structure(src):
    files = os.listdir(src)
    if os.path.exists(src+'Video/827000/') or os.path.exists(src+'Video/984/'):
        return True

# transferFilesToServer(src, dest)

if __name__ == "__main__":
    src = ''
    os.listdir(src)
    transferFilesToServer(src, dest)