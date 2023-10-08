from pydantic import BaseModel


class PackModel(BaseModel):
    name: str
    size: tuple[int, int, int]
    material: str
    image_url: str
