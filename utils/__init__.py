from PIL import ImageFont
from math import floor


def to_multiline(line: str, font: ImageFont, width: int, lines=1000):
    line_bbox = font.getbbox(line)
    line_height = line_bbox[3] + line_bbox[1]
    words = line.split()
    words_beg = shift = iter = 0
    words_len = words_end = len(words)
    multiline_shifter = 0

    while words_beg < words_len:
        line_width = font.getlength("".join(words[words_beg:words_end]))
        while line_width > width - 15:
            words_end -= 1
            line_width = font.getlength("".join(words[words_beg:words_end]))
        lines -= 1
        words_beg = words_end if (words_beg != words_end) else words_end + 1
        words[words_end - 1] += "\n"
        iter += 1
        shift += line_height + multiline_shifter
        multiline_shifter = -2
        if lines == 0:
            words = words[:words_end]
            break
        words_end = words_len

    line = "".join(map(lambda el: el if "\n" in el else f"{el} ", words))
    return line, shift


def plural(forms: tuple[str, str, str]):
    def same(_: int | float):
        return forms[0]

    def get(value: int | float):
        two_periods = float(value) % 100
        first_period = floor(two_periods) % 10
        if (two_periods >= 10 and two_periods < 20) or first_period >= 5:
            return forms[2]

        if first_period == 1:
            return forms[0]

        return forms[1]

    return same if len(set(forms)) == 1 else get


currency = plural(["руб", "руб", "руб"]) # numerate(["рубль", "рубля", "рублей"])
counter = plural(["штука", "штуки", "штук"])
