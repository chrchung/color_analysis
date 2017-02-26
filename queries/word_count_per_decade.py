import sqlite3
from scipy import stats
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def word_count_per_decade(period):
    period = period.split('_')

    start = period[0]
    finish = period[1]
    
    query = 'SELECT count(*) FROM sentence, book ' + \
            'WHERE sentence.book = book.id AND ' + \
            '(book.year >= ' + start + ' AND book.year < ' + finish + ')'
    
    c.execute(query)

    return c.fetchone()[0]

# go through each decade and get the total text count
decades = ['1800_1810', '1810_1820', '1820_1830', '1830_1840', '1840_1850', '1850_1860', '1860_1870', '1870_1880', '1880_1890', '1890_1900']

res = {}

for decade in decades:
    res[decade] = word_count_per_decade(decade)
    
# save results as json
f = open('../query_results/word_count_per_decade.txt', 'w')
f.write(json.dumps(res))
f.close()

    

