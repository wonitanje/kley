from configparser import ConfigParser
from PIL import ImageFont
import default_constants as default
from db import DB

config = ConfigParser()
config.read('config.ini')

try: exists = config['FONT']
except: exists = False
if exists:
  FONT_MAIN = config['FONT'].get('MAIN', default.FONT_MAIN)
  FONT_SECOND = config['FONT'].get('SECOND', default.FONT_SECOND)
else:
  FONT_MAIN = default.FONT_MAIN
  FONT_SECOND = default.FONT_SECOND

try: exists = config['TEXT']
except: exists = False
if exists:
  TEXT = {}
  TEXT['TITLE'] = ImageFont.truetype(FONT_SECOND, int(config['TEXT'].get('TITLE', default.TITLE_SIZE)))
  TEXT['NUMB'] = ImageFont.truetype(FONT_MAIN, int(config['TEXT'].get('NUMERATOR', default.NUMERATOR_SIZE)))
  TEXT['INFO'] = ImageFont.truetype(FONT_MAIN, int(config['TEXT'].get('INFO', default.INFO_SIZE)))
else:
  TEXT = {
    'TITLE': ImageFont.truetype(FONT_MAIN, default.TITLE_SIZE),
    'NUMB': ImageFont.truetype(FONT_MAIN, default.NUMERATOR_SIZE),
    'INFO': ImageFont.truetype(FONT_MAIN, default.INFO_SIZE)
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
  LAYOUT_PADDING_TOP = int(config['LAYOUT'].get('PADDING_TOP', default.LAYOUT_PADDING_TOP))
  LAYOUT_PADDING_BOT = int(config['LAYOUT'].get('PADDING_BOT', default.LAYOUT_PADDING_BOT))
  LAYOUT_PADDING_HOR = int(config['LAYOUT'].get('PADDING_HOR', default.LAYOUT_PADDING_HOR))
  LAYOUT_BACKGROUND = config['LAYOUT'].get('BACKGROUND', default.LAYOUT_BACKGROUND)
  LAYOUT_DIRECTION = config['LAYOUT'].get('DIRECTION', default.LAYOUT_DIRECTION)
else:
  LAYOUT_WIDTH = default.LAYOUT_WIDTH
  LAYOUT_HEIGHT = default.LAYOUT_HEIGHT
  LAYOUT_PADDING_HOR = default.LAYOUT_PADDING_HOR
  LAYOUT_PADDING_TOP = default.LAYOUT_PADDING_TOP
  LAYOUT_PADDING_BOT = default.LAYOUT_PADDING_BOT
  LAYOUT_BACKGROUND = default.LAYOUT_BACKGROUND
  LAYOUT_DIRECTION = default.LAYOUT_DIRECTION

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

IMAGE_WIDTH = int(BLOCK_WIDTH)
TEXT_WIDTH = int(BLOCK_WIDTH)

HORIZONTAL_AMOUNT = (LAYOUT_WIDTH - LAYOUT_PADDING_HOR * 2) // BLOCK_WIDTH
VERTICAL_AMOUNT = (LAYOUT_HEIGHT - LAYOUT_PADDING_TOP - LAYOUT_PADDING_BOT) // BLOCK_HEIGHT
IMAGE_RESOLUTION = IMAGE_WIDTH / BLOCK_HEIGHT
LAYOUT_PADDING_HORIZONTAL = LAYOUT_PADDING_HOR #+ ((LAYOUT_WIDTH - LAYOUT_PADDING_HOR * 2) - BLOCK_WIDTH*HORIZONTAL_AMOUNT - HORIZONTAL_AMOUNT*BLOCK_MARGIN) // 2
LAYOUT_PADDING_TOP = LAYOUT_PADDING_TOP + ((LAYOUT_HEIGHT - LAYOUT_PADDING_TOP - LAYOUT_PADDING_BOT) - BLOCK_HEIGHT*VERTICAL_AMOUNT - VERTICAL_AMOUNT*BLOCK_MARGIN) // 2
LAYOUT_PADDING_BOT = LAYOUT_PADDING_BOT + ((LAYOUT_HEIGHT - LAYOUT_PADDING_TOP - LAYOUT_PADDING_BOT) - BLOCK_HEIGHT*VERTICAL_AMOUNT - VERTICAL_AMOUNT*BLOCK_MARGIN) // 2
DIRECTION = int(LAYOUT_DIRECTION == 'vertical')