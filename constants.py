from configparser import ConfigParser
from PIL import ImageFont
import json
import default_constants as default

with open('db.json', 'r', encoding='1251') as json_file:
  DB = json.load(json_file)

config = ConfigParser()
config.read('config.ini')

try: exists = config['TEXT']
except: exists = False
if exists:
  TEXT = {}
  TEXT['SIRE'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('SIRE', default.SIRE_SIZE)))
  TEXT['ENUM'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('ENUM', default.ENUM_SIZE)))
  TEXT['NAME'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('NAME', default.NAME_SIZE)))
  TEXT['DESC'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('DESC', default.DESC_SIZE)))
  TEXT_MARGIN = int(config['TEXT'].get('MARGIN', 4))
else:
  TEXT = {
    'SIRE': default.SIRE_SIZE,
    'ENUM': default.ENUM_SIZE,
    'NAME': default.NAME_SIZE,
    'DESC': default.DESC_SIZE
  }


try:
  FOLDER_PATH = config['FOLDER'].get('PATH', default.FOLDER_PATH)
except:
  FOLDER_PATH = default.FOLDER_PATH


try: exists = config['LAYOUT']
except: exists = False
if exists:
  LAYOUT_WIDTH = int(config['LAYOUT'].get('WIDTH', default.LAYOUT_WIDTH))
  LAYOUT_HEIGHT = int(config['LAYOUT'].get('HEIGHT', default.LAYOUT_HEIGHT))
else:
  LAYOUT_WIDTH = default.LAYOUT_WIDTH
  LAYOUT_HEIGHT = default.LAYOUT_HEIGHT


try: exists = config['BLOCK']
except: exists = False
if exists:
  BLOCK_MARGIN = int(config['BLOCK'].get('MARGIN', default.BLOCK_MARGIN))
  BLOCK_HEIGHT = int(config['BLOCK'].get('HEIGHT', default.BLOCK_HEIGHT))
  BLOCK_WIDTH = int(config['BLOCK'].get('WIDTH', default.BLOCK_WIDTH))
else:
  BLOCK_MARGIN = default.BLOCK_MARGIN
  BLOCK_HEIGHT = default.BLOCK_HEIGHT
  BLOCK_WIDTH = default.BLOCK_WIDTH


try: exists = config['IMAGE_TEXT']
except: exists = False
if exists:
  IMAGE_TEXT_MARGIN = int(config['IMAGE_TEXT'].get('MARGIN', default.IMAGE_TEXT_MARGIN))
  IMAGE_TEXT_RESOLUTION = list(map(int, config['IMAGE_TEXT'].get('RESOLUTION', default.IMAGE_TEXT_RESOLUTION).split(':')))
else:
  IMAGE_TEXT_MARGIN = default.IMAGE_TEXT_MARGIN
  IMAGE_TEXT_RESOLUTION = default.IMAGE_TEXT_RESOLUTION


IMAGE_TEXT_RESOLUTION.append(IMAGE_TEXT_RESOLUTION[0] + IMAGE_TEXT_RESOLUTION[1])
IMAGE_WIDTH = int(BLOCK_WIDTH / IMAGE_TEXT_RESOLUTION[2] * IMAGE_TEXT_RESOLUTION[0] - IMAGE_TEXT_MARGIN // 2)
TEXT_WIDTH = int(BLOCK_WIDTH / IMAGE_TEXT_RESOLUTION[2] * IMAGE_TEXT_RESOLUTION[1] - IMAGE_TEXT_MARGIN // 2)

HORIZONTAL_AMOUNT = LAYOUT_WIDTH // BLOCK_WIDTH
VERTICAL_AMOUNT = LAYOUT_HEIGHT // BLOCK_HEIGHT
IMAGE_RESOLUTION = IMAGE_WIDTH / BLOCK_HEIGHT
LAYOUT_PADDING_HORIZONTAL = (LAYOUT_WIDTH - BLOCK_WIDTH*HORIZONTAL_AMOUNT - HORIZONTAL_AMOUNT*BLOCK_MARGIN) // 2
LAYOUT_PADDING_VERTICAL = (LAYOUT_HEIGHT - BLOCK_HEIGHT*VERTICAL_AMOUNT - VERTICAL_AMOUNT*BLOCK_MARGIN) // 2