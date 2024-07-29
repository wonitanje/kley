from pydantic import BaseModel


class AttachmentModel(BaseModel):
    name: str
    size: tuple[float, float, float]
    image_url: str
