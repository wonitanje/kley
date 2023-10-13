from functools import reduce
from utils.layouts.layout import Layout
import utils.constants as const
from datetime import datetime


class LayoutTerms(Layout):
    def __init__(self, image_url: str | None = None) -> None:
        super().__init__(image_url)
        self.font = const.TEXT["NUMB"]
        self.fill = (0, 0, 0)
        self.shift = (0, 0)
        self.size = (1200, 60)

    def set_util_date(self, dateISO: str):
        position = (
            round(self.image.size[0] * 0.4307),
            round(self.image.size[1] * 0.2024),
        )
        date = datetime.fromisoformat(dateISO)
        text = self.get_string_date(date).replace(" ", "  ")
        size = (800, 60)
        fill = (255, 0, 0)
        text_image = self._generate_text(text, size, self.font, self.shift, fill)
        self.image.paste(text_image, position)

    def set_delivery_date(self, datesISO: tuple[str, str]):
        position = (
            round(self.image.size[0] * 0.3318),
            round(self.image.size[1] * 0.32),
        )
        dates = [datetime.fromisoformat(iso) for iso in datesISO]
        text = self.get_string_date(*dates)
        text_image = self._generate_text(
            text, self.size, self.font, self.shift, self.fill
        )
        self.image.paste(text_image, position)

    def set_payment_term(self, term: str):
        position = (
            round(self.image.size[0] * 0.3318),
            round(self.image.size[1] * 0.415),
        )
        text_image = self._generate_text(
            term, self.size, self.font, self.shift, self.fill
        )
        self.image.paste(text_image, position)

    def get_string_date(self, date1: datetime, date2: datetime | None = None):
        months = {
            1: "января",
            2: "февраля",
            3: "марта",
            4: "апреля",
            5: "мая",
            6: "июня",
            7: "июля",
            8: "августа",
            9: "сентября",
            10: "октября",
            11: "ноября",
            12: "декабря",
        }

        if date2 is None or date2 == date1:
            return f"{date1.day} {months.get(date1.month)} {date1.year} года"

        if date1.year != date2.year:
            return f"{date1.day} {months.get(date1.month)} {date1.year} - {date2.day} {months.get(date2.month)} {date2.year} года"

        if date1.month != date2.month:
            return f"{date1.day} {months.get(date1.month)} - {date2.day} {months.get(date2.month)} {date1.year} года"

        return f"{date1.day} - {date2.day} {months.get(date1.month)} {date1.year} года"
