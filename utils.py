from os import listdir
from PIL import Image

def resize_img(image: Image, width: int, height: int, resolution: float):
  img_w, img_h = image.size
  img_resolution = img_w / img_h
  if img_resolution != resolution and img_resolution != 1:
    if img_resolution < 1:
      width = int(height * img_resolution)
    else:
      height = int(width * img_h / img_w)
  resized = image.resize([width, height], resample=0)
  resized.amount = image.amount
  resized.source = image.source
  return resized


def resize_images(images: list, width: int, height: int, resolution: float):
  return [resize_img(img, width, height, resolution) for img in images]


def get_fullname(name: str, lst: list):
  for el in lst:
    if el.find(name) != -1:
      print(f'Найдено совпадение {el}\n')
      return el
  print(f'Не найдено совпадений для {name}\n')
  return None


def get_image_names(path: str):
  folder_items = listdir(path)
  image_files = []
  print("Введите список конфет. Чтобы закончить введите '0'")
  counter = 1
  while True:
    inp = input(f'{counter}: ').replace('?', '').replace('"', '').strip(' ') # To fix
    counter += 1
    if not inp or inp == '0': break
    if inp == None: continue
    image_files.append(get_fullname(inp, folder_items))

  filtred = []
  for img in image_files:
    if len(filtred) > 0:
      images, _ = zip(*filtred)
      if img in images: continue
    amount = image_files.count(img)
    filtred.append([img, amount])
  return filtred


def load_image(source: str, amount: int, path: str):
  img = Image.open(f'{path}/{source}')
  img.load()
  img.amount = amount
  img.source = source
  return img


def get_images(name_amount_pairs: list, path: str):
  return [load_image(src, amount, path) for src, amount in name_amount_pairs]


def get(file_name: str, db: dict):
  ind = file_name.rindex('.')
  image_name = file_name[:ind]
  return db[image_name]


def to_multiline(line, font, width):
  line_height = font.getsize(line)[1]
  words = line.split()
  words_beg = shift = 0
  words_len = words_end = len(words)

  while words_beg < words_len - 1:
    line_width = font.getsize(''.join(words[words_beg:words_end]))[0]
    while line_width > width - 10:
      words_end -= 1
      line_width = font.getsize(''.join(words[words_beg:words_end]))[0]
    shift += line_height
    words_beg = words_end - 1 if words_end - words_beg != 1 else words_end
    words_end = words_len
    words[words_beg] += '\n'

  line = ''.join(map(lambda el: el if '\n' in el else f'{el} ', words))
  return line, shift