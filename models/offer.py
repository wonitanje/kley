from enum import Enum
from typing import Optional
from uuid import uuid4
from fastapi import UploadFile, File, Form
from pydantic import BaseModel, HttpUrl
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
    background: HttpUrl
    config: OfferConfig


class ChangeOfferModel(BaseModel):
    price: Optional[str] = Form(...)
    files: list[UploadFile] = File(...)
