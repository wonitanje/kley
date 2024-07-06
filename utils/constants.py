from configparser import ConfigParser
from PIL import ImageFont
import utils.default_constants as default

config = ConfigParser()
config.read("config.ini")

try:
    PRIMARY_FONT = config["FONT"].get("MAIN", default.PRIMARY_FONT)
    SECOND_FONT = config["FONT"].get("ADD", default.PRIMARY_FONT)
except:
    PRIMARY_FONT = default.PRIMARY_FONT
    SECOND_FONT = default.SECOND_FONT

try:
    exists = config["TEXT"]
except:
    exists = False
if exists:
    TEXT = {}
    TEXT["SIRE"] = ImageFont.truetype(
        PRIMARY_FONT, int(config["TEXT"].get("SIRE", default.SIRE_SIZE))
    )
    TEXT["ENUM"] = ImageFont.truetype(
        PRIMARY_FONT, int(config["TEXT"].get("ENUM", default.ENUM_SIZE))
    )
    TEXT["NAME"] = ImageFont.truetype(
        PRIMARY_FONT, int(config["TEXT"].get("NAME", default.NAME_SIZE))
    )
    TEXT["DESC"] = ImageFont.truetype(
        PRIMARY_FONT, int(config["TEXT"].get("DESC", default.DESC_SIZE))
    )
    TEXT["NUMB"] = ImageFont.truetype(
        PRIMARY_FONT, int(config["TEXT"].get("NUMERATOR", default.NUMERATOR_SIZE))
    )
    TEXT["INFO"] = ImageFont.truetype(
        PRIMARY_FONT, int(config["TEXT"].get("INFO", default.INFO_SIZE))
    )
    TEXT["AREA"] = ImageFont.truetype(SECOND_FONT, 40)
    TEXT_MARGIN = int(config["TEXT"].get("MARGIN", default.TEXT_MARGIN))
    NAME_LINES = int(config["TEXT"].get("NAME_MAX_LINES", default.NAME_LINES))
else:
    TEXT = {
        "SIRE": ImageFont.truetype(PRIMARY_FONT, default.SIRE_SIZE),
        "ENUM": ImageFont.truetype(PRIMARY_FONT, default.ENUM_SIZE),
        "NAME": ImageFont.truetype(PRIMARY_FONT, default.NAME_SIZE),
        "DESC": ImageFont.truetype(PRIMARY_FONT, default.DESC_SIZE),
        "NUMB": ImageFont.truetype(SECOND_FONT, default.NUMERATOR_SIZE),
        "INFO": ImageFont.truetype(SECOND_FONT, default.INFO_SIZE),
        "AREA": ImageFont.truetype(SECOND_FONT, 40),
    }
    TEXT_MARGIN = default.TEXT_MARGIN
    NAME_LINES = default.NAME_LINES

try:
    FOLDER_PATH = config["FOLDER"].get("PATH", default.FOLDER_PATH)
except:
    FOLDER_PATH = default.FOLDER_PATH


try:
    exists = config["LAYOUT"]
except:
    exists = False
if exists:
    LAYOUT_WIDTH = int(config["LAYOUT"].get("WIDTH", default.LAYOUT_WIDTH))
    LAYOUT_HEIGHT = int(config["LAYOUT"].get("HEIGHT", default.LAYOUT_HEIGHT))
    LAYOUT_PADDING_TOP = int(
        config["LAYOUT"].get("PADDING_TOP", default.LAYOUT_PADDING_TOP)
    )
    LAYOUT_PADDING_BOT = int(
        config["LAYOUT"].get("PADDING_BOT", default.LAYOUT_PADDING_BOT)
    )
    LAYOUT_PADDING_H = int(config["LAYOUT"].get("PADDING_H", default.LAYOUT_PADDING_H))
    LAYOUT_BACKGROUND = config["LAYOUT"].get(
        "LAYOUT_BACKGROUND", default.LAYOUT_BACKGROUND
    )
