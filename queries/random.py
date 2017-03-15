import sqlite3
from scipy import stats
import json
from numpy import percentile
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()


q = "select num_dep from sentence"

c.execute(q)

vals = []


for row in c.fetchall():
    vals.append(int(row[0]))



print(percentile(vals, 99))
print(percentile(vals, 95))
print(percentile(vals, 90))
print(percentile(vals, 80))
print(percentile(vals, 70))
print(percentile(vals, 60))
print(percentile(vals, 50))
print(percentile(vals, 40))
print(percentile(vals, 30))
print(percentile(vals, 20))
print(percentile(vals, 10))
