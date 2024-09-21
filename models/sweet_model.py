from pydantic import BaseModel

import utils.constants as const
from models.text_model import TextConfig


class SweetModel(BaseModel):
    name: str
    description: str
    organization: str
    weight: float
    amount: int
    image_url: str = None


class SweetConfig(BaseModel):
    width: int = const.BLOCK_WIDTH
    height: int = const.BLOCK_HEIGHT
    margin: int = const.BLOCK_MARGIN
    text: TextConfig
