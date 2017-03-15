import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def sentence_per_period(period):
    period = period.split('_')

    start = period[0]
    finish = period[1]
    
    query = 'SELECT count(*) FROM sentence WHERE (sentence.height >= ' +\
            start + ' AND sentence.height < ' + finish + ') AND sentence.height >= 0' 
    
    c.execute(query)

    return c.fetchone()[0]

# go through each decade and get the total text count
periods = ['0_6','6_8', '8_10', '10_13', '13_16', '16_19', '19_21', '21_28', '28_40', '40_60', '60_80', '80_100', '100_1000']

res = {}

for period in periods:
    res[period] = sentence_per_period(period)
    
# save results as json
f = open('../query_results/height_distribution.txt', 'w')
f.write(json.dumps(res))
f.close()

    
