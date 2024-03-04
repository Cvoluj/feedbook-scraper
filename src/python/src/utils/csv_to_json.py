import json
import csv

def convert_csv_to_json(csv_file, json_file):
    proxies = []
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            proxy = row[0].split(',')[0].replace('"', '')
            row = row[0].split(',')[1].replace('"', '')
            proxies.append({'proxy': proxy + ':' + row, 'auth': None})

    with open(json_file, 'w') as jsonfile:
        json.dump(proxies, jsonfile, indent=4)

csv_file = 'proxy_list.csv'
json_file = 'proxy_list.json'

convert_csv_to_json(csv_file, json_file)