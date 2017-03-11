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


mentions = json.loads(open('../query_results/color_mentions_per_period.txt', 'r').read())
wc = json.loads(open('../query_results/period_distribution.txt', 'r').read())
co = parse_color_list()
to = json.loads(open('../query_results/total_occurence_per_color.json', 'r').read())
decades = ['-1_1','1_2', '2_3', '3_4', '4_7', '7_14', '14_23', '23_46', '46_1000']

to_wc = sum([int(wc[decade]) for decade in wc])

res = []
for color in co:
    stat = {'name': color, 'occur': to[color], 'expected': [], 'actual': [], 'ratio': [], 'p': []}
    
    for decade in decades:
        length = decade
        expected = to[color] * wc[length] / to_wc

        actual = mentions[length][color] / wc[decade] if color in mentions[length].keys() else 0
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

f = open('../query_results/distinctive_heights.json', 'w')
f.write(json.dumps(res2))
f.close()
