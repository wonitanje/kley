from typing import Annotated
from fastapi import File
from pydantic import BaseModel

import utils.constants as const
from models.text import TextConfig


class SweetModel(BaseModel):
    name: str
    description: str
    organization: str
    weight: float
    price: float
    amount: int
    image: Annotated[bytes, File()]


class SweetConfig(BaseModel):
    width: float = const.BLOCK_WIDTH
    height: float = const.BLOCK_HEIGHT
    margin: float = const.BLOCK_MARGIN
    text: TextConfig
