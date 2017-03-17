import json
import numpy as np
from sklearn.decomposition import PCA
import plotly.tools as tls
tls.set_credentials_file(username='ChristinaChung', api_key='9Qz7ub7MJHtBqdy6N6OX')
import plotly.plotly as py
import plotly.graph_objs as go

def parse_color_list(f):
    res = []
    with open(f, 'r') as f:
        for row in f:
            row = row.strip('\n')
            res.append(row) 

    f.close()
    return res

def get_o(ob, name):
    for o in ob:
        if o['name'] == name:
            return o


def parse_hex_list(f):
    res = []
    with open(f, 'r') as f:
        for row in f:
            row = row.strip('\n')
            row = row.split(':')
            res.append(row[1]) 

    f.close()
    return res


hex_values = parse_hex_list('../query_results/colors.txt')

##height = json.loads(open('../query_results/distinctive_heights.json', 'r').read())
##periodicity = json.loads(open('../query_results/distinctive_periods.json', 'r').read())
##clause = json.loads(open('../query_results/clause_dep.json', 'r').read())

co = parse_color_list('../query_results/thresholded.txt')

data = json.loads(open('../query_results/pca_data.txt', 'r').read())
#num_comp = len(data[0]['p'])

num_comp = 3

ar = [[] for x in range(0, num_comp)]

for color in co:
    i = 0
    a = get_o(data, color)

    ar[0].append(a['height'])
    ar[1].append(a['clause'])
    ar[2].append(a['period'])

##        
##    b = get_o(periodicity, color)['p']
##    for comp in b:
##        ar[i].append(comp)
##        i+=1
##        
##    c = get_o(clause, color)['p']
##    for comp in c:
##        ar[i].append(comp)
##        i+=1
    
f = open('../query_results/pca.json', 'w')
f.write(json.dumps(ar))
f.close()

X = np.array(ar)

pca = PCA(n_components=2)
pca.fit(X)

pca_res = list(pca.components_)

data = []

for c in range(0, len(co)):
    trace = go.Scatter(
    x = pca_res[0][c],
    y = pca_res[1][c],
    mode='markers',
    name=co[c],
    textposition='bottom',
    marker={'color': hex_values[c]}
    )

    data.append(trace)

    
py.iplot(data, filename='PCA5')

