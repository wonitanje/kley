from math import ceil, floor
from PIL import Image, ImageDraw, ImageFont

from models.layout import LayoutConfig
from utils import constants as const, currency, to_multiline
from utils.sweet import Sweet
from utils.layouts.layout import Layout


class LayoutSweet(Layout):
    def __init__(
        self, image_url: str | None = None, config: LayoutConfig | None = None
    ) -> None:
        super().__init__(image_url)

        if config:
            self.apply(config)

    def draw_price(self, price: int):
        # Old price
        price_position = (
            ceil(const.LAYOUT_WIDTH * 0.8),
            ceil(const.LAYOUT_HEIGHT * 0.07),
        )
        fill = (255, 25, 31)
        size = (400, 80)
        # Text
        old_price = floor(price / 0.85)
        text = f"{old_price} {currency(old_price)}"
        font = const.TEXT["INFO"]
        text_bbox = font.getbbox(text)
        text_size = (text_bbox[0] + text_bbox[2], text_bbox[1] + text_bbox[3])
        text_position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        text_image = self._generate_text(text, size, font, text_position, fill)
        # Line
        drawer = ImageDraw.Draw(text_image)
        shape = [(0, text_image.size[1]), (text_image.size[0], 0)]
        drawer.line(shape, fill=(0, 0, 0), width=8)
        self.image.paste(text_image, price_position)

        # New price
        fill = (0, 0, 0)

        sale_position = (
            price_position[0] + size[0] + 24,
            price_position[1],
        )
        text = "-15%"
        text_bbox = font.getbbox(text)
        text_size = (text_bbox[0] + text_bbox[2], text_bbox[1] + text_bbox[3])
        text_position = (0, (size[1] - text_size[1]) // 2)
        text_image = self._generate_text(text, size, font, text_position, fill)
        self.image.paste(text_image, sale_position)

        discount_position = (
            price_position[0],
            price_position[1] + size[1] + 8,
        )
        font = ImageFont.truetype(const.PRIMARY_FONT, 70)
        size = (400, 100)
        text = f"{price} {currency(price)}"
        text_bbox = font.getbbox(text)
        text_size = (text_bbox[0] + text_bbox[2], text_bbox[1] + text_bbox[3])
        text_position = ((size[0] - text_size[0]) // 2, 0)
        text_image = self._generate_text(text, size, font, text_position, fill)
        self.image.paste(text_image, discount_position)

    def draw_weight(self, weight: int):
        weight_position = (
            ceil(const.LAYOUT_WIDTH * 0.6357),
            ceil(const.LAYOUT_HEIGHT * 0.07),
        )
        fill = (255, 25, 31)
        size = (400, 80)
        font = const.TEXT["INFO"]
        text = f"{weight} граммов"
        text_bbox = font.getbbox(text)
        text_size = (text_bbox[0] + text_bbox[2], text_bbox[1] + text_bbox[3])
        position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        text_image = self._generate_text(text, size, font, position, fill)
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
        text_bbox = font.getbbox(text)
        text_size = (text_bbox[0] + text_bbox[2], text_bbox[1] + text_bbox[3])
        text_position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        text_image = self._generate_text(text, size, font, text_position, fill)
        self.image.paste(text_image, amount_position)

    def add_item(self, sweet: Sweet):
        if self._row >= const.VERTICAL_AMOUNT:
            self._x_offset += const.BLOCK_WIDTH + const.BLOCK_MARGIN
            self._y_offset = const.LAYOUT_PADDING_TOP + const.BLOCK_MARGIN
            self._col += 1
            self._row = 0
        if self._col >= const.HORIZONTAL_AMOUNT:
            return False

        # Defines
        img_size = (const.IMAGE_WIDTH, const.BLOCK_HEIGHT)
        text_size = (const.TEXT_WIDTH, const.BLOCK_HEIGHT)

        # Draw image
        img = sweet.picture.resize(img_size)
        img_centred = (
            self._x_offset + (img_size[0] - img.size[0]) // 2,
            self._y_offset + (img_size[1] - img.size[1]) // 2,
        )
        try:
            self.image.paste(img, img_centred, mask=img.split()[3])
        except:
            self.image.paste(img, img_centred)

        # Draw text
        sire = sweet.sire
        name = sweet.name.replace("г)", "гр)").replace(" гр)", "гр)")
        desc = sweet.description
        weight = sweet.weight
        if weight is not None and str(weight) not in name:
            name += f" ({weight}гр)"

        text_img = Image.new("RGBA", text_size, (255, 255, 255))
        drawer = ImageDraw.Draw(text_img)
        text_x = text_y = 0

        # Write sire
        drawer.text(
            (text_x, text_y), sire, font=const.TEXT["SIRE"], fill=(120, 120, 120)
        )

        # Write amount
        text_x = const.TEXT["SIRE"].getlength(sire) + 10
        drawer.text(
            (text_x, text_y),
            f"{sweet.amount} шт",
            font=const.TEXT["ENUM"],
            fill=(18, 183, 45),
        )

        # Write amount
        text_x = 0
        text_bbox = const.TEXT["ENUM"].getbbox(sire)
        text_height = text_bbox[3] - text_bbox[1]
        text_y += text_height + const.TEXT_MARGIN
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
        text_img = text_img.crop((0, 0, const.TEXT_WIDTH, text_height))
        text_x = self._x_offset + const.IMAGE_WIDTH + const.IMAGE_TEXT_MARGIN
        text_y = self._y_offset + (const.BLOCK_HEIGHT - text_height) // 2
        self.image.paste(text_img, (text_x, text_y))
        text_img.close()

        # Shift to next node
        self._row += 1
        self._y_offset += const.BLOCK_HEIGHT + const.BLOCK_MARGIN

        return True
