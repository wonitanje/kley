from os import listdir
import json

for file in listdir('assets'):
  if 'db.json' in file:
    db_filename = file
    break

with open(f'assets/{db_filename}', 'r', encoding='utf-8') as json_file:
  DB = json.load(json_file)