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

config['FONT-SIZE'] = {}
config['FONT-SIZE']['SIZE'] = '18'
config['FONT-SIZE']['NAME'] = '22'
config['FONT-SIZE']['DESC'] = '18'


with open('config.ini', 'w') as configfile:
  config.write(configfile)