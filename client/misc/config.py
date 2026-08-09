from configparser import ConfigParser
config = ConfigParser()
configLocation = 'misc/settings.ini'

if __name__ == '__main__':
    configLocation = 'settings.ini'

config.read(configLocation)

print(config.sections())

wifiSettings = config['WIFI']
selfSettings = config['SELF']

print('[CONFIG] Settings loaded')

def editConfig(section, option, value):
    config.set(section, option, value)

    with open(configLocation, 'w') as configfile:
        config.write(configfile)
    
    print(f'[CONFIG] {section} {option} set to {value}')

