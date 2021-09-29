from os import rename
import json
from regexp import compile

def modify_item(key: str):
  item = DB[key].copy()
  while True:
    print('\n Изменить данные о конфете')
    print(' [0] Сохранить данные')
    print(f' [1] Изображение ({item["image"]})')
    print(f' [2] Название ({item["name"]})')
    print(f' [3] Производитель ({item["sire"]})')
    print(f' [4] Вес ({item["weight"]})')
    print(f' [5] Описание ({item["description"]})')
    mode = input('- Ввод: ')
    if mode == '0': break
    elif mode == '1': 
      item['image'] = input('- Введите название изображения: ')
    elif mode == '2':
      item['name'] = input('- Введите название конфеты: ')
    elif mode == '3':
      item['name'] = input('- Введите производителя: ')
    elif mode == '4':
      item['weight'] = input('- Введите вес: ')
    elif mode == '5':
      item['description'] = input('- Введите описание: ')
    else: print(' Не корректный ввод')
  new_key = compile(img)
  if key != new_key:
    DB.popkey(key)
  DB[new_key] = item
  print(' Данные о конфете сохранены. Перезапись выполнится перед концом программы')

def add_item(key: str, img: str):
  print(' Конфета не найдена в базе. Хотите добавить?')
  print('[1] Да, добавить новую конфету')
  print('[2] Нет, ввести другое название (по умолчанию)')
  if input('- Введите 1 или 2: ').strip() != '1':
    return
  key = compile(img)
  DB[key]["image"] = img
  print(' Введите данные о конфете')
  DB[key]["name"] = input('- Название: ')
  DB[key]["sire"] = input('- Производитель: ')
  DB[key]["weight"] = input('- Вес: ')
  DB[key]["description"] = input('- Описание: ')
  print(' Добавлена конфета', DB[key])

if __name__ == '__main__':
  with open('db.json', 'r', encoding='utf-8') as json_file:
      DB = json.load(json_file)

  while True:
    print("\n[?] Введите '0' чтобы закончить")
    img = input('- Введите название изображения: ')
    key = compile(img)
    if img == None or img == '0': 
      break
    if DB.get(key, None) is not None:
      modify_item(key)
    else:
      add_item(key, img)

  rename('db.json', 'db_old.json')
  with open('db.json', 'w', encoding='utf-8') as json_file:
    json.dump(DB, json_file, ensure_ascii=False)