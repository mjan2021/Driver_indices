@echo off
setlocal enabledelayedexpansion

rem Set the parent directory where you have subdirectories with folder names
set "parent_directory=Y:\VIDEOS"

rem Set the Python script path
set "python_script=.\LogExtraction.py"

rem Set the JSON file path
set "json_file=data_storage.json"

rem Set the base video folder path
set "base_video_folder=Y:\VIDEOS"

rem Define a list of folder names to skip (separate folder names with spaces)
set "skip_list=1003 1004-nonAI 1005-nonAI 1082 1094 2062"

rem Loop through subdirectories in the parent directory
for /d %%f in ("%parent_directory%\*") do (
    set "folder_name=%%~nxf"
    set "vfolder=!base_video_folder!\!folder_name!\Video"
    set "lfolder=!base_video_folder!\!folder_name!\Disk_files\debug"
    echo Processing folder: "!folder_name!"
    rem Check if the current folder_name is in the skip list
    echo "!skip_list!" | findstr /i /c:"!folder_name!" >nul
    if errorlevel 1 (
        rem Run the Python command for each subdirectory
        start /wait python "%python_script%" --id "!folder_name!" -f "%json_file%" --vfolder "!vfolder!" --lfolder "!lfolder!"
    ) else (
        echo Skipping folder: "!folder_name!"
    )
)
endlocal
