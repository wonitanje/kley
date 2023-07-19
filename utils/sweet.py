from typing import Optional
from models.sweet import SweetConfig, SweetModel
from utils.picture import Picture


class Sweet:
    def __init__(self, model: SweetModel, config: Optional[SweetConfig] = None) -> None:
        self.name = model.name
        self.description = model.description
        self.price = model.price
        self.weight = model.weight
        self.sire = model.organization
        self.amount = model.amount
        self.picture = Picture(self.name)
        if config:
            self.apply(config)

    def apply(self, config: SweetConfig):
        self.picture.resize(config.width, config.height, config.width / config.height)
