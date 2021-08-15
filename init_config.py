from configparser import ConfigParser

config = ConfigParser()

config['LAYOUT'] = {}
config['LAYOUT']['WIDTH'] = '1754'
config['LAYOUT']['HEIGHT'] = '1240'

config['BLOCK'] = {}
config['BLOCK']['MARGIN'] = '10'
config['BLOCK']['WIDTH'] = '340'
config['BLOCK']['HEIGHT'] = '165'

config['FOLDER'] = {}
config['FOLDER']['NAME'] = 'images'

config['TEXT-SIZE'] = {}
config['TEXT-SIZE']['SIRE'] = '18'
config['TEXT-SIZE']['ENUM'] = '18'
config['TEXT-SIZE']['NAME'] = '22'
config['TEXT-SIZE']['DESC'] = '18'


with open('config.ini', 'w') as configfile:
  config.write(configfile)