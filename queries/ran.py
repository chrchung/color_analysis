import json

to = json.loads(open('../query_results/total_occurence_per_color.json', 'r').read())


f = open('../query_results/total_occurences_per_color.csv', 'w')

for color in to:
    f.write(color + ',' + str(to[color]) + '\n')

f.close()
