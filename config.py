from configparser import ConfigParser
config = ConfigParser()
config.read('settings.ini')

robotSettings = config['ROBOTS']
wifiSettings = config['WIFI']
visionSettings = config['VISION']
