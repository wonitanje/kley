from configparser import ConfigParser
from PIL import ImageFont

config = ConfigParser()
config.read('config.ini')

FONT = {}
FONT['SIRE'] = ImageFont.truetype('arial.ttf', int(config['FONT-SIZE'].get('SIRE', 18)))
FONT['NAME'] = ImageFont.truetype('arial.ttf', int(config['FONT-SIZE'].get('NAME', 22)))
FONT['DESC'] = ImageFont.truetype('arial.ttf', int(config['FONT-SIZE'].get('DESC', 18)))

FOLDER_NAME = config['FOLDER'].get('NAME', '')

LAYOUT_WIDTH = int(config['LAYOUT'].get('WIDTH', 1754))
LAYOUT_HEIGHT = int(config['LAYOUT'].get('HEIGHT', 1240))

BLOCK_MARGIN = int(config['BLOCK'].get('MARGIN', 10))
BLOCK_HEIGHT = int(config['BLOCK'].get('HEIGHT', 165))
BLOCK_WIDTH = int(config['BLOCK'].get('WIDTH', 340))
IMAGE_WIDTH = TEXT_WIDTH = BLOCK_WIDTH // 2

HORIZONTAL_AMOUNT = LAYOUT_WIDTH // BLOCK_WIDTH
VERTICAL_AMOUNT = LAYOUT_HEIGHT // BLOCK_HEIGHT
IMAGE_RESOLUTION = IMAGE_WIDTH / BLOCK_HEIGHT
LAYOUT_PADDING_HORIZONTAL = (LAYOUT_WIDTH - BLOCK_WIDTH*HORIZONTAL_AMOUNT - HORIZONTAL_AMOUNT*BLOCK_MARGIN) // 2
LAYOUT_PADDING_VERTICAL = (LAYOUT_HEIGHT - BLOCK_HEIGHT*VERTICAL_AMOUNT - VERTICAL_AMOUNT*BLOCK_MARGIN) // 2