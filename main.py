from genericpath import exists
from os import makedirs
from os.path import exists
from PIL import Image, ImageDraw
import constants as const
import utils

file_names = utils.get_filenames(const.FOLDER_PATH, const.DB)
pillow_images = utils.get_images(file_names, const.FOLDER_PATH)
images = utils.resize_images(pillow_images, const.IMAGE_WIDTH, const.BLOCK_HEIGHT, const.IMAGE_RESOLUTION)
ll = len(images)
print(f'Всего изображений: {ll}\nКоличество строк: {const.VERTICAL_AMOUNT}\nКоличество столбцев: {const.HORIZONTAL_AMOUNT}')
layout_name = input('Введите название сгенерированной картинки: ') or 'test'
if not exists('result'):
  makedirs('result')

layout_number = 1
pasted_counter = 0
is_ended = False
while not is_ended:
  x_offset = const.LAYOUT_PADDING_HORIZONTAL + const.BLOCK_MARGIN
  y_offset = const.LAYOUT_PADDING_VERTICAL + const.BLOCK_MARGIN
  layout = Image.new('RGB', [const.LAYOUT_WIDTH, const.LAYOUT_HEIGHT], (255, 255, 255))

  row = col = 0
  while not is_ended and col < const.HORIZONTAL_AMOUNT:
    while not is_ended and row < const.VERTICAL_AMOUNT:
      img = images[pasted_counter]
      x_offset_centred = x_offset + (const.IMAGE_WIDTH - img.size[0]) // 2
      y_offset_centred = y_offset + (const.BLOCK_HEIGHT - img.size[1]) // 2
      txt = utils.db_name(img.key, const.DB)
      sire = txt['sire']
      name = txt['name'].replace('гр)', 'г)').replace(' г)', 'г)')
      desc = txt.get('description', None)
      weight = txt.get('weight', None)
      if weight is not None and weight not in name:
        name += f' ({weight}г)'

      try:
        layout.paste(img, (x_offset_centred, y_offset_centred), mask=img.split()[3])
      except:
        layout.paste(img, (x_offset_centred, y_offset_centred))

      text = Image.new('RGBA', [const.TEXT_WIDTH, const.BLOCK_HEIGHT], (255, 255, 255))
      drawer = ImageDraw.Draw(text)

      text_x = text_y = 0
      drawer.text((text_x, text_y), sire, font=const.TEXT['SIRE'], fill=(120, 120, 120))

      text_x = const.TEXT['SIRE'].getsize(sire)[0] + 10
      drawer.text((text_x, text_y), f'{img.amount} шт', font=const.TEXT['ENUM'], fill=(18,183,45))

      text_x = 0
      text_y += const.TEXT['ENUM'].getsize(sire)[1] + const.TEXT_MARGIN
      name, shift = utils.to_multiline(name, const.TEXT['NAME'], const.TEXT_WIDTH, const.NAME_LINES)
      drawer.multiline_text((text_x, text_y), name, font=const.TEXT['NAME'], fill=(3, 3, 3))

      if desc is not None:
        text_y += shift + const.TEXT_MARGIN
        desc, shift = utils.to_multiline(desc, const.TEXT['DESC'], const.TEXT_WIDTH)
        drawer.multiline_text((text_x, text_y), desc, font=const.TEXT['DESC'], fill=(3, 3, 3))
        text_height = text_y + shift

      text_x = x_offset + const.IMAGE_WIDTH + const.IMAGE_TEXT_MARGIN
      text_y = y_offset + (const.BLOCK_HEIGHT - text_height) // 2
      layout.paste(text, (text_x, text_y))

      y_offset += const.BLOCK_HEIGHT + const.BLOCK_MARGIN
      pasted_counter += 1
      row += 1

      if pasted_counter >= ll:
        is_ended = True

    x_offset += const.BLOCK_WIDTH + const.BLOCK_MARGIN
    y_offset = const.LAYOUT_PADDING_VERTICAL + const.BLOCK_MARGIN
    col += 1
    row = 0

  layout.convert('RGB').save(f"result/{layout_name}-{layout_number}.jpg")
  print(f"Файл '{layout_name}-{layout_number}.jpg' сохранен в папке 'result'")
  layout_number += 1

input("\nПрограмма закончила работу\nНажмите 'Enter' чтобы закрыть программу")