import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def sentence_per_period(period):
    period = period.split('_')

    start = period[0]
    finish = period[1]
    
    query = 'SELECT count(*) FROM sentence WHERE (sentence.periodicity >= ' +\
            start + ' AND sentence.periodicity < ' + finish + ')'
    
    c.execute(query)

    return c.fetchone()[0]

# go through each decade and get the total text count
periods = ['-1_1','1_2', '2_3', '3_4', '4_7', '7_14', '14_23', '23_46', '46_1000']

res = {}

for period in periods:
    res[period] = sentence_per_period(period)
    
# save results as json
f = open('../query_results/period_distribution.txt', 'w')
f.write(json.dumps(res))
f.close()

    
