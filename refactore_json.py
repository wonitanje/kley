import json

with open('inventory.json', 'r', encoding='1251') as json_file:
  # print(json_file.read())
  data = json.load(json_file)['sweet']
  # print(data)

with open('refactored.json', 'w', encoding='1251') as json_file:
  for item in data:
    item['image'] = item['image'].lower().replace(',', '').replace(' ', '_')
    # print(json.dump(item, ))
    json_file.write(f'{json.dumps(item, ensure_ascii=False)},\n')