import sqlite3
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()


# distribution of clauses
query = """SELECT num_dep + num_indep, count(*) FROM sentence
    GROUP BY num_dep + num_indep"""

c.execute(query)

f = open('../query_results/results.txt', 'w')
f.write(str(c.fetchall()))

f.close()
