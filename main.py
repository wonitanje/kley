from genericpath import exists
from os import makedirs
from os.path import exists
from PIL import Image, ImageDraw
from math import ceil
from functools import reduce
import constants as const
import utils

def main():
  file_names = utils.get_filenames(const.FOLDER_PATH, const.DB)
  if len(file_names) == 0:
    print('Нет ниодного изображения. Выход...')
    return
  pillow_images = utils.get_images(file_names, const.FOLDER_PATH)
  images = utils.resize_images(pillow_images, const.IMAGE_WIDTH, const.BLOCK_HEIGHT, const.IMAGE_RESOLUTION)
  ll = len(images)
  print(f' Всего изображений: {ll}\n Количество строк: {const.VERTICAL_AMOUNT}\n Количество столбцев: {const.HORIZONTAL_AMOUNT}')
  bg_mode = int(input('\nРежимы работы:\n [1] Написать название на фоне\n [2] Выбрать готовый фон\n- Выберите режим работы: '))
  if bg_mode == 1:
    bg_title = input('- Введите название состава: ')
  else:
    avaible_bgs = utils.get_avaible_backgrounds()
    msg_list = ''.join([f'\n [{idx + 1}] {filename}' for idx, filename in enumerate(avaible_bgs)])
    bg_input = int(input(f'\nДоступные изображения:{msg_list}\n- Выберите фон: '))
    bg_name = avaible_bgs[bg_input - 1]
  try:
    bg = Image.open(const.LAYOUT_BACKGROUND if bg_mode == 1 else f'assets/backgrounds/{bg_name}').resize((const.LAYOUT_WIDTH, const.LAYOUT_HEIGHT))
  except:
    input(f"\n Не удалось загрузить фон {const.LAYOUT_BACKGROUND}\n Нажмите 'Enter' чтобы закрыть программу")
    exit()

  total_amount = int(input('\n- Введите количетсво конфет: '))
  total_weight = int(input('- Введите вес подарка: '))
  layout_name = input('- Введите название сгенерированной картинки: ') or 'test'
  if not exists('result'):
    makedirs('result')

  pasted_counter = 0

  drawer_font = const.TEXT['TITLE']
  drawer_font_num = const.TEXT['NUMB']
  drawer_font_str = const.TEXT['INFO']
  drawer_fill = (0, 0, 0)

  if (bg_mode == 1):
    drawer_size = (980, 105)
    drawer_text_size = drawer_font.getsize(bg_title)
    print(f'{drawer_text_size=}')
    drawer_text_pos = ((drawer_size[0] - drawer_text_size[0]) // 2, (drawer_size[1] - drawer_text_size[1]) // 2)
    bg.paste(utils.text_drawer(bg_title, drawer_size, drawer_font, (0, -15), (255, 255, 255), (255, 0, 0, 0)), (230, 40))

  layout = Image.new('RGB', [const.LAYOUT_WIDTH, const.LAYOUT_HEIGHT], (255, 255, 255))
  layout.paste(bg, (0, 0))

  # Weight numbers
  drawer_position = (1860, 26)
  drawer_size = (210, 86)
  drawer_text = str(total_weight)
  drawer_text_size = drawer_font_num.getsize(drawer_text)
  drawer_text_pos = ((drawer_size[0] - drawer_text_size[0]) // 2, (drawer_size[1] - drawer_text_size[1]) // 2)
  layout.paste(utils.text_drawer(drawer_text, drawer_size, drawer_font_num, drawer_text_pos, drawer_fill), drawer_position)
  # Weight letters
  drawer_position = (1860, 130)
  drawer_size = (210, 36)
  drawer_text = utils.get_weight_word(total_weight)
  drawer_text_size = drawer_font_str.getsize(drawer_text)
  drawer_text_pos = ((drawer_size[0] - drawer_text_size[0]) // 2, (drawer_size[1] - drawer_text_size[1]) // 2)
  layout.paste(utils.text_drawer(drawer_text, drawer_size, drawer_font_str, drawer_text_pos, drawer_fill), drawer_position)

  # Amount numbers
  drawer_position = (1515, 26)
  drawer_size = (160, 86)
  drawer_text = str(total_amount)
  drawer_text_size = drawer_font_num.getsize(drawer_text)
  drawer_text_pos = ((drawer_size[0] - drawer_text_size[0]) // 2, (drawer_size[1] - drawer_text_size[1]) // 2)
  layout.paste(utils.text_drawer(drawer_text, drawer_size, drawer_font_num, drawer_text_pos, drawer_fill), drawer_position)
  # Amount letters
  drawer_position = (1515, 130)
  drawer_size = (160, 36)
  drawer_text = utils.get_amount_word(total_amount)
  drawer_text_size = drawer_font_str.getsize(drawer_text)
  drawer_text_pos = ((drawer_size[0] - drawer_text_size[0]) // 2, (drawer_size[1] - drawer_text_size[1]) // 2)
  layout.paste(utils.text_drawer(drawer_text, drawer_size, drawer_font_str, drawer_text_pos, drawer_fill), drawer_position)

  is_ended = False

  line = [0, 0]

  x_offset_d = const.LAYOUT_PADDING_HORIZONTAL + const.BLOCK_MARGIN
  y_offset_d = const.LAYOUT_PADDING_TOP + const.BLOCK_MARGIN
  offset_d = [x_offset_d, y_offset_d]

  x_shift = const.BLOCK_WIDTH + const.BLOCK_MARGIN
  y_shift = const.BLOCK_HEIGHT + const.BLOCK_MARGIN
  shift = [x_shift, y_shift]
  
  x_amount = const.HORIZONTAL_AMOUNT
  y_amount = const.VERTICAL_AMOUNT
  amount = [x_amount, y_amount]

  x_offset = x_offset_d
  y_offset = y_offset_d
  offset = [x_offset, y_offset]

  primary = const.DIRECTION
  secondary = (const.DIRECTION + 1) % 2
  
  while not is_ended and line[secondary] < amount[secondary]:
    while not is_ended and line[primary] < amount[primary]:
      img = images[pasted_counter]
      offset_centred = (offset[0] + (const.IMAGE_WIDTH - img.size[0]) // 2, offset[1] + (const.BLOCK_HEIGHT - img.size[1]) // 2)
      txt = utils.db_name(img.key, const.DB)
      sire = txt['sire']
      name = txt['name'].replace('гр)', 'г)').replace(' г)', 'г)')
      desc = txt.get('description', None)
      weight = txt.get('weight', None)
      if weight is not None and weight not in name:
        name += f' ({weight}г)'

      try:
        layout.paste(img, offset_centred, mask=img.split()[3])
      except:
        layout.paste(img, offset_centred)
      img.close()

      offset[primary] += shift[primary]
      line[primary] += 1
      pasted_counter += 1

      if pasted_counter >= ll:
        is_ended = True

    offset[primary] = offset_d[primary]
    offset[secondary] += shift[secondary]
    line[primary] = 0
    line[secondary] += 1

  if input("- Введите '1' чтобы посмотреть результат: ").strip() == '1':
    layout.show()

  layout.convert('RGB').save(f"result/{layout_name}.jpg")
  layout.close()
  print(f" Файл '{layout_name}.jpg' сохранен в папке 'result'")
  bg.close()

if __name__ == '__main__':
  main()
  input("\n Программа закончила работу\n Нажмите 'Enter' чтобы закрыть программу")