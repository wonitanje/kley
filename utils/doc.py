from typing import Annotated
from fastapi import File
from models.offer import OfferConfig, OfferMimetype
from utils.layouts.layout import Layout


class Doc:
    def __init__(
        self,
        pages: Annotated[bytes, File()] | None = None,
        config: OfferConfig | None = None,
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
        return layout

    def get_pages(self, LayoutModel: Layout):
        return list(filter(lambda x: type(x) == LayoutModel, self.pages))

    def get_last_page(self, LayoutModel: Layout):
        pages = self.get_pages(LayoutModel)
        if len(pages) > 0:
            return pages[-1]

    def save(self, name: str) -> str:
        # ext = None
        # if self.format == OfferMimetype.pdf:
        ext = ".pdf"
        path = f"results/{name}{ext}"
        images = [
            page.image if page.image.mode == "RGB" else page.image.convert("RGB")
            for page in self.pages
        ]
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
