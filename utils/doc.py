from typing import Annotated, Optional
from fastapi import File
from models.offer import OfferConfig, OfferMimetype
from utils.layout import Layout


class Doc:
    format = OfferMimetype.pdf
    pages: list[Layout] = []
    page: Optional[Layout] = None

    def __init__(
        self,
        pages: Optional[Annotated[bytes, File()]] = None,
        config: Optional[OfferConfig] = None,
    ) -> None:
        if pages:
            self.pages = [Layout(file) for file in pages]
            self.page = self.pages[0]

        if config:
            self.apply(config)

    def apply(self, config: OfferConfig):
        [page.apply(config.layout) for page in self.pages]
        self.format = config.format

    def add_page(self, layout: Layout):
        self.pages.append(layout)
        self.page = layout

    def save(self, name: str) -> list[str]:
        ext = (
            ".pdf"
            if self.format == OfferMimetype.pdf
            else ".png"
            if self.format == OfferMimetype.svg
            else None
        )
        if ext is None:
            Exception("Unwkown doc format")

        path = f"results/{name}{ext}"
        images = [page.image for page in self.pages]
        images[0].save(path, save_all=True, append_images=images)

        # return [page.save(f"{name}-{idx}.png") for idx, page in enumerate(self.pages)]
        return path
