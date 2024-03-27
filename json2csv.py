import json

filepath = input('请输入年份: ')

with open(f'{filepath}.json', 'r') as f:
    data = json.load(f)

with open(f'{filepath}.csv', 'w', encoding='utf-8') as f:
    for line in data:
        f.write(line['mids'] + ',' + line['titles'] + ',' + line['views'] + ',' + line['keytags'] + ',' + line['times'] + ',' + line['hrefs'] + '\n')