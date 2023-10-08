from math import ceil
from PIL import Image, ImageFont, ImageDraw

import utils.constants as const
from utils.service import get_bytes
from models.layout import LayoutConfig


class Layout:
    def __init__(self, image_url: str | None = None) -> None:
        self.image = Image.new(
            "RGB", [const.LAYOUT_WIDTH, const.LAYOUT_HEIGHT], (255, 255, 255)
        )
        self._x_offset = const.LAYOUT_PADDING_HORIZONTAL + const.BLOCK_MARGIN
        self._y_offset = const.LAYOUT_PADDING_TOP + const.BLOCK_MARGIN
        self._row = 0
        self._col = 0

        if image_url:
            self.image = Image.open(get_bytes(image_url))

    def _generate_text(
        self,
        text: str,
        size: tuple[int, int],
        font: ImageFont,
        position: tuple[int, int] = (0, 0),
        fill: tuple[int, int, int] = (3, 3, 3),
    ):
        image = Image.new("RGB", size, (255, 255, 255))
        drawer = ImageDraw.Draw(image)
        drawer.text(position, text, font=font, fill=fill)
        return image

    def apply(self, config: LayoutConfig):
        layout_size = (config.width, config.height)
        bg = Image.open(get_bytes(config.image_url))

        if bg.size != layout_size:
            bg = bg.resize(layout_size)

        if self.image.size != layout_size:
            self.image = self.image.resize(layout_size)

        self.image.paste(bg, (0, 0))

    def draw_numerator(self, index: int, amount: int):
        numerator_position = (
            ceil(const.LAYOUT_WIDTH * 0.923),
            ceil(const.LAYOUT_HEIGHT * 0.95),
        )
        font = const.TEXT["NUMB"]
        text = f"{index} / {amount}"
        text_width = font.getsize(text)[0]
        size = (150, 60)
        position = ((size[0] - text_width) // 2, 0)
        text_image = self._generate_text(text, size, font, position)
        self.image.paste(text_image, numerator_position)

    def add_item(self):
        return True
