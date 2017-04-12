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
decades = ['0_2','2_4', '4_8', '8_15', '15_24', '24_47', '47_60', '60_80', '80_100', '100_150', '150_200', '200_1000']


to_wc = sum([int(wc[decade]) for decade in wc])

res = []
for color in co:
    stat = {'name': color, 'occur': to[color], 'expected': [], 'actual': [], 'ratio': [], 'p': [], 'percent':[]}
    
    for decade in decades:
        length = decade
        expected = to[color] * wc[length] / to_wc

        actual = mentions[length][color] if color in mentions[length].keys() else 0
        ratio = actual / expected if expected else float('inf')
        
        stat['expected'].append(expected)
        stat['actual'].append(actual)
        stat['ratio'].append(ratio)
        stat['percent'].append(actual / to[color])
        stat['p'].append(abs(actual - expected) / expected if expected else float('inf'))


    #print(str(sum(stat['actual'])) + ' ' + str(to[color]))

        
    res.append(stat)


    
res2 = []
for color in res:
    stat = {'name': color['name'], 'actual': color['actual']}
    res2.append(stat)

f = open('../query_results/distinctive_periods.json', 'w')
f.write(json.dumps(res))
f.close()
