import json
from regexp import compile

with open('assets/inventory.json', 'r', encoding='utf-8') as json_file:
  js = json.load(json_file)
  dicts = js[list(js.keys())[0]]

with open('assets/refactored.json', 'w', encoding='utf-8') as json_file:
  db = {}
  for d in dicts:
    key = compile(d['image'].strip())
    db[key] = d
  json.dump(db, json_file, ensure_ascii=False)