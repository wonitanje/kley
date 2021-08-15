from os import listdir
from PIL import Image
import constants as const

def resize_img(img: Image):
  img_w, img_h = img.size
  w, h = const.IMAGE_WIDTH, const.BLOCK_HEIGHT
  img_resolution = img_w / img_h
  if img_resolution != const.IMAGE_RESOLUTION and img_resolution != 1:
    if img_resolution < 1:
      w = int(h * img_resolution)
    else:
      h = int(w * img_h / img_w)
  resized = img.resize([w, h], resample=0)
  resized.amount = img.amount
  return resized


def resize_images(images: list):
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

  filtred = []
  for img in image_files:
    if len(filtred) > 0:
      images, _ = zip(*filtred)
      if img in images: continue
    amount = image_files.count(img)
    filtred.append([img, amount])
  print(f'{filtred=}')
  return filtred


def load_image(name_amount_pair: list):
  src = name_amount_pair[0]
  amount = name_amount_pair[1]
  img = Image.open(f'{const.FOLDER_NAME}/{src}')
  img.load()
  img.amount = amount
  return img


def get_images(name_amount_pairs: list):
  return [load_image(pair) for pair in name_amount_pairs]