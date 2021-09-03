from json import dumps
from configparser import ConfigParser

config = ConfigParser()

config['LAYOUT'] = {}
config['LAYOUT']['WIDTH'] = '3508'
config['LAYOUT']['HEIGHT'] = '2480'
config['LAYOUT']['PADDING_V'] = '170'
config['LAYOUT']['PADDING_H'] = '230'
config['LAYOUT']['BACKGROUND'] = 'assets/bg.png'

config['FOLDER'] = {}
config['FOLDER']['PATH'] = '../'

config['BLOCK'] = {}
config['BLOCK']['MARGIN'] = '16'
config['BLOCK']['WIDTH'] = '575'
config['BLOCK']['HEIGHT'] = '279'

config['IMAGE_TEXT'] = {}
config['IMAGE_TEXT']['MARGIN'] = '16'
config['IMAGE_TEXT']['RESOLUTION'] = '1:2'

config['TEXT'] = {}
config['TEXT']['MARGIN'] = '6'
config['TEXT']['SIRE'] = '25'
config['TEXT']['ENUM'] = '25'
config['TEXT']['NAME'] = '30'
config['TEXT']['DESC'] = '23'
config['TEXT']['NAME_MAX_LINES'] = '4'

config['FONT'] = {}
config['FONT']['MAIN'] = 'arial.ttf'
config['FONT']['ADD'] = 'assets/Lobster.ttf'


with open('config.ini', 'w') as configfile:
  config.write(configfile)