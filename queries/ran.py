import sqlite3
from scipy import stats
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

query = """SELECT count(*) FROM color"""

to = json.loads(open('../query_results/total_occurence_per_color.json', 'r').read())

c.execute(query)

print(c.fetchone())

##def parse_color_list():
##    res = []
##    with open('../query_results/thresholded.txt', 'r') as f:
##        for row in f:
##            row = row.strip('\n')
##            res.append(row) 
##
##    f.close()
##    return res
##
##co = parse_color_list()
##
##s = 0
##for color in co:
##    print(to[color])
##


