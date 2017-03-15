import json

##name = 'tree_heights'
##js = json.loads(open('../query_results/distinctive_heights.json', 'r').read())
##cats = ['0_5','6_7', '8_9', '10_12', '13_15', '16_18', '19_20', '21_27', '28_39', '40_59', '60_79', '80_99', '100_999']


##name = 'periods'
##js = json.loads(open('../query_results/distinctive_periods.json', 'r').read())
##cats = ['0_1','2_3', '4_7', '8_14', '15_23', '24_46', '47_59', '60_79', '80_99', '100_149', '150_199', '200+']


name = 'num_dependent_clauses'
js = json.loads(open('../query_results/clause_dep.json', 'r').read())
cats = ['0_0', '1_1', '2_2', '3_3', '4_4', '5_5', '6_9', '10_20', '21_30', '31_40', '41+']

name = 'sentence_legnths'
js = json.loads(open('../query_results/sentences.json', 'r').read())
cats = ['0_3', '4_6', '7_9', '10_12', '13_16', '16_20', '21_25', '26_33', '34_44', '45_57', '58_87', '88_150', '151_199', '200+']



spreadsheets = ['expected', 'actual', 'percent', 'ratio', 'p']

for s in spreadsheets:
    f = name + '_' + s + '.csv'
    f = open('../query_results/' + f, 'w')

    f.write(','.join(['color'] + cats) + '\n')

    for color in js:
        f.write(','.join([color['name']] + list(map(str, color[s]))) + '\n')
    
    f.close()



