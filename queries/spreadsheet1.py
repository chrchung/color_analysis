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
    query = """SELECT count(*) FROM sentence"""

    c.execute(query)

    return c.fetchone()[0]

def occurence_color_in_length(length_dist):
    res = {}

    for length in length_dist:        
        query = """SELECT color.name, count(*) FROM color, mention, sentence, clause
        WHERE mention.color=color.id AND mention.clause=clause.id
        AND clause.sentence=sentence.id AND
        sentence.length >= """ + str(length[0]) + """ AND sentence.length <= """ + str(length[1]) + """ GROUP BY color.name"""

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
        query = """SELECT count(*) FROM sentence WHERE sentence.length >= """ + str(length[0]) + """ AND sentence.length <= """ + str(length[1])

        c.execute(query)

        res[str(length[0]) + '_' + str(length[1])] = c.fetchone()[0] / num_sentences

    return res
       

co = parse_color_list()
##string_list = stringify_color_list(color_list)
to = json.loads(open('../query_results/total_occurence_per_color.json', 'r').read())

# considering sentence lengths of 0-5, 6-15, etc. 
length_dist = [(0, 3), (4, 6), (7, 9), (10, 12), (13, 16), (16, 20), (21, 25), (26, 33), (34, 44), (45, 57), (58, 87), (88, 150), (151, 199), (200, 1000)]

# number of sentences in corpus
num_sentences = json.loads(open('../query_results/num_sentences.json', 'r').read())

# get total occurrence of sentences for various lengths
pos = percent_occurence_sentences_of_length(length_dist, num_sentences)

oc = occurence_color_in_length(length_dist)

res = []
for color in co:
    stat = {'name': color, 'occur': to[color], 'expected': [], 'actual': [], 'ratio': [], 'p': [], 'percent':[]}
    
    for length in length_dist:
        length = str(length[0]) + '_' + str(length[1])
        expected = to[color] * pos[length]

        actual = oc[length][color] if color in oc[length].keys() else 0
        ratio = actual / expected if expected else 0
        
        stat['expected'].append(expected)
        stat['actual'].append(actual)
        stat['ratio'].append(ratio)
        stat['percent'].append(actual / to[color])

        stat['p'].append(abs(actual - expected) / expected)


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
    



    

