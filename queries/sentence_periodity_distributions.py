import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def sentences_per_period(period):
    period = period.split('_')

    start = period[0]
    finish = period[1]
    
    query = 'SELECT count(*) FROM sentence WHERE (sentence.periodicity >= ' +\
            start + ' AND sentence.periodicity < ' + finish + ') AND sentence.periodicity >= 0'
    
    c.execute(query)

    return c.fetchone()[0]

# go through each decade and get the total text count
periods = ['0_2','2_4', '4_8', '8_15', '15_24', '24_47', '47_60', '60_80', '80_100', '100_150', '150_200', '200_1000']


res = {}

for period in periods:
    res[period] = sentences_per_period(period)
    
# save results as json
f = open('../query_results/period_distribution.txt', 'w')
f.write(json.dumps(res))
f.close()

    
