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


mentions = json.loads(open('../query_results/indiv_color_mention_per_decade.txt', 'r').read())
wc = json.loads(open('../query_results/word_count_per_decade.txt', 'r').read())
co = parse_color_list()
to = json.loads(open('../query_results/total_occurence_per_color.json', 'r').read())
decades = ['1800_1810', '1810_1820', '1820_1830', '1830_1840', '1840_1850', '1850_1860', '1860_1870', '1870_1880', '1880_1890', '1890_1900']
to_wc = sum([int(wc[decade]) for decade in wc])

res = []
for color in co:
    stat = {'name': color, 'occur': to[color], 'expected': [], 'actual': [], 'ratio': [], 'p': []}
    
    for decade in decades:
        length = decade
        expected = to[color] * wc[length] / to_wc

        actual = mentions[length][color] if color in mentions[length].keys() else 0
        ratio = actual / expected if expected else 0
        
        stat['expected'].append(expected)
        stat['actual'].append(actual)
        stat['ratio'].append(ratio)

        stat['p'].append(abs(actual - expected) / expected)
        
    res.append(stat)
    
res2 = []
for color in res:
    stat = {'name': color['name'], 'p': color['p']}
    res2.append(stat)

f = open('../query_results/distinctive_decades.json', 'w')
f.write(json.dumps(res2))
f.close()

m = 1000
c = 0
avg = 0
count = 0
for color in res2:
    rat = color['p']
    avg += sum(rat)
    count += len(rat)

    m = min(rat) if min(rat) < m else m
    c = max(rat) if max(rat) > c else c


