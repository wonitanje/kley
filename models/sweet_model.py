from pydantic import BaseModel
from enum import Enum

import utils.constants as const
from models.text_model import TextConfig


class SweetModel(BaseModel):
    name: str
    description: str
    organization: str
    weight: float
    amount: int
    image_url: str = None


class Direction(int, Enum):
    Vertical = 0
    Horizontal = 1

class SweetConfig(BaseModel):
    width: int = const.BLOCK_WIDTH
    height: int = const.BLOCK_HEIGHT
    margin: int = const.BLOCK_MARGIN
    direction: Direction = Direction.Horizontal
    # text: TextConfig
