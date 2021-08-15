from genericpath import exists
from os import makedirs
from os.path import exists
from PIL import Image, ImageDraw
import constants as const
import utils


images = utils.resize_images(utils.get_images(utils.get_image_names()))
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

      try:
        layout.paste(img, (x_offset_centred, y_offset_centred), mask=img.split()[3])
      except:
        layout.paste(img, (x_offset_centred, y_offset_centred))

      text = Image.new('RGB', [const.TEXT_WIDTH, const.BLOCK_HEIGHT], (255, 255, 255))
      drawer = ImageDraw.Draw(text)

      text_x = text_y = 0
      drawer.text((text_x, text_y), f'Sire', font=const.TEXT['SIRE'], fill=(120, 120, 120))

      text_x = const.TEXT['ENUM'].getsize('Sire')[0] + 10
      drawer.text((text_x, text_y), f'{img.amount} шт', font=const.TEXT['ENUM'], fill=(18,183,45))

      text_x = 0
      text_y += const.TEXT['ENUM'].getsize('Sire')[1] + 4
      drawer.text((text_x, text_y), 'Name', font=const.TEXT['NAME'], fill=(3, 3, 3))

      text_y += const.TEXT['ENUM'].getsize('Name')[1] + 8
      drawer.multiline_text((text_x, text_y), 'Description\nLine2', font=const.TEXT['DESC'], fill=(3, 3, 3))
      text_x, text_y = x_offset + const.IMAGE_WIDTH, y_offset
      layout.paste(text, (text_x, text_y))

      y_offset += const.BLOCK_HEIGHT + const.BLOCK_MARGIN
      pasted_counter += 1
      row += 1

      if pasted_counter >= ll:
        is_ended = True

    x_offset += const.BLOCK_WIDTH + const.BLOCK_MARGIN
    y_offset = const.LAYOUT_PADDING_VERTICAL
    col += 1
    row = 0

  layout.show()
  layout.save(f"result/{layout_name}-{layout_number}.jpg")
  print(f"Файл '{layout_name}-{layout_number}.jpg' сохранен в папке 'result'")
  layout_number += 1

input("\nПрограмма закончила работу\nНажмите 'Enter' чтобы закрыть программу")