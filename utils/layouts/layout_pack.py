from models.layout import LayoutConfig
from utils import constants as const

from PIL import ImageFont
from utils.layouts.layout import Layout

from utils.pack import Pack


class LayoutPack(Layout):
    def __init__(self, image_url: str | None = None) -> None:
        super().__init__(image_url)
        self.col_amount = 1
        self._computeSize()

    def _computeSize(self):
        w_pad = const.LAYOUT_PADDING_HORIZONTAL * 2
        self.width = self.image.size[0] - w_pad

        h_pad = const.LAYOUT_PADDING_TOP + const.LAYOUT_PADDING_BOT
        self.height = self.image.size[1] - h_pad
        self.item_size = (
            self.width // self.col_amount,
            self.height - 210,
        )

    def apply(self, config: LayoutConfig):
        self._computeSize()
        return super().apply(config)

    def add_item(self, pack: Pack):
        if self._col >= self.col_amount:
            return False

        # Draw image
        img = pack.picture.resize(self.item_size)
        x_offset_centred = self._x_offset + (self.item_size[0] - img.size[0]) // 2
        y_offset_centred = self._y_offset + (self.item_size[1] - img.size[1]) // 2
        try:
            self.image.paste(
                img, (x_offset_centred, y_offset_centred), mask=img.split()[3]
            )
        except:
            self.image.paste(img, (x_offset_centred, y_offset_centred))

        # Shared
        position = (
            self._x_offset,
            self._y_offset + self.item_size[1],
        )

        # Write name
        font = ImageFont.truetype(const.PRIMARY_FONT, 60)
        text_height = 90
        size = (self.item_size[0], text_height)

        text = pack.name
        text_width = font.getlength(text)
        text_position = ((size[0] - text_width) // 2, 0)
        text_image = self._generate_text(text, size, font, text_position)
        self.image.paste(text_image, position)
        position = (position[0], position[1] + text_height)

        # Write size
        font = ImageFont.truetype(const.PRIMARY_FONT, 40)
        text_height = 60
        size = (self.item_size[0], text_height)

        text = f"Размер: {' x '.join([str(i // 10) for i in pack.size])} см"
        text_width = font.getlength(text)
        text_position = ((size[0] - text_width) // 2, 0)
        text_image = self._generate_text(text, size, font, text_position)
        self.image.paste(text_image, position)
        position = (position[0], position[1] + text_height)

        # Write material
        text = f"Материал: {pack.material}"
        text_width = font.getlength(text)
        text_position = ((size[0] - text_width) // 2, 0)
        text_image = self._generate_text(text, size, font, text_position)
        self.image.paste(text_image, position)
        position = (position[0], position[1] + text_height)

        # Shift to next node
        self._col += 1
        self._x_offset += self.item_size[0] + const.BLOCK_MARGIN
        self._y_offset += self.item_size[1] + const.BLOCK_MARGIN

        return True
