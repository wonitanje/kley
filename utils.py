from os import listdir
from PIL import Image
from regexp import compile, strip_format, format

def resize_img(image: Image, width: int, height: int, resolution: float):
  img_w, img_h = image.size
  img_resolution = img_w / img_h
  if img_resolution == 1:
    width = height = min(width, height)
  elif img_resolution != resolution:
    if img_resolution < 1:
      new_width = int(height * img_resolution)
      if (new_width > width):
        height = int(width * img_h / img_w)
      else: width = new_width
    else:
      new_height = int(width * img_h / img_w)
      if (new_height > height): 
        width = int(height * img_resolution)
      else: height = new_height

  resized = image.resize([width, height], resample=0)
  resized.amount = image.amount
  resized.source = image.source
  resized.key = image.key
  return resized


def resize_images(images: list, width: int, height: int, resolution: float):
  return [resize_img(img, width, height, resolution) for img in images]


def find(lst: list, item):
  try:
    idx = lst.index(item)
  except:
    idx = -1
  return idx


def get_full_filename(name: list, path: str):
  folder_items = [file for file in listdir(path) if format(file) in ['.png', '.jpg', '.jpeg']]
  compiled_folder_items = [strip_format(compile(el)) for el in folder_items]
  idx = find(compiled_folder_items, compile(name[0]))
  if idx == -1:
    idx = find(compiled_folder_items, compile(name[1]))
  if idx == -1:
    print(f'Не найдено совпадений для {name}\n')
    return None
  print(f'Найдено совпадение {folder_items[idx]}\n')
  return folder_items[idx]


def get_filenames(path: str, db: dict):
  image_files = []
  print("Введите список конфет. Чтобы закончить введите '0'")
  counter = 1
  while True:
    inp = input(f'{counter}: ')
    counter += 1
    if inp == '0': break
    filename = db_filename(inp, db)
    if filename == None: continue
    db_key = compile(filename[2])
    fullname = get_full_filename(filename, path)
    if fullname == None: continue
    image_files.append([fullname, db_key])

  filtred = []
  for [img, db_key] in image_files:
    if len(filtred) > 0:
      images, _, _ = zip(*filtred) 
      if img in images: continue
    amount = image_files.count([img, db_key])
    filtred.append([img, amount, db_key])
  return filtred


def load_image(source: str, amount: int, key: str, path: str):
  img = Image.open(f'{path}/{source}').convert('RGBA')
  img.amount = amount
  img.source = source
  img.key = key
  return img


def get_images(name_amount_keyDB: list, path: str):
  print('\nЗагружаю изображения\n')
  return [load_image(src, amount, key, path) for src, amount, key in name_amount_keyDB]


def db_name(key: str, db: dict):
  return db[key]


def db_filename(name: str, db: dict):
  db_key = compile(name)
  item = db.get(db_key, None)
  if item is None:
    for [key, value] in db.items():
      # if name in value['name'] or value['name'] in name or name in value['image'] or value['image'] in name:
      if compile(name) == compile(value['name']) or compile(name) == compile(value['image']):
        return value['name'], value['image'], key
    print(f'{name} не найдено в базе')
    return None
  return item['name'], item['image'], db_key


def to_multiline(line, font, width, lines=1000):
  line_height = font.getsize(line)[1]
  words = line.split()
  words_beg = shift = iter = 0
  words_len = words_end = len(words)
  multiline_shifter = 0

  while words_beg < words_len:
    line_width = font.getsize(''.join(words[words_beg:words_end]))[0]
    while line_width > width - 15:
      words_end -= 1
      line_width = font.getsize(''.join(words[words_beg:words_end]))[0]
    lines -= 1
    words_beg = words_end if (words_beg != words_end) else words_end + 1
    words[words_end - 1] += '\n'
    iter += 1
    shift += line_height + multiline_shifter
    multiline_shifter = -2
    if lines == 0: 
      words = words[:words_end]
      break
    words_end = words_len

  line = ''.join(map(lambda el: el if '\n' in el else f'{el} ', words))
  return line, shift