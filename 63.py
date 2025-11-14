import csv
from collections import Counter

sports = Counter()

with open('sport.txt', 'r', encoding='cp1251') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)
    for row in reader:
        sport = row[3].strip().split(',')
        for elem in sport:
            good = elem.lower().strip()
            if good:
                sports[good] += 1


print(sports.most_common(3))