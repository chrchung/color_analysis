import json
from numpy import array, percentile

def parse_color_list(f):
    res = []
    with open(f, 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

f = open('../query_results/distinctive_periods.json', 'r').read()
res = json.loads(f)
##f2 = open('../query_results/spreadsheet_clause2.csv', 'w')

vals = []
count = 0
m = 100000000
c = 0
for color in res:
    vals.extend([-1 * x for x in color['p']])
##    avg += sum(rat)
##    count += len(rat)
##
    rat = color['p']
    m = min(rat) if min(rat) < m else m
    c = max(rat) if max(rat) > c else c

print(percentile(vals, 99))
print(percentile(vals, 95))
print(percentile(vals, 90))
print(percentile(vals, 80))
print(percentile(vals, 70))
print(percentile(vals, 60))
print(percentile(vals, 50))
print(percentile(vals, 40))
print(percentile(vals, 30))
print(percentile(vals, 20))
print(percentile(vals, 10))
