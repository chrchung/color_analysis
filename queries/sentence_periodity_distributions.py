import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def sentences_per_period(period):
    period = period.split('_')

    start = period[0]
    finish = period[1]
    
    query = 'SELECT count(*) FROM sentence WHERE (sentence.height >= ' +\
            start + ' AND sentence.height < ' + finish + ')'
    
    c.execute(query)

    return c.fetchone()[0]

# go through each decade and get the total text count
periods = ['3_12.7','12.7_22.4', '22.4_32.1', '32.1_41.8', \
           '41.8_51.5', '51.5_61.2', '61.2_70.9', '70.9_80.6', \
           '80.6_94.6', '94.6_102.15', '102.15_108.09', '108.09_10000']

res = {}

for period in periods:
    res[period] = sentences_per_period(period)
    
# save results as json
f = open('../query_results/height_distribution.txt', 'w')
f.write(json.dumps(res))
f.close()

    
