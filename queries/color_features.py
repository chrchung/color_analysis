import sqlite3
from scipy import stats
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def parse_color_list():
    res = []
    with open('../query_results/thresholded.txt', 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

def parse_features():
    res = {}

    with open('../extended_colors.csv', 'r') as f:
        for row in f:
            row = row.strip('\n')
            row = row.split(',')

            res[row[0]] = {}

            res[row[0]]['bec'] = row[2]
            res[row[0]]['cao'] = row[4]

    return res

col = parse_color_list()
fea = parse_features()

f = open('../query_results/fea.txt', 'w')

f.write('bec,cao\n')
for c in col:
 #   f.write(fea[c]['bec'] + ',' + fea[c]['cao'] + '\n')
 if c not in fea:
     print(c)


f.close()
