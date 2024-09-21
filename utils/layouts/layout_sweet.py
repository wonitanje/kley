from enum import Enum
from math import floor
from PIL import Image, ImageDraw, ImageFont

from models.layout_model import LayoutConfig
from utils import constants as const, currency, counter, to_multiline
from utils.sweet import Sweet
from utils.layouts.layout import Layout


class Area(int, Enum):
    amount = 0
    weight = 1
    price = 2
    noTaxPrice = 3


area_titles = ("Количество конфет", "Вес подарка", "Цена подарка", "Цена без НДС")


class LayoutSweet(Layout):
    def __init__(
        self, name: str, image_url: str | None = None, config: LayoutConfig | None = None
    ) -> None:
        super().__init__(name, image_url)
        print(name, image_url)

        if config:
            self.apply(config)

    def draw_area(
        self,
        title: Area,
        data: str,
        line_through: bool = False,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        size = [440, 174]
        initial_pos = (1100, 90)
        padding = 50
        idx = title.value
        pos = (
            initial_pos[0] + (size[0] + padding) * idx,
            initial_pos[1],
        )
        if title == Area.noTaxPrice:
            size[0] = 520

        area = Image.new("RGBA", size=size, color=(255, 255, 255))
        drawer = ImageDraw.Draw(area)
        drawer.rounded_rectangle(
            xy=((0, 0), [i - 2 for i in size]),
            radius=10,
            width=1,
            outline="red",
        )

        # Title
        font = const.TEXT["AREA"]
        text = area_titles[idx]
        width = font.getlength(text)
        drawer.text(
            xy=((size[0] - width) / 2, 12),
            align="center",
            fill="black",
            font=font,
            text=text,
        )

        # Text
        font = const.TEXT["INFO"]
        width = font.getlength(data)
        drawer.text(
            xy=((size[0] - width) / 2, size[1] / 2),
            align="center",
            fill=(255, 25, 31),
            font=font,
            text=data,
        )

        if line_through:
            shape = [(0, size[1]), (size[0], 0)]
            drawer.line(shape, fill=(0, 0, 0), width=8)

        self.image.paste(area, pos)
        area.close()

        return (pos, [i + size[idx] for idx, i in enumerate(pos)])

    def draw_price(self, price: int, addNoTax: bool):
        if addNoTax:
            noTaxPrice = round(price * 100 / 120, 2)
            self.draw_area(Area.noTaxPrice, f"{noTaxPrice} {currency(noTaxPrice)}")

        old_price = floor(price / 0.85)
        bbox = self.draw_area(Area.price, f"{old_price} {currency(old_price)}", True)

        size = (bbox[1][0] - bbox[0][0], bbox[1][1] - bbox[0][1])
        fill = (0, 0, 0)

        # font = const.TEXT["INFO"]
        # sale_position = (bbox[1][0] + 24, bbox[1][1] + 8)
        # text = "-15%"
        # text_bbox = font.getbbox(text)
        # text_size = (text_bbox[0] + text_bbox[2], text_bbox[1] + text_bbox[3])
        # text_image = self._generate_text(text, size, font, (0, 4), fill)
        # self.image.paste(text_image, sale_position)
        # text_image.close()

        discount_position = (bbox[0][0], bbox[1][1] + 8)
        font = ImageFont.truetype(const.PRIMARY_FONT, 70)
        text = f"{price} {currency(price)}"
        text_bbox = font.getbbox(text)
        text_size = (text_bbox[0] + text_bbox[2], text_bbox[1] + text_bbox[3])
        text_position = ((size[0] - text_size[0]) // 2, 0)
        text_image = self._generate_text(text, size, font, text_position, fill)
        self.image.paste(text_image, discount_position)
        text_image.close()

    def draw_weight(self, weight: int):
        self.draw_area(Area.weight, f"{weight} грамм")

    def draw_amount(self, amount: int):
        self.draw_area(Area.amount, f"{amount} {counter(amount)}")

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
        finally:
            img.close()

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
