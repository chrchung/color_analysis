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
    
    query = """SELECT color.name, count(*) FROM mention, clause, sentence, book, color WHERE mention.color = color.id AND mention.clause = clause.id AND clause.sentence = sentence.id AND sentence.book = book.id AND (book.year >= """ +start + """ AND book.year < """ + finish + """) GROUP BY color.name"""
    
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
decades = ['1800_1810', '1810_1820', '1820_1830', '1830_1840', '1840_1850', '1850_1860', '1860_1870', '1870_1880', '1880_1890', '1890_1900']
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
f = open('../query_results/word_count_per_decade.txt', 'w')
f.write(json.dumps(res))
f.close()

    
