from PIL import ImageFont
from math import floor


def to_multiline(line: str, font: ImageFont, width: int, lines=1000):
    line_height = font.getsize(line)[1]
    words = line.split()
    words_beg = shift = iter = 0
    words_len = words_end = len(words)
    multiline_shifter = 0

    while words_beg < words_len:
        line_width = font.getsize("".join(words[words_beg:words_end]))[0]
        while line_width > width - 15:
            words_end -= 1
            line_width = font.getsize("".join(words[words_beg:words_end]))[0]
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


def currency(price: float):
    last = floor(price) % 10
    if (price >= 10 and price < 20) or last > 5:
        return "рублей"

    if last == 1:
        return "рубль"

    return "рубля"
