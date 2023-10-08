from enum import Enum
from uuid import uuid4
from pydantic import BaseModel
import mimetypes
from models.layout import LayoutConfig
from models.pack import PackModel

from models.sweet import SweetConfig, SweetModel

mimetypes.init()


class OfferMimetype(str, Enum):
    pdf = mimetypes.types_map[".pdf"]
    png = mimetypes.types_map[".png"]


class OfferConfig(BaseModel):
    format: OfferMimetype
    # layout: LayoutConfig
    # sweet: SweetConfig


class OfferModel(BaseModel):
    sweets: list[SweetModel]
    packs: list[PackModel]
    name: str = uuid4()
    weight: int
    price: int
    layouts: dict[str, str]
    config: OfferConfig
