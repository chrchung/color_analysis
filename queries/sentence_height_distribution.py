import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def sentence_per_period(period):
    period = period.split('_')

    start = period[0]
    finish = period[1]
    
    query = """SELECT count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format + """ AND (sentence.height >=""" +\
start + ' AND sentence.height < ' + finish + ') AND sentence.height >= 0' 
    
    c.execute(query)

    return c.fetchone()[0]

# go through each decade and get the total text count
periods = ['0_6','6_8', '8_10', '10_13', '13_16', '16_19', '19_21', '21_28', '28_40', '40_60', '60_80', '80_100', '100_1000']

# get list of colors
def parse_color_list():
    res = []
    with open('../query_results/thresholded.txt', 'r') as f:
        for row in f:
            row = row.split(',')
            res.append(row[0].strip('\n'))
    return res

col = parse_color_list()

sql_format = '('

for i in range(0, len(col) - 1):
    sql_format += "'" + col[i] + "',"
sql_format += "'" + col[len(col) - 1] + "'"
sql_format += ')'


res = {}

for period in periods:
    res[period] = sentence_per_period(period)
    
# save results as json
f = open('../query_results/height_distribution.txt', 'w')
f.write(json.dumps(res))
f.close()

    
