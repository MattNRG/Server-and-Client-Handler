import os
from configparser import ConfigParser
config = ConfigParser()
config.read('misc/settings.ini')

robotSettings = config['ROBOTS']
wifiSettings = config['WIFI']
visionSettings = config['VISION']

print('[CONFIG] Settings loaded')

def changeSetting(section, option, value):
    config.set(section, option, value)
    with open('misc/settings.ini', 'w') as configfile:
        config.write(configfile)
    print(f'[CONFIG] {section} {option} set to {value}')

# Notification function
# Source - https://stackoverflow.com/a/41318195
# Posted by Christopher Shroba, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-13, License - CC BY-SA 4.0
def message(title, text):
    if not os.name == 'posix': return
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
