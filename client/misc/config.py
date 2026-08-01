from configparser import ConfigParser
config = ConfigParser()
config.read('misc/settings.ini')

print(config.sections())

wifiSettings = config['WIFI']
selfSettings = config['SELF']

print('[CONFIG] Settings loaded')