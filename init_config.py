from configparser import ConfigParser

config = ConfigParser()

config['LAYOUT'] = {}
config['LAYOUT']['WIDTH'] = '2115'
config['LAYOUT']['HEIGHT'] = '1585'
config['LAYOUT']['PADDING_HOR'] = '55'
config['LAYOUT']['PADDING_TOP'] = '200'
config['LAYOUT']['PADDING_BOT'] = '40'
config['LAYOUT']['BACKGROUND'] = 'assets/bg-novogodniy-standart.png'

config['FOLDER'] = {}
config['FOLDER']['PATH'] = 'images/cropped'

config['BLOCK'] = {}
config['BLOCK']['MARGIN'] = '16'
config['BLOCK']['WIDTH'] = '200'
config['BLOCK']['HEIGHT'] = '170'

config['TEXT'] = {}
config['TEXT']['TITLE'] = '100'
config['TEXT']['NUMERATOR'] = '80'
config['TEXT']['INFO'] = '30'

config['FONT'] = {}
config['FONT']['MAIN'] = 'assets/fonts/OpenSans-ExtraBold.ttf'
config['FONT']['SECOND'] = 'assets/fonts/OpenSans-Bold.ttf'


with open('config.ini', 'w') as configfile:
  config.write(configfile)