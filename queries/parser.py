import sqlite3
from scipy import stats
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

buc = json.loads(open('10.txt', 'r').read())


f = open('10_bac.txt', 'w')

for key in 
