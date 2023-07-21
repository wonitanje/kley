from enum import Enum
from uuid import uuid4
from pydantic import BaseModel
from models.layout import LayoutConfig
import mimetypes

from models.sweet import SweetConfig, SweetModel

mimetypes.init()


class OfferMimetype(str, Enum):
    pdf = mimetypes.types_map[".pdf"]
    png = mimetypes.types_map[".png"]


class OfferConfig(BaseModel):
    format: OfferMimetype
    layout: LayoutConfig
    sweet: SweetConfig


class OfferModel(BaseModel):
    sweets: list[SweetModel]
    name: str = uuid4()
    weight: str
    price: str
    config: OfferConfig
