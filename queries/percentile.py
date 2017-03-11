import sqlite3
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()
from numpy import percentile

query = """SELECT height, count(*) FROM sentence GROUP BY height"""

c.execute(query)

res = []

for row in c.fetchall():
    res.append(row[0])


print(percentile(res, 99))
print(percentile(res, 95))
print(percentile(res, 90))
print(percentile(res, 80))
print(percentile(res, 70))
print(percentile(res, 60))
print(percentile(res, 50))
print(percentile(res, 40))
print(percentile(res, 30))
print(percentile(res, 20))
print(percentile(res, 10))


