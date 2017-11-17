# CodeSchool-Downloader
This is a python code that helps you to download all videos from [Code School](https://www.codeschool.com/).

If you have any question feel free to contact me at `sudo.liyang [at] gmail.com`.

# Donations
Bitcoin address: `1N5EoxpR9w5mdG7WBbThA96hx6bu6QoNbh`

## Demo 

[![See video](http://i.imgur.com/bLdUpUq.png)](https://www.youtube.com/watch?v=TqvQNQtWhdU)

# Requirement

*   [Code School Membership](https://www.codeschool.com/pricing) 
*   Python 2.7
*   [pip](https://pypi.python.org/pypi/pip) 
*   Firefox


# Usage 

### Prepare 
Install dependency 

        $ pip install -r requirement.txt

Configure user and password, edit parsing_courses_to_json.py or parsing_screencasts_to_json.py file, add your Username and Password in the code.
```python
        Username = "your_username"
        Password = "your_password"
```

### Parsing
Parsing courses or screencasts video direct url to json
and it will open Firefox and auto parse videos, when it finished it will output in current path as courses.json or screencasts.json.

        $ python parsing_courses_to_json.py
        $ python parsing_screencasts_to_json.py


### Downloading
When you finished parsing, just run download_courses.py or download_screencasts.py to downloading videos 

        $ python download_courses.py
        $ python download_screencasts.py
