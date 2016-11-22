# Code-School-Downloader
This is a python code that helps you to download [Code School](codeschool.com) courses and screencasts videos.


# Requirement

*   [Code School Membership](https://www.codeschool.com/pricing) 
*   Python 2.7
*   [pip](https://pypi.python.org/pypi/pip) 
*   Firefox


# Usage 
Install dependency 

        pip install -r requirement.txt


### Parsing
Parsing courses or screencasts video direct url to json
and it will open Firefox and auto parsing videos, when it finished it will output in current path as courses.json or screencasts.json.

        python parsing_courses_to_json.py
        python parsing_screencasts_to_json.py


### Downloading
when you finished parsing, just run download_courses.py or download_screencasts.py to downloading videos 


        python download_courses.py
        python download_screencasts.py