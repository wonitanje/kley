from pydantic import BaseModel


class PackModel(BaseModel):
    name: str
    size: tuple[float, float, float]
    material: str
    image_url: str
