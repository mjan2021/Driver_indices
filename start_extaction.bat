@echo off
setlocal enabledelayedexpansion

set "script_dir=%~dp0"
set "parent_directory=Y:\VIDEOS"
set "python_script=%script_dir%LogExtraction.py"
set "json_file=%script_dir%data_storage.json"
set "base_video_folder=%parent_directory%"
set "skip_list=1003 1004-nonAI 1005-nonAI 1082 1094 2062"

if not exist "%python_script%" (
    echo Error: Python script not found: "%python_script%"
    exit /b 1
)

if not exist "%json_file%" (
    echo Error: JSON file not found: "%json_file%"
    exit /b 1
)

set "python_cmd=python"
%python_cmd% --version >nul 2>&1
if errorlevel 1 (
    set "python_cmd=py -3"
    py -3 --version >nul 2>&1
    if errorlevel 1 (
        echo Error: Python was not found on PATH and py -3 is not available.
        exit /b 1
    )
)

if not exist "%parent_directory%" (
    echo Error: Video root not found: "%parent_directory%"
    exit /b 1
)

for /d %%f in ("%parent_directory%\*") do (
    set "folder_name=%%~nxf"
    set "vfolder=%%~ff\Video"
    set "lfolder=%%~ff\Disk_files\debug"
    echo Processing folder: "!folder_name!"

    echo "!skip_list!" | findstr /i /c:"!folder_name!" >nul
    if errorlevel 1 (
        if exist "!vfolder!\" (
            if exist "!lfolder!\" (
                call %python_cmd% "%python_script%" --id "!folder_name!" -f "%json_file%" --vfolder "!vfolder!" --lfolder "!lfolder!"
            ) else (
                echo Skipping folder because log folder is missing: "!folder_name!"
            )
        ) else (
            echo Skipping folder because video folder is missing: "!folder_name!"
        )
    ) else (
        echo Skipping folder: "!folder_name!"
    )
)

endlocal


