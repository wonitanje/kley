from os import listdir
from PIL import Image
import constants as const

def resize_img(img):
  img_w, img_h = img.size
  w, h = const.IMAGE_WIDTH, const.BLOCK_HEIGHT
  img_resolution = img_w / img_h
  if img_resolution != const.IMAGE_RESOLUTION and img_resolution != 1:
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
  folder_items = listdir(const.FOLDER_NAME)
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
  img = Image.open(f'{const.FOLDER_NAME}/{src}')
  img.load()
  return img


def get_images(file_names):
  return [load_image(name) for name in file_names if name]