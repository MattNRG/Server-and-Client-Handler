import os
from configparser import ConfigParser
config = ConfigParser()
config.read('misc/settings.ini')

robotSettings = config['ROBOTS']
wifiSettings = config['WIFI']
visionSettings = config['VISION']

print('[CONFIG] Settings loaded')

def message(title, text):
    if not os.name == 'posix': return
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
