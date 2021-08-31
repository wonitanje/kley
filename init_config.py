from json import dumps
from configparser import ConfigParser

config = ConfigParser()

config['LAYOUT'] = {}
config['LAYOUT']['WIDTH'] = '1754'
config['LAYOUT']['HEIGHT'] = '1240'

config['BLOCK'] = {}
config['BLOCK']['MARGIN'] = '10'
config['BLOCK']['WIDTH'] = '340'
config['BLOCK']['HEIGHT'] = '165'

config['IMAGE_TEXT'] = {}
config['IMAGE_TEXT']['MARGIN'] = '10'
config['IMAGE_TEXT']['RESOLUTION'] = '1:2'

config['FOLDER'] = {}
config['FOLDER']['PATH'] = './'

config['TEXT'] = {}
config['TEXT']['MARGIN'] = '4'
config['TEXT']['SIRE'] = '15'
config['TEXT']['ENUM'] = '15'
config['TEXT']['NAME'] = '18'
config['TEXT']['DESC'] = '14'


with open('config.ini', 'w') as configfile:
  config.write(configfile)