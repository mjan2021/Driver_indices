### Driver Indices Extraction

This package extract information from the log files of the mdvr and upload it to the webserver. 

To run the extraction process use below command in terminal 

``python LogExtraction.py --id driver_id -f json_folder --vfolder Video_folder --lfolder logfiles_folder``

where: 

``--id`` is the driver ID

``-f`` is the path for json file where all the data is stored

``--vfolder`` is the path for that driver videos folder

``--lfolder`` is the path for the logfiles folder of that driver.

#### Running the Web Server
To run the web server use the following command

``python web_server.py`` and the navigate to [127.0.0.1:5000](127.0.0.1:5000)

