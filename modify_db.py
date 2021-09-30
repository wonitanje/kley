from os import rename, remove
from os.path import exists
import json
from regexp import compile
from db import DB
from utils import db_filename

def modify_item(key: str):
  item = DB[key].copy()
  while True:
    print('\n Изменить данные о конфете')
    print('[0] Сохранить данные')
    print(f'[1] Изображение ({item["image"]})')
    print(f'[2] Название ({item["name"]})')
    print(f'[3] Производитель ({item["sire"]})')
    print(f'[4] Вес ({item["weight"]})')
    print(f'[5] Описание ({item["description"]})')
    mode = input('- Ввод: ')
    if mode == '0': break
    elif mode == '1': 
      item['image'] = input('- Введите название изображения: ')
    elif mode == '2':
      item['name'] = input('- Введите название конфеты: ')
    elif mode == '3':
      item['sire'] = input('- Введите производителя: ')
    elif mode == '4':
      item['weight'] = input('- Введите вес: ')
    elif mode == '5':
      item['description'] = input('- Введите описание: ')
    else: print(' Не корректный ввод')
  new_key = compile(item['image'])
  if key != new_key:
    DB.pop(key)
  DB[new_key] = item
  print(' Данные о конфете сохранены. Перезапись выполнится перед концом программы')

def add_item(img: str):
  print('\n Конфета не найдена в базе. Хотите добавить?')
  print('[1] Да, добавить новую конфету')
  print('[2] Нет, ввести другое название (по умолчанию)')
  if input('- Введите 1 или 2: ').strip() != '1':
    return
  key = compile(img)
  DB[key] = {}
  DB[key]["image"] = img
  print('\n Введите данные о конфете')
  DB[key]["name"] = input('- Название: ')
  DB[key]["sire"] = input('- Производитель: ')
  DB[key]["weight"] = input('- Вес: ')
  DB[key]["description"] = input('- Описание: ')
  print(' Добавлена конфета', DB[key])

if __name__ == '__main__':
  while True:
    print("\n [?] Введите '0' чтобы закончить")
    img = input('- Введите название изображения: ')
    if img == None or img == '0': 
      break
    keys = db_filename(img, DB)
    if keys is not None:
      modify_item(keys[2])
    else:
      add_item(img)

  if exists('assets/db.old.json'):
    remove('assets/db.old.json')
  db_busy = True
  while db_busy:
    try:
      rename('assets/db.json', 'assets/db.old.json')
      db_busy = False
    except:
      print(' Что-то пошло не так. Скорее всего база занята другой программой')
      print(' Попробовать снова?')
      print('[1] Да (по умолчанию)')
      print('[2] Нет, отменить изменения')
      if input('- Ввод: ') == '2':
        raise Exception

  with open('assets/db.json', 'w', encoding='utf-8') as json_file:
    json.dump(DB, json_file, ensure_ascii=False)