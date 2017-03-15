import sqlite3
from scipy import stats
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def indiv_color_mentions_per_decade(period):
    res = {}
    period = period.split('_')

    start = period[0]
    finish = period[1]
    
    query = """SELECT color.name, count(*) FROM mention, clause, sentence, book, color WHERE mention.color = color.id AND mention.clause = clause.id AND clause.sentence = sentence.id AND sentence.book = book.id AND (sentence.height >= """ +start + """ AND sentence.height < """ + finish + """) GROUP BY color.name"""
    
    c.execute(query)

    for row in c.fetchall():
        res[row[0]] = row[1]

    return res

def parse_color_list():
    res = []
    with open('../query_results/thresholded.txt', 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

# go through each decade and get the total text count
decades = ['0_6','6_8', '8_10', '10_13', '13_16', '16_19', '19_21', '21_28', '28_40', '40_60', '60_80', '80_100', '100_1000']

res = {}

co = parse_color_list()


for decade in decades:
    decade_res = indiv_color_mentions_per_decade(decade)

    res[decade] = {}

    for color in co:
        if color in decade_res.keys():
            res[decade][color] = decade_res[color]
        else:
            res[decade][color] = 0
    
# save results as json
f = open('../query_results/color_mentions_per_height.txt', 'w')
f.write(json.dumps(res))
f.close()

    
