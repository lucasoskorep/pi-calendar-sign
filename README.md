# Pi Calendar Sign

Assumes python3 as the base:
* python -m venv ./venv
* pip install -r requirements.txt
* sudo pip install adafruit-circuitpython-charlcd
* create your .auth.json file with a corresponding API key from GCP
* edit config.json to have a list of all the emails you want to track
* edit pi-calendar-sign.py to have the calendar names that you would like to receive events for. 
* python pi-calendar-sign.py
