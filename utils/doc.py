from typing import Annotated, Optional
from fastapi import File
from models.offer import OfferConfig, OfferMimetype
from utils.layout import Layout


class Doc:
    def __init__(
        self,
        pages: Optional[Annotated[bytes, File()]] = None,
        config: Optional[OfferConfig] = None,
    ) -> None:
        self.format = OfferMimetype.pdf
        self.pages: list[Layout] = []

        if pages:
            self.pages = [Layout(file) for file in pages]

        if config:
            self.apply(config)

    def apply(self, config: OfferConfig):
        [page.apply(config.layout) for page in self.pages]
        self.format = config.format

    def add_page(self, layout: Layout):
        self.pages.append(layout)

    def save(self, name: str) -> str:
        # ext = None
        # if self.format == OfferMimetype.pdf:
        ext = ".pdf"
        path = f"results/{name}{ext}"
        images = [page.image for page in self.pages]
        images[0].save(path, save_all=True, append_images=images[1:])

        return path

        # if self.format == OfferMimetype.png:
        #     ext = ".png"
        #     paths = []
        #     for idx, page in enumerate(self.pages):
        #         path = f"results/{name}-{idx + 1}{ext}"
        #         page.image.save(path)
        #         paths.append(path)

        #     return paths

        # if ext is None:
        #     Exception("Unwkown doc format")