else:
    LAYOUT_WIDTH = default.LAYOUT_WIDTH
    LAYOUT_HEIGHT = default.LAYOUT_HEIGHT
    LAYOUT_PADDING_H = default.LAYOUT_PADDING_H
    LAYOUT_PADDING_TOP = default.LAYOUT_PADDING_TOP
    LAYOUT_PADDING_BOT = default.LAYOUT_PADDING_BOT
    LAYOUT_BACKGROUND = default.LAYOUT_BACKGROUND


try:
    exists = config["BLOCK"]
except:
    exists = False
if exists:
    BLOCK_MARGIN = int(config["BLOCK"].get("MARGIN", default.BLOCK_MARGIN))
    BLOCK_HEIGHT = int(config["BLOCK"].get("HEIGHT", default.BLOCK_HEIGHT))
    BLOCK_WIDTH = int(config["BLOCK"].get("WIDTH", default.BLOCK_WIDTH))
else:
    BLOCK_MARGIN = default.BLOCK_MARGIN
    BLOCK_HEIGHT = default.BLOCK_HEIGHT
    BLOCK_WIDTH = default.BLOCK_WIDTH


try:
    exists = config["IMAGE_TEXT"]
except:
    exists = False
if exists:
    IMAGE_TEXT_MARGIN = int(
        config["IMAGE_TEXT"].get("MARGIN", default.IMAGE_TEXT_MARGIN)
    )
    IMAGE_TEXT_RESOLUTION = list(
        map(
            int,
            config["IMAGE_TEXT"]
            .get("RESOLUTION", default.IMAGE_TEXT_RESOLUTION)
            .split(":"),
        )
    )
else:
    IMAGE_TEXT_MARGIN = default.IMAGE_TEXT_MARGIN
    IMAGE_TEXT_RESOLUTION = default.IMAGE_TEXT_RESOLUTION


IMAGE_TEXT_RESOLUTION.append(IMAGE_TEXT_RESOLUTION[0] + IMAGE_TEXT_RESOLUTION[1])
IMAGE_WIDTH = int(
    BLOCK_WIDTH / IMAGE_TEXT_RESOLUTION[2] * IMAGE_TEXT_RESOLUTION[0]
    - IMAGE_TEXT_MARGIN // 2
)
TEXT_WIDTH = int(
    BLOCK_WIDTH / IMAGE_TEXT_RESOLUTION[2] * IMAGE_TEXT_RESOLUTION[1]
    - IMAGE_TEXT_MARGIN // 2
)

HORIZONTAL_AMOUNT = (LAYOUT_WIDTH - LAYOUT_PADDING_H * 2) // BLOCK_WIDTH
VERTICAL_AMOUNT = (
    LAYOUT_HEIGHT - LAYOUT_PADDING_TOP - LAYOUT_PADDING_BOT
) // BLOCK_HEIGHT
IMAGE_RESOLUTION = IMAGE_WIDTH / BLOCK_HEIGHT
LAYOUT_PADDING_HORIZONTAL = (
    LAYOUT_PADDING_H
    + (
        (LAYOUT_WIDTH - LAYOUT_PADDING_H * 2)
        - BLOCK_WIDTH * HORIZONTAL_AMOUNT
        - HORIZONTAL_AMOUNT * BLOCK_MARGIN
    )
    // 2
)
LAYOUT_PADDING_TOP = (
    LAYOUT_PADDING_TOP
    + (
        (LAYOUT_HEIGHT - LAYOUT_PADDING_TOP - LAYOUT_PADDING_BOT)
        - BLOCK_HEIGHT * VERTICAL_AMOUNT
        - VERTICAL_AMOUNT * BLOCK_MARGIN
    )
    // 2
)
LAYOUT_PADDING_BOT = (
    LAYOUT_PADDING_BOT
    + (
        (LAYOUT_HEIGHT - LAYOUT_PADDING_TOP - LAYOUT_PADDING_BOT)
        - BLOCK_HEIGHT * VERTICAL_AMOUNT
        - VERTICAL_AMOUNT * BLOCK_MARGIN
    )
    // 2
)
