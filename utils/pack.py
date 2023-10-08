from models.pack import PackModel
from utils.picture import Picture


class Pack:
    def __init__(self, model: PackModel) -> None:
        self.name = model.name
        self.size = model.size
        self.material = model.material
        self.picture = Picture(model.image_url)
