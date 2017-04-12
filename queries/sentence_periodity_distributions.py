import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def sentences_per_period(period):
    period = period.split('_')

    start = period[0]
    finish = period[1]

    query = """SELECT count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format + """ AND (sentence.periodicity >=""" +\
start + ' AND sentence.periodicity < ' + finish + ') AND sentence.periodicity >= 0'
    
    c.execute(query)

    return c.fetchone()[0]

# go through each decade and get the total text count
periods = ['0_2','2_4', '4_8', '8_15', '15_24', '24_47', '47_60', '60_80', '80_100', '100_150', '150_200', '200_1000']


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
    res[period] = sentences_per_period(period)
    
# save results as json
f = open('../query_results/period_distribution.txt', 'w')
f.write(json.dumps(res))
f.close()

    
