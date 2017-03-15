import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def data(co):
    query = """SELECT color.name, avg(sentence.height), avg(sentence.num_dep), avg(sentence.periodicity) FROM color, mention, sentence, clause, book
    WHERE mention.color=color.id AND mention.clause=clause.id
    AND clause.sentence=sentence.id AND sentence.book=book.id GROUP BY color.name"""
    
    c.execute(query)

    res = []
    for row in c.fetchall():
        n = {}
        n['name'] = row[0]

        if n['name'] in co:
            n['height'] = row[1]
            n['clause'] = row[2]
            n['period'] = row[3]

            res.append(n)

    return res
            
def parse_color_list(f):
    res = []
    with open(f, 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

co = parse_color_list('../query_results/thresholded.txt')


res = data(co)

# save results as json
f = open('../query_results/pca_data.txt', 'w')
f.write(json.dumps(res))
f.close()

    
