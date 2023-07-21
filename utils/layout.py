from math import ceil
from typing import Optional
from PIL import Image, ImageDraw, ImageFont


import utils.constants as const
from utils import to_multiline
from utils.service import get_bytes
from utils.sweet import Sweet
from models.layout import LayoutConfig


class Layout:
    def __init__(
        self,
        image_url: Optional[str] = None,
        config: Optional[LayoutConfig] = None,
    ) -> None:
        self.image = Image.new(
            "RGB", [const.LAYOUT_WIDTH, const.LAYOUT_HEIGHT], (255, 255, 255)
        )
        self._x_offset = const.LAYOUT_PADDING_HORIZONTAL + const.BLOCK_MARGIN
        self._y_offset = const.LAYOUT_PADDING_TOP + const.BLOCK_MARGIN
        self._row = 0
        self._col = 0

        if image_url:
            self.image = Image.open(get_bytes(image_url))

        if config:
            self.apply(config)

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

    def draw_price(self, price: str):
        price_position = (
            ceil(const.LAYOUT_WIDTH * 0.8),
            ceil(const.LAYOUT_HEIGHT * 0.07),
        )
        fill = (255, 25, 31)
        size = (400, 80)
        font = const.TEXT["INFO"]
        text_size = font.getsize(price)
        text_position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        text_image = self._generate_text(price, size, font, text_position, fill)
        self.image.paste(text_image, price_position)

    def draw_weight(self, weight: str):
        weight_position = (
            ceil(const.LAYOUT_WIDTH * 0.6357),
            ceil(const.LAYOUT_HEIGHT * 0.07),
        )
        fill = (255, 25, 31)
        size = (400, 80)
        font = const.TEXT["INFO"]
        text_size = font.getsize(weight)
        position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        text_image = self._generate_text(weight, size, font, position, fill)
        self.image.paste(text_image, weight_position)

    def draw_amount(self, amount: int):
        amount_position = (
            ceil(const.LAYOUT_WIDTH * 0.4775),
            ceil(const.LAYOUT_HEIGHT * 0.07),
        )
        font = const.TEXT["INFO"]
        size = (400, 80)
        fill = (255, 25, 31)
        text = f"{amount} штук"
        text_size = font.getsize(text)
        text_position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        text_image = self._generate_text(text, size, font, text_position, fill)
        self.image.paste(text_image, amount_position)

    def add_sweet(self, sweet: Sweet):
        print("add sweet", self._row, self._col)
        if self._row >= const.VERTICAL_AMOUNT:
            self._x_offset += const.BLOCK_WIDTH + const.BLOCK_MARGIN
            self._y_offset = const.LAYOUT_PADDING_TOP + const.BLOCK_MARGIN
            self._col += 1
            self._row = 0
        if self._col >= const.HORIZONTAL_AMOUNT:
            return False

        # Defines
        img = sweet.picture.image
        x_offset_centred = self._x_offset + (const.IMAGE_WIDTH - img.size[0]) // 2
        y_offset_centred = self._y_offset + (const.BLOCK_HEIGHT - img.size[1]) // 2
        sire = sweet.sire
        name = sweet.name.replace("гр)", "г)").replace(" г)", "г)")
        desc = sweet.description
        weight = sweet.weight
        if weight is not None and str(weight) not in name:
            name += f" ({weight}г)"

        # Draw image
        try:
            self.image.paste(
                img, (x_offset_centred, y_offset_centred), mask=img.split()[3]
            )
        except:
            self.image.paste(img, (x_offset_centred, y_offset_centred))

        text = Image.new(
            "RGBA", [const.TEXT_WIDTH, const.BLOCK_HEIGHT], (255, 255, 255)
        )
        drawer = ImageDraw.Draw(text)
        text_x = text_y = 0

        # Write sire
        drawer.text(
            (text_x, text_y), sire, font=const.TEXT["SIRE"], fill=(120, 120, 120)
        )
        text_x = const.TEXT["SIRE"].getsize(sire)[0] + 10
        drawer.text(
            (text_x, text_y),
            f"{sweet.amount} шт",
            font=const.TEXT["ENUM"],
            fill=(18, 183, 45),
        )

        # Write amount
        text_x = 0
        text_y += const.TEXT["ENUM"].getsize(sire)[1] + const.TEXT_MARGIN
        name, shift = to_multiline(
            name, const.TEXT["NAME"], const.TEXT_WIDTH, const.NAME_LINES
        )
        drawer.multiline_text(
            (text_x, text_y), name, font=const.TEXT["NAME"], fill=(3, 3, 3)
        )

        # Write description
        if desc is not None:
            text_y += shift + const.TEXT_MARGIN
            desc, shift = to_multiline(desc, const.TEXT["DESC"], const.TEXT_WIDTH)
            drawer.multiline_text(
                (text_x, text_y), desc, font=const.TEXT["DESC"], fill=(3, 3, 3)
            )
            text_height = text_y + shift

        # Draw text
        text_x = self._x_offset + const.IMAGE_WIDTH + const.IMAGE_TEXT_MARGIN
        text_y = self._y_offset + (const.BLOCK_HEIGHT - text_height) // 2
        self.image.paste(text, (text_x, text_y))
        text.close()

        # Shift to next node
        self._row += 1
        self._y_offset += const.BLOCK_HEIGHT + const.BLOCK_MARGIN

        return True
