from genericpath import exists
from os import listdir, makedirs
from os.path import exists
from sys import exit
from math import ceil
from PIL import Image

ITEMS_MARGIN = 10
LAYOUT_WIDTH = 1754
LAYOUT_HEIGHT = 1240
IMAGE_WIDTH = 185
IMAGE_HEIGHT = 165
HORIZONTAL_AMOUNT = LAYOUT_WIDTH // IMAGE_WIDTH
VERTICAL_AMOUNT = LAYOUT_HEIGHT // IMAGE_HEIGHT
IMAGE_RESOLUTION = IMAGE_WIDTH / IMAGE_HEIGHT
LAYOUT_PADDING_HORIZONTAL = (LAYOUT_WIDTH - IMAGE_WIDTH*HORIZONTAL_AMOUNT - HORIZONTAL_AMOUNT*ITEMS_MARGIN) // 2
LAYOUT_PADDING_VERTICAL = (LAYOUT_HEIGHT - IMAGE_HEIGHT*VERTICAL_AMOUNT - VERTICAL_AMOUNT*ITEMS_MARGIN) // 2

def resize_img(img):
  img_w, img_h = img.size
  w, h = IMAGE_WIDTH, IMAGE_HEIGHT
  img_resolution = img_w / img_h
  if img_resolution != IMAGE_RESOLUTION and img_resolution != 1:
    if img_resolution < 1:
      w = int(h * img_resolution)
    else:
      h = int(w * img_h / img_w)
  return img.resize([w, h], resample=0)


def resize_images(images):
  return [resize_img(img) for img in images]


def get_fullname(name: str, lst: list):
  for el in lst:
    if el.find(name) != -1:
      print(f'Найдено совпадение {el}\n')
      return el
  print(f'Не найдено совпадений для {name}\n')
  return None


def get_image_names():
  folder_items = listdir()
  image_files = []
  print("Введите список конфет. Чтобы закончить введите '0'")
  counter = 1
  while True:
    inp = input(f'{counter}: ').replace('?', '').replace('"', '').strip(' ')
    if not inp or inp == '0': break
    image_files.append(get_fullname(inp, folder_items))
    counter += 1
  return image_files


def load_image(src):
  img = Image.open(f'{src}')
  img.load()
  return img


def get_images(file_names):
  return [load_image(name) for name in file_names if name]


images = resize_images(get_images(get_image_names()))
ll = len(images)
print(f'Всего изображений: {ll}\nКоличество строк: {HORIZONTAL_AMOUNT}\nКоличество столбцев: {VERTICAL_AMOUNT}')
layout_name = input('Введите название сгенерированной картинки: ') or 'test'
if not exists('result'):
  makedirs('result')

layout_number = 1
pasted_counter = 0
is_ended = False
while not is_ended:
  x_offset = LAYOUT_PADDING_HORIZONTAL + ITEMS_MARGIN
  y_offset = LAYOUT_PADDING_VERTICAL + ITEMS_MARGIN
  layout = Image.new('RGB', [LAYOUT_WIDTH, LAYOUT_HEIGHT], 'white')
  while not is_ended and x_offset < LAYOUT_WIDTH - LAYOUT_PADDING_HORIZONTAL:
    while not is_ended and y_offset < LAYOUT_HEIGHT - LAYOUT_PADDING_VERTICAL:
      x_offset_centred = x_offset + (IMAGE_WIDTH - images[pasted_counter].size[0]) // 2 
      y_offset_centred = y_offset + (IMAGE_HEIGHT - images[pasted_counter].size[1]) // 2 
      try:
        layout.paste(images[pasted_counter], (x_offset_centred, y_offset_centred), mask=images[pasted_counter].split()[3])
      except:
        layout.paste(images[pasted_counter], (x_offset_centred, y_offset_centred))
      y_offset += IMAGE_HEIGHT + ITEMS_MARGIN
      pasted_counter += 1
      if pasted_counter >= ll:
        is_ended = True
    y_offset = LAYOUT_PADDING_VERTICAL
    x_offset += IMAGE_WIDTH + ITEMS_MARGIN
  layout.save(f'result/{layout_name}-{layout_number}.jpg')
  print(f"Файл '{layout_name}-{layout_number}.jpg' сохранен в папке 'result'")
  layout_number += 1

input("\nПрограмма закончила работу\nНажмите 'Enter' чтобы закрыть программу")