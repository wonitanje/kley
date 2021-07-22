from configparser import ConfigParser

config = ConfigParser()

config['LAYOUT'] = {}
config['LAYOUT']["WIDTH"] = '1754'
config['LAYOUT']["HEIGHT"] = '1240'
config['IMAGE'] = {}
config['IMAGE']["MARGIN"] = '10'
config['IMAGE']["WIDTH"] = '185'
config['IMAGE']["HEIGHT"] = '165'

with open('config.ini', 'w') as configfile:
  config.write(configfile)