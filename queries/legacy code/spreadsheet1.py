import sqlite3
from scipy import stats
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

def total_occurence_per_color():
    res = {}
##    query = """SELECT color.name, count(*) FROM color, mention, sentence, clause, book
##    WHERE mention.color=color.id AND mention.clause=clause.id
##    AND clause.sentence=sentence.id AND sentence.book=book.id AND
##    book.id and color.name IN """ + color_list + """ GROUP BY color.name"""

    query = """SELECT color.name, count(*) FROM color, mention
    WHERE mention.color=color.id GROUP BY color.name"""

    c.execute(query)

    for row in c.fetchall():
        color = row[0]
        count = row[1]

        res[color] = count

    return res
       
def parse_color_list():
    res = []
    with open('../query_results/thresholded.txt', 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

def stringify_color_list(color_list):
    res = "("
    for color in color_list:
        res = res + "'" + color + "'" + ","

    res = res[0:len(res) - 1] + ")"

    return res

def number_of_sentences_in_corpus():
    query = """SELECT DISTINCT count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format
    
    c.execute(query)

    return c.fetchone()[0]

def occurence_color_in_length(length_dist):
    res = {}


    for length in length_dist:        
##        query = """SELECT color.name, count(*) FROM color, mention, sentence, clause
##        WHERE mention.color=color.id AND mention.clause=clause.id
##        AND clause.sentence=sentence.id AND
##        sentence.length >= """ + str(length[0]) + """ AND sentence.length <= """ + str(length[1]) + """ GROUP BY color.name"""

        start = str(length[0])
        finish = str(length[1])

        query = """SELECT color.name, count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format + """ AND (sentence.length >=""" +\
start + ' AND sentence.length < ' + finish + ') AND sentence.length >= 0' +\
' GROUP BY color.name'
    
        c.execute(query)

        res[str(length[0]) + '_' + str(length[1])] = {}
        for row in c.fetchall():
            color = row[0]
            count = row[1]
            res[str(length[0]) + '_' + str(length[1])][color] = count
            
    return res

def percent_occurence_sentences_of_length(length_dist, num_sentences):
    res = {}
    
    for length in length_dist:
        start = str(length[0])
        finish = str(length[1])
        
        query = """SELECT DISTINCT count(*) FROM sentence, mention, clause, color
WHERE mention.clause = clause.id AND
clause.sentence = sentence.id AND mention.type != 'noun'
AND mention.type != 'verb' AND mention.color = color.id AND
color.name IN """ + sql_format + """ AND (sentence.length >=""" +\
start + ' AND sentence.length < ' + finish + ') AND sentence.length >= 0'
        
        c.execute(query)

        res[str(length[0]) + '_' + str(length[1])] = c.fetchone()[0] / num_sentences

    return res
       

col = parse_color_list()

sql_format = '('
for i in range(0, len(col) - 1):
    sql_format += "'" + col[i] + "',"
sql_format += "'" + col[len(col) - 1] + "'"
sql_format += ')'

##string_list = stringify_color_list(color_list)
to = json.loads(open('../query_results/total_occurence_per_color.json', 'r').read())

# considering sentence lengths of 0-5, 6-15, etc. 
length_dist = [(0, 3), (4, 7), (7, 10), (10, 13), (13, 16), (16, 21), (21, 26), (26, 34), (34, 45), (45, 58), (58, 88), (88, 151), (151, 200), (200, 1000)]

# number of sentences in corpus
num_sentences = number_of_sentences_in_corpus()

# get total occurrence of sentences for various lengths
pos = percent_occurence_sentences_of_length(length_dist, num_sentences)
print(pos)
oc = occurence_color_in_length(length_dist)

res = []
for color in col:
    stat = {'name': color, 'occur': to[color], 'expected': [], 'actual': [], 'ratio': [], 'p': [], 'percent':[]}
    
    for length in length_dist:
        length = str(length[0]) + '_' + str(length[1])
        expected = to[color] * pos[length]

        actual = oc[length][color] if color in oc[length].keys() else 0
        ratio = actual / expected if expected else float('inf')
        
        stat['expected'].append(expected)
        stat['actual'].append(actual)
        stat['ratio'].append(ratio)
        stat['percent'].append(actual / to[color])

        stat['p'].append(abs(actual - expected) / expected if expected else float('inf'))
    res.append(stat)

f = open('../query_results/spreadsheet_sent.txt', 'w')
f.write(json.dumps(res))
f.close()

res2 = []
for color in res:
    stat = {'name': color['name'], 'p': color['p']}
    res2.append(stat)

f = open('../query_results/sentences.json', 'w')
f.write(json.dumps(res))
f.close()
    



    

