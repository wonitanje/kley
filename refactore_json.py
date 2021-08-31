import json
from regexp import compile

with open('inventory.json', 'r', encoding='utf-8') as json_file:
  js = json.load(json_file)
  dicts = js[js.keys()[0]]

with open('refactored.json', 'w', encoding='utf-8') as json_file:
  db = {}
  for dict in dicts:
    key = compile(dict['name'])
    db[key] = dict
  json.dump(db, json_file, ensure_ascii=False)