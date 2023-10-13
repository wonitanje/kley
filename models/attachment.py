from pydantic import BaseModel


class AttachmentModel(BaseModel):
    name: str
    size: tuple[int, int, int]
    image_url: str
