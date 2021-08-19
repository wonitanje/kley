from configparser import ConfigParser
from PIL import ImageFont
import json

with open('db.json', 'r', encoding='1251') as json_file:
  DB = json.load(json_file)

config = ConfigParser()
config.read('config.ini')

TEXT = {}
TEXT['SIRE'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('SIRE', 16)))
TEXT['ENUM'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('ENUM', 16)))
TEXT['NAME'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('NAME', 19)))
TEXT['DESC'] = ImageFont.truetype('arial.ttf', int(config['TEXT'].get('DESC', 15)))
TEXT_MARGIN = int(config['TEXT'].get('MARGIN', 4))

FOLDER_PATH = config['FOLDER'].get('PATH', './')

LAYOUT_WIDTH = int(config['LAYOUT'].get('WIDTH', 1754))
LAYOUT_HEIGHT = int(config['LAYOUT'].get('HEIGHT', 1240))

BLOCK_MARGIN = int(config['BLOCK'].get('MARGIN', 10))
BLOCK_HEIGHT = int(config['BLOCK'].get('HEIGHT', 165))
BLOCK_WIDTH = int(config['BLOCK'].get('WIDTH', 340))

IMAGE_TEXT_MARGIN = int(config['IMAGE_TEXT'].get('MARGIN', '10'))
IMAGE_TEXT_RESOLUTION = list(map(int, config['IMAGE_TEXT'].get('RESOLUTION', '1:2').split(':')))
IMAGE_TEXT_RESOLUTION.append(IMAGE_TEXT_RESOLUTION[0] + IMAGE_TEXT_RESOLUTION[1])
IMAGE_WIDTH = int(BLOCK_WIDTH / IMAGE_TEXT_RESOLUTION[2] * IMAGE_TEXT_RESOLUTION[0] - IMAGE_TEXT_MARGIN // 2)
TEXT_WIDTH = int(BLOCK_WIDTH / IMAGE_TEXT_RESOLUTION[2] * IMAGE_TEXT_RESOLUTION[1] - IMAGE_TEXT_MARGIN // 2)

HORIZONTAL_AMOUNT = LAYOUT_WIDTH // BLOCK_WIDTH
VERTICAL_AMOUNT = LAYOUT_HEIGHT // BLOCK_HEIGHT
IMAGE_RESOLUTION = IMAGE_WIDTH / BLOCK_HEIGHT
LAYOUT_PADDING_HORIZONTAL = (LAYOUT_WIDTH - BLOCK_WIDTH*HORIZONTAL_AMOUNT - HORIZONTAL_AMOUNT*BLOCK_MARGIN) // 2
LAYOUT_PADDING_VERTICAL = (LAYOUT_HEIGHT - BLOCK_HEIGHT*VERTICAL_AMOUNT - VERTICAL_AMOUNT*BLOCK_MARGIN) // 2