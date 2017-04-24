import sqlite3
import json
conn = sqlite3.connect('../color_analysis_merged.db')
c = conn.cursor()

# get list of colors
def parse_color_list():
    res = []
    with open('../query_results/thresholded.txt', 'r') as f:
        for row in f:
            row = row.split(',')
            res.append(row[0].strip('\n'))
    return res


def parse_sentence_list():
    res = "(" 
    with open('../query_results/valid_sentences.json', 'r') as f:
        res = res + f.read().strip('\n')

    return res + ")"

def sentences_in_range(r):
    r = r.split('_')
    start = r[0]
    finish = r[1]

    query = """SELECT count(DISTINCT sentence.id) FROM sentence, mention, clause, color
    WHERE mention.color = color.id AND mention.clause = clause.id AND
    clause.sentence = sentence.id AND mention.type != 'verb' AND mention.type != 'noun' AND
    color.name IN """ + sen + """ AND (""" + measure + """>=""" +\
    start + ' AND ' + measure + '< ' + finish + ') AND ' + measure + '>= 0'
    
    c.execute(query)


    return c.fetchone()[0]

def indiv_color_mentions_per_range(r):
    res = {}
    r = r.split('_')

    start = r[0]
    finish = r[1]
    query = """SELECT color.name, count(*) FROM mention,
clause, sentence, color WHERE mention.color = color.id AND
mention.clause = clause.id AND mention.type != 'verb' AND mention.type != 'noun' AND
clause.sentence = sentence.id AND (""" + measure + """ >= """ +start + """
AND """ + measure + """ < """ + finish + """) GROUP BY color.name"""

    c.execute(query)

    for row in c.fetchall():
        res[row[0]] = row[1]

    return res

def sentences_in_binary_range(r):
    res = {}
    query = """SELECT count(sentence.id) FROM sentence, mention, clause, color
WHERE mention.color = color.id AND mention.clause = clause.id AND
clause.sentence = sentence.id AND 
color.name IN """ + sen + """ AND """ + measure + """='""" + r + """'"""

    c.execute(query)

    return c.fetchone()[0]

def indiv_color_mentions_per_binary_range(r):
    res = {}
    query = """SELECT color.name, count(*) FROM mention,
clause, sentence, color WHERE mention.color = color.id AND
mention.clause = clause.id AND
clause.sentence = sentence.id AND """ + measure + """ = '""" + r + """' GROUP BY color.name"""

    c.execute(query)

    for row in c.fetchall():
        res[row[0]] = row[1]

    return res


def pipeline(measure, ranges, res_file, binary=False):
    num_sent_per_rang = {}
    for rang in ranges:
        if binary:
            num_sent_per_rang[rang] = sentences_in_binary_range(rang)
        else:
            num_sent_per_rang[rang] = sentences_in_range(rang)
        
    indiv_color_mentions_per_rang = {}
    for rang in ranges:
        if binary:
            num_mentions = indiv_color_mentions_per_binary_range(rang)           
        else:
            num_mentions = indiv_color_mentions_per_range(rang)

        indiv_color_mentions_per_rang[rang] = {}

        for color in col:
            if color in num_mentions.keys():
                indiv_color_mentions_per_rang[rang][color] = num_mentions[color]
            else:
                indiv_color_mentions_per_rang[rang][color] = 0

    to_wc = sum([int(num_sent_per_rang[rang]) for rang in num_sent_per_rang])
    print(to_wc)

    res = []
    for color in col:
        stat = {'name': color, 'occur': to[color], 'expected': [], 'actual': [], 'ratio': [], 'p': [], 'percent': []}
        
        for rang in ranges:
            length = rang
            expected = to[color] * num_sent_per_rang[length] / to_wc

            actual = indiv_color_mentions_per_rang[length][color] if color in indiv_color_mentions_per_rang[length].keys() else 0
            ratio = actual / expected if expected else float('inf')
            
            stat['expected'].append(expected)
            stat['actual'].append(actual)
            stat['ratio'].append(ratio)
            stat['percent'].append(actual / to[color])
            stat['p'].append(abs(actual - expected) / expected if expected else float('inf'))
            
        res.append(stat)

    f = open('../query_results/' + res_file, 'w')
    f.write(json.dumps(res))
    f.close()

to = json.loads(open('../query_results/total_occurence_per_color.json', 'r').read())
col = parse_color_list()
sen = "('" + "','".join(col) + "')"

measure = "sentence.height"
ranges = ['0_6','6_8', '8_10', '10_13', '13_16', '16_19', '19_21', '21_28', '28_40', '40_60', '60_80', '80_100', '100_1000']
res_file = "heights.json"
pipeline(measure, ranges, res_file)

measure = "sentence.num_dep"
ranges = ['0_1','1_2', '2_3', '3_4', '4_5', '5_6', '6_10', '10_21', '21_31', '31_41', '41_100']
res_file = "num_dependent_clauses.json"
pipeline(measure, ranges, res_file)

measure = "sentence.length"
ranges = ['0_3','3_7', '7_10', '10_13', '13_16', '16_21', '21_26', '26_34', '34_45', '45_58', '58_88', '88_151', '151_200', '200_1000']
res_file = "sentence_length.json"
pipeline(measure, ranges, res_file)

measure = "sentence.periodicity"
ranges = ['0_2','2_4', '4_8', '8_15', '15_24', '24_47', '47_60', '60_80', '80_100', '100_150', '150_200', '200_1000']
res_file = "distintive_periodicity.json"
pipeline(measure, ranges, res_file)

measure = 'mention.type'
ranges = ['pred', 'attr', 'noun', 'verb']
res_file = "distinctive_pred.json"
pipeline(measure, ranges, res_file, True)
