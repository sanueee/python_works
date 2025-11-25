import csv
import requests
from collections import Counter

url = 'https://dfedorov.spb.ru/python3/sport.txt'
response = requests.get(url)
response.encoding = 'cp1251'

with open('../sport.txt', 'w', encoding='cp1251') as f:
    f.write(response.text)

sports = Counter()

with open('../sport.txt', 'r', encoding='cp1251') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    for row in reader:
        sport = row[3].strip().split(',')
        for elem in sport:
            good = elem.lower().strip()
            if good:
                sports[good] += 1

print(sports.most_common(3))