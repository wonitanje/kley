from models.attachment import AttachmentModel
from utils.picture import Picture


class Attachment:
    def __init__(self, model: AttachmentModel) -> None:
        self.name = model.name
        self.size = model.size
        self.picture = Picture(model.image_url)
