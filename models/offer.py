from enum import Enum
from uuid import uuid4
from pydantic import BaseModel
import mimetypes
from models.pack import PackModel
from models.sweet import SweetModel
from models.attachment import AttachmentModel

mimetypes.init()


class Page(str, Enum):
    title = "title"
    branding = "branding"
    filling = "filling"
    pack = "pack"
    sweet = "sweet"
    attachment = "attachment"
    terms = "terms"


class OfferMimetype(str, Enum):
    pdf = mimetypes.types_map[".pdf"]
    png = mimetypes.types_map[".png"]


class OfferConfig(BaseModel):
    format: OfferMimetype
    branding: bool
    until_date: str
    delivery_date: tuple[str, str]
    payment_term: str
    draw_no_tax: bool = False
    # layout: LayoutConfig
    # sweet: SweetConfig


class OfferModel(BaseModel):
    packs: list[PackModel]
    sweets: list[SweetModel]
    attachments: list[AttachmentModel]
    name: str = uuid4()
    weight: int
    price: int
    layouts: dict[Page, str]
    config: OfferConfig
