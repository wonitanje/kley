from models.sweet import SweetConfig, SweetModel
from utils import constants as const
from utils.picture import Picture


class Sweet:
    def __init__(self, model: SweetModel) -> None:
        self.name = model.name
        self.description = model.description
        wh = model.weight
        self.weight = int(wh) if int(wh) == wh else wh
        self.sire = model.organization
        self.amount = model.amount
        self.picture = Picture(model.image_url)
