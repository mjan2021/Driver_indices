#!/bin/bash

storage='data_storage.json'
root='Z:/VIDEOS/'

for id in 1001 1002 1005 1006 1009 1010
do
#  python .\LogExtraction.py -id $id -f $storage --vfolder $root$id/Video --lfolder $root$id/Disk_files/debug/
 echo "-id $id"
 echo "-f $storage"
 echo "--vfolder $root$id/Video/"
 echo "--lfolder $root$id/Disk_files/debug/"
# sleep 3
 wait
done
#python .\LogExtraction.py -id 2047 -f data_storage.json --vfolder Z:/VIDEOS/2047/Video/ --lfolder Z:/VIDEOS/2047/Disk_files/debug/