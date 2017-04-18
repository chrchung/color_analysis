import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()
from numpy import percentile



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

res = []

query = """SELECT DISTINCT sentence.id FROM mention, clause, sentence, color, book
WHERE mention.color = color.id AND mention.clause = clause.id AND clause.sentence
= sentence.id AND mention.type != 'verb' AND mention.type != 'noun' AND sentence.book = book.id
AND color.name IN""" + sql_format

                       
c.execute(query)

for item in c.fetchall():
    res.append(str(item[0]))


f = open('../query_results/clause_distribution.txt', 'w')
f.write(','.join(res))
f.close()


##print(percentile(res, 99))
##print(percentile(res, 95))
##print(percentile(res, 90))
##print(percentile(res, 80))
##print(percentile(res, 70))
##print(percentile(res, 60))
##print(percentile(res, 50))
##print(percentile(res, 40))
##print(percentile(res, 30))
##print(percentile(res, 20))
##print(percentile(res, 10))
##
##
